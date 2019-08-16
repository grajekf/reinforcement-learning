import numpy as np
import math

import game.physics
from game.circle import Circle

FOOT_WEIGHT_RATIO = 0.03
FOOT_RADIUS_RATIO = 0.2
EPS = 1e-5

class Player(Circle):

    def __init__(self, position, radius, weight, kick_radius, kick_max_force, kick_wait_time, max_speed, max_run_force):
        super().__init__(position, radius, weight)
        self.foot = Circle(position, radius * FOOT_RADIUS_RATIO, weight * FOOT_WEIGHT_RATIO)
        self.kick_radius = kick_radius
        self.kick_max_force = kick_max_force
        self.max_speed = max_speed
        self.max_run_force = max_run_force
        self.kick_wait_time = kick_wait_time
        self.time_since_last_kick = kick_wait_time

    @classmethod
    def from_config(cls, config):
        player = config["player"]
        radius = player["radius"]
        weight = player["weight"]
        max_v = player["max_velocity"]
        max_run_force = player["max_run_force"]

        kick = player["kick"]
        kick_radius = kick["radius"]
        kick_max_force = kick["max_momentum"]
        kick_wait_time = kick["wait_time"]

        return Player([0, 0], radius, weight, kick_radius, kick_max_force, kick_wait_time, max_v, max_run_force)

    def draw(self, surface, camera, color):
        camera.draw_circle(surface, color, self.position, self.radius)
        camera.draw_circle(surface, (0, 0, 0), self.position, self.radius, 1)
        kick_color = (255, 255, 255) if self.time_since_last_kick >= self.kick_wait_time else (0, 0, 0)
        camera.draw_circle(surface, kick_color, self.position, self.kick_radius, 1)
        # camera.draw_circle(surface, (0, 0, 0), self.foot.position, self.foot.radius)


    def do_kick(self, ball, power):
        if self.time_since_last_kick >= self.kick_wait_time:
            vector_between = ball.position - self.position
            distance = np.sqrt(np.sum((vector_between)**2))

            if distance <= self.kick_radius + ball.radius:
                normal = vector_between / distance
                
                ball_impulse_vector = normal * power * self.kick_max_force

                ball.add_velocity(ball_impulse_vector)

                # maybe reset always when kicking, even when the player misses?
            self.time_since_last_kick = 0

    def accelerate(self, power):
        self.apply_force(power * self.max_run_force)

    def update(self, passed_time):
        super().update(passed_time)
        if self.body.linearVelocity.length > self.max_speed:
            current_velocity = np.array(self.body.linearVelocity)
            normalized = current_velocity / self.body.linearVelocity.length

            new_velocity = self.max_speed * normalized

            print("Max velocity reached!")
            self.body.linearVelocity = new_velocity.tolist()
            
        self.time_since_last_kick += passed_time

    def execute_command(self, command, ball):
        self.accelerate(command.accel)
        if command.kick > 0.0:
            self.do_kick(ball, command.kick)
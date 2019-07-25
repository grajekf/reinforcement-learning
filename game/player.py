import numpy as np
import math

import physics
from entity import Entity

FOOT_WEIGHT_RATIO = 0.03
FOOT_RADIUS_RATIO = 0.2
EPS = 1e-5

class Player(Entity):

    def __init__(self, position, radius, weight, kick_radius, kick_max_force, kick_wait_time, height):
        super().__init__(position, radius, weight)
        self.velocity = np.random.uniform(-5, 5, 2)
        self.foot = Entity(position, radius * FOOT_RADIUS_RATIO, weight * FOOT_WEIGHT_RATIO)
        self.kick_radius = kick_radius
        self.kick_max_force = kick_max_force
        self.height = height
        self.kick_wait_time = kick_wait_time
        self.time_since_last_kick = kick_wait_time

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
                # Foot touches ball
                foot_center_point = ball.position - normal * (ball.radius + self.foot.radius - EPS)
                self.foot.position = foot_center_point
                self.foot.velocity = power * self.kick_max_force * normal

                collided = self.foot.handle_collision(ball)

                self.did_kick = True

                self.time_since_last_kick = 0

    def update(self, passed_time, friction):
        super().update(passed_time, friction)
        # self.acceleration = np.random.uniform(-10, 10, 2)
        self.time_since_last_kick += passed_time
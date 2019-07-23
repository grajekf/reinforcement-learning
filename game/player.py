import numpy as np
import math

import physics

class Player:

    def __init__(self, position, radius, kick_radius, height, weight):
        self.position = np.array(position)
        self.velocity = np.array([0.0, 0.0])
        self.radius = radius
        self.kick_radius = kick_radius
        self.height = height
        self.weight = weight

    def draw(self, surface, camera, color):
        camera.draw_circle(surface, color, self.position, self.radius)
        camera.draw_circle(surface, (0, 0, 0), self.position, self.radius, 1)
        camera.draw_circle(surface, (255, 255, 255), self.position, self.kick_radius, 1)


    def handle_ball_collision(self, ball):
        vector_between = ball.position - self.position
        distance = np.sqrt(np.sum((vector_between)**2))
        if distance <= self.radius + ball.radius:
            normal = vector_between / distance
            # Move player and ball apart
            touch_dist_from_player = distance * (self.radius / (self.radius + ball.radius))
            contact_point = self.position + normal * touch_dist_from_player
            self.position = contact_point - normal * self.radius
            ball.position = contact_point + normal * ball.radius

            # self.velocity = np.array([0, 0])
            # ball.velocity = np.array([0, 0])


            player_vel = np.sqrt(np.sum(self.velocity**2))
            ball_vel = np.sqrt(np.sum(ball.velocity**2))

            player_direction = math.atan2(self.velocity[1], self.velocity[0])
            ball_direction = math.atan2(ball.velocity[1], ball.velocity[0])

            contact_dir = math.atan2(normal[1], normal[0])

            physics.elastic2DCollision(self, ball, player_vel, ball_vel, player_direction, ball_direction, contact_dir)

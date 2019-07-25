
import math
import numpy as np

import physics

class Entity:

    def __init__(self, position, radius, weight, movable = True):
        self.position = np.array(position)
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.radius = radius
        self.weight = weight
        self.movable = movable

    def get_left(self):
        return self.position[0] - self.radius

    def get_right(self):
        return self.position[0] + self.radius   

    def get_top(self):
        return self.position[1] - self.radius

    def get_bottom(self):
        return self.position[1] + self.radius   


    def mul_x_vel(self, factor):
        self.velocity[0] = self.velocity[0] * factor

    def mul_y_vel(self, factor):
        self.velocity[1] = self.velocity[1] * factor

    def set_top(self, value):
        self.position[1] = value + self.radius

    def set_bottom(self, value):
        self.position[1] = value - self.radius

    def set_left(self, value):
        self.position[0] = value + self.radius

    def set_right(self, value):
        self.position[0] = value - self.radius

    def update(self, passed_time, friction):
        self.update_velocity(passed_time, friction)
        self.update_position(passed_time)

    def update_velocity(self, passed_time, friction):
        self.velocity = self.velocity * (1 - friction * passed_time) + self.acceleration * passed_time

    def update_position(self, passed_time):
        self.position = self.position + self.velocity * passed_time


    def handle_collision(self, entity):
        vector_between = entity.position - self.position
        distance = np.sqrt(np.sum((vector_between)**2))
        if distance <= self.radius + entity.radius:
            # print(f"Collision with {type(self).__name__}!")
            normal = vector_between / distance
            # Move self and entity apart
            touch_dist_from_self = distance * (self.radius / (self.radius + entity.radius))
            contact_point = self.position + normal * touch_dist_from_self

            any_movable = False

            if self.movable:
                self.position = contact_point - normal * self.radius
                any_movable = True
            if entity.movable:
                entity.position = contact_point + normal * entity.radius
                any_movable = True

            if not any_movable:
                return

            #Simulate collision
            self_vel = np.sqrt(np.sum(self.velocity**2))
            entity_vel = np.sqrt(np.sum(entity.velocity**2))

            self_direction = math.atan2(self.velocity[1], self.velocity[0])
            entity_direction = math.atan2(entity.velocity[1], entity.velocity[0])

            contact_dir = math.atan2(normal[1], normal[0])

            physics.elastic2DCollision(self, entity, self_vel, entity_vel, self_direction, entity_direction, contact_dir)

            return True
    
        return False

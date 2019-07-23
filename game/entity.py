import numpy as np

class Entity:

    def __init__(self, position, radius, weight):
        self.position = np.array(position)
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.radius = radius
        self.weight = weight

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
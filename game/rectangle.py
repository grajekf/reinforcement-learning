import numpy as np


class Rectangle:
    def __init__(self, position, width, length):
        self.position = np.array(position)
        self.width = width
        self.length = length

        self.left = position[0] - length / 2.0
        self.right = position[0] + length / 2.0
        self.top = position[1] - width / 2.0
        self.bottom = position[1] + width / 2.0


    def is_circle_inside(self, circle):
        return circle.get_left() > self.left and circle.get_right() < self.right and circle.get_top() > self.top and circle.get_bottom() < self.bottom


    def handle_collison(self, circle, vel_multiplier = -1):
        nearest_x = max(self.left, min(circle.position[0], self.right))
        nearest_y = max(self.top, min(circle.position[1], self.bottom))

        nearest_point = np.array([nearest_x, nearest_y])

        center_to_nearest = circle.position - nearest_point

        distance = np.sqrt(np.sum((center_to_nearest)**2))

        if distance > circle.radius:
            return False

        # Circle moves towards the rectangle
        if np.dot(circle.velocity, center_to_nearest) < 0:
            if nearest_x == self.left or nearest_x == self.right:
                circle.mul_x_vel(vel_multiplier)
            if nearest_y == self.top or nearest_y == self.bottom:
                circle.mul_y_vel(vel_multiplier)


        normal = center_to_nearest / distance

        penetration_depth = circle.radius - distance
        penetration_vector = normal * penetration_depth

        circle.position = circle.position - penetration_vector



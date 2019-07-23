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


    def is_circle_inside(self, ball):
        return ball.get_left() > self.left and ball.get_right() < self.right and ball.get_top() > self.top and ball.get_bottom() < self.bottom

import numpy as np
from Box2D import b2PolygonShape


class Rectangle:
    def __init__(self, position, width, length):
        self.position = np.array(position)
        self.width = width
        self.length = length

        self.left = position[0] - length / 2.0
        self.right = position[0] + length / 2.0
        self.top = position[1] - width / 2.0
        self.bottom = position[1] + width / 2.0

    def register_in_world(self, world):
        self.body = world.CreateStaticBody()
        self.body.CreatePolygonFixture(box=(self.length, self.width, self.position.tolist(), 0.0))

    def update(self, passedTime):
        self.position = np.array(self.body.position)

    def is_circle_inside(self, circle):
        return circle.get_left() > self.left and circle.get_right() < self.right and circle.get_top() > self.top and circle.get_bottom() < self.bottom





import numpy as np

from game.rectangle import Rectangle

COLLISION_RECT_DEPTH = 2

class Field(Rectangle):

    def __init__(self, width, length, goal_width, goal_depth):
        super().__init__([0, 0], width, length)
        self.goal_width = goal_width
        self.goal_depth = goal_depth

    @classmethod
    def from_config(cls, config):
        field = config["field"]
        field_length = field["length"]
        field_width = field["width"]

        goal = config["goal"]
        goal_width = goal["width"]
        goal_depth = goal["depth"]

        return Field(field_width, field_length, goal_width, goal_depth)

    def register_in_world(self, world):

        self.boundary = world.CreateStaticBody(position=self.position.tolist())
        self.boundary.CreateEdgeChain([(self.left, self.top), 
            (self.left, -self.goal_width / 2),
            (self.left - self.goal_depth, -self.goal_width / 2),
            (self.left - self.goal_depth, self.goal_width / 2),
            (self.left, self.goal_width / 2),
            (self.left, self.bottom),
            (self.right, self.bottom),
            (self.right, self.goal_width / 2),
            (self.right + self.goal_depth, self.goal_width / 2),
            (self.right + self.goal_depth, -self.goal_width / 2),
            (self.right, -self.goal_width / 2),
            (self.right, self.top),
            (self.left, self.top)])

    def draw(self, surface, camera, color):
        camera.draw_rect(surface, color, self)

        




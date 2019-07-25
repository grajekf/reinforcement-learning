import numpy as np

from rectangle import Rectangle

COLLISION_RECT_DEPTH = 2

class Field(Rectangle):

    def __init__(self, width, length, color, goal_width):
        super().__init__([0, 0], width, length)
        self.color = color
        self.goal_width = goal_width
        upper_collision_rect = Rectangle([0, -width / 2 - COLLISION_RECT_DEPTH / 2], COLLISION_RECT_DEPTH, length  + 2 * COLLISION_RECT_DEPTH)
        bottom_collision_rect = Rectangle([0, width / 2 + COLLISION_RECT_DEPTH / 2], COLLISION_RECT_DEPTH, length  + 2 * COLLISION_RECT_DEPTH)
        left_collision_rect = Rectangle([-length / 2 - COLLISION_RECT_DEPTH / 2, 0], width, COLLISION_RECT_DEPTH)
        right_collision_rect = Rectangle([length / 2 + COLLISION_RECT_DEPTH / 2, 0], width, COLLISION_RECT_DEPTH)

        self.collision_rects = [upper_collision_rect, bottom_collision_rect, left_collision_rect, right_collision_rect]

    def register_in_world(self, world):
        # for rect in self.collision_rects:
        #     rect.register_in_world(world)

        self.boundary = world.CreateStaticBody(position=self.position.tolist())
        self.boundary.CreateEdgeChain([(self.left, self.top), 
            (self.left, self.bottom),
            (self.right, self.bottom),
            (self.right, self.top),
            (self.left, self.top)])

    def draw(self, surface, camera):
        camera.draw_rect(surface, self.color, self)
        r, g, b = self.color
        for rect in self.collision_rects:

            camera.draw_rect(surface, (r / 2, g / 2, b / 2), rect)

        




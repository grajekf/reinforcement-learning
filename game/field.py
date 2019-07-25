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

    def handle_collison(self, ball, vel_multiplier = -1):
        for rect in self.collision_rects:
            rect.handle_collison(ball, vel_multiplier)
        # if ball.get_top() < self.top:
        #     ball.mul_y_vel(vel_multiplier)
        #     ball.set_top(self.top)

        # if ball.get_bottom() > self.bottom:
        #     ball.mul_y_vel(vel_multiplier)
        #     ball.set_bottom(self.bottom)

        # if ball.get_left() < self.left:
        #     if ball.get_bottom() > self.goal_width / 2.0 or ball.get_top() < -self.goal_width / 2.0:
        #         ball.mul_x_vel(vel_multiplier)
        #         ball.set_left(self.left)

        # if ball.get_right() > self.right :
        #     testA = ball.get_bottom() > self.goal_width / 2.0
        #     testB = ball.get_top() < -self.goal_width / 2.0
        #     if ball.get_bottom() > self.goal_width / 2.0 or ball.get_top() < -self.goal_width / 2.0:
        #         ball.mul_x_vel(vel_multiplier)
        #         ball.set_right(self.right)   

    def draw(self, surface, camera):
        camera.draw_rect(surface, self.color, self)
        r, g, b = self.color
        for rect in self.collision_rects:

            camera.draw_rect(surface, (r / 2, g / 2, b / 2), rect)

        




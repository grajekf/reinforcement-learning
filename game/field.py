import numpy as np

from rectangle import Rectangle

class Field(Rectangle):

    def __init__(self, width, length, color, goal_width):
        super().__init__([0, 0], width, length)
        self.color = color
        self.goal_width = goal_width


    def handle_collison(self, ball, vel_multiplier = -1):
        if ball.get_top() < self.top:
            ball.mul_y_vel(vel_multiplier)
            ball.set_top(self.top)

        if ball.get_bottom() > self.bottom:
            ball.mul_y_vel(vel_multiplier)
            ball.set_bottom(self.bottom)

        if ball.get_left() < self.left:
            if ball.get_bottom() > self.goal_width / 2.0 or ball.get_top() < -self.goal_width / 2.0:
                ball.mul_x_vel(vel_multiplier)
                ball.set_left(self.left)

        if ball.get_right() > self.right :
            testA = ball.get_bottom() > self.goal_width / 2.0
            testB = ball.get_top() < -self.goal_width / 2.0
            if ball.get_bottom() > self.goal_width / 2.0 or ball.get_top() < -self.goal_width / 2.0:
                ball.mul_x_vel(vel_multiplier)
                ball.set_right(self.right)   

    def draw(self, surface, camera):
        camera.draw_rect(surface, self.color, self)

        




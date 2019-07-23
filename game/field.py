import numpy as np

class Field:

    def __init__(self, left_goal, right_goal, width, length, outer_width, outer_length):
        self.left_goal = left_goal
        self.right_goal = right_goal

        self.width = width
        self.length = length

        self.left = -length / 2.0
        self.right = length / 2.0
        self.top = -width / 2.0
        self.bottom = width / 2.0

        self.outer_width = outer_width
        self.outer_length = outer_length

        self.position = np.array([0.0, 0.0])


    def handle_ball_collison(self, ball):
        if ball.get_top() < self.top:
            ball.mul_y_vel(-1)
            ball.set_top(self.top)

        if ball.get_bottom() > self.bottom:
            ball.mul_y_vel(-1)
            ball.set_bottom(self.bottom)

        if(ball.get_left() < self.left):
            ball.mul_x_vel(-1)
            ball.set_left(self.left)

        if(ball.get_right() > self.right):
            ball.mul_x_vel(-1)
            ball.set_right(self.right)

    def draw(self, surface, camera):
        camera.draw_rect(surface, (96, 128, 56), self)

        




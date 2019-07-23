import numpy as np

class Field:

    def __init__(self, width, length, color):
        self.width = width
        self.length = length

        self.left = -length / 2.0
        self.right = length / 2.0
        self.top = -width / 2.0
        self.bottom = width / 2.0

        self.color = color

        self.position = np.array([0.0, 0.0])


    def handle_collison(self, ball, vel_multiplier = -1):
        if ball.get_top() < self.top:
            ball.mul_y_vel(vel_multiplier)
            ball.set_top(self.top)

        if ball.get_bottom() > self.bottom:
            ball.mul_y_vel(vel_multiplier)
            ball.set_bottom(self.bottom)

        if(ball.get_left() < self.left):
            ball.mul_x_vel(vel_multiplier)
            ball.set_left(self.left)

        if(ball.get_right() > self.right):
            ball.mul_x_vel(vel_multiplier)
            ball.set_right(self.right)   

    def draw(self, surface, camera):
        camera.draw_rect(surface, self.color, self)

        




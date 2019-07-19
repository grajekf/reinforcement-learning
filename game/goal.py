
class Goal:

    def __init__(self, position, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.position = position

        self.left = self.position[0] - self.depth / 2.0
        self.right = self.position[0] + self.depth / 2.0
        self.top = self.position[1] - self.width / 2.0
        self.bottom = self.position[1] + self.width / 2.0


    def is_ball_inside(self, ball):
        return ball.get_left() > self.left and ball.get_right() < self.right and ball.get_top() > self.top and ball.get_bottom() < self.bottom

    # def intersects_with_circle(self, circle):

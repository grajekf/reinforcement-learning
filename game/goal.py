from rectangle import Rectangle
class Goal(Rectangle):

    def __init__(self, position, width, depth):
        super().__init__(position, width, depth)
        self.goal_subscribers = []

    def draw(self, surface, camera):
        camera.draw_rect(surface, (225, 225, 225), self)

    def subscribe(self, handler):
        self.goal_subscribers.append(handler)

    def handle_collison(self, ball):
        if self.is_circle_inside(ball):
            for subscriber in self.goal_subscribers:
                subscriber(ball)

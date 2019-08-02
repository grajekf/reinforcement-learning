import numpy as np
from game.rectangle import Rectangle
class Goal(Rectangle):

    def __init__(self, position, width, depth):
        super().__init__(position, width, depth)
        self.goal_subscribers = []


    @classmethod
    def from_config(cls, config):
        field = config["field"]
        goal = config["goal"]
        goal_width = goal["width"]
        goal_depth = goal["depth"]
        position = np.array([-field["length"] / 2 - goal_depth / 2, 0])

        return Goal(position, goal_width, goal_depth)

    def draw(self, surface, camera):
        camera.draw_rect(surface, (225, 225, 225), self)

    def subscribe(self, handler):
        self.goal_subscribers.append(handler)

    def handle_collison(self, ball):
        if self.is_circle_inside(ball):
            for subscriber in self.goal_subscribers:
                subscriber(ball)

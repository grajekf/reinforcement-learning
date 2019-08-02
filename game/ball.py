import numpy as np

from game.circle import Circle

class Ball(Circle):

    def __init__(self, position, radius, weight):
        super().__init__(position, radius, weight)

    def draw(self, surface, camera):
        camera.draw_circle(surface, (255, 255, 255), self.position, self.radius)
        # camera.draw_circle(surface, (0, 0, 0), self.position, self.radius, 1)

    @classmethod
    def from_config(cls, config):
        radius = config["ball"]["radius"]
        weight = config["ball"]["weight"]

        return Ball([0, 0], radius, weight)
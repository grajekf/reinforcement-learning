import numpy as np

from entity import Entity

class Ball(Entity):

    def __init__(self, position, radius, weight):
        super().__init__(position, radius, weight)

    def draw(self, surface, camera):
        camera.draw_circle(surface, (255, 255, 255), self.position, self.radius)
        # camera.draw_circle(surface, (0, 0, 0), self.position, self.radius, 1)
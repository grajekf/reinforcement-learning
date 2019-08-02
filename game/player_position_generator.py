import numpy as np
import random

class RandomPlayerPositionGenerator:

    def __init__(self, seed = -1):
        self.seed = seed
        random.seed(self.seed)

    def get_position(self, field, player_radius):
        return np.array([random.uniform(-field.length / 2 + player_radius, 0), 
                random.uniform(-field.width / 2 + player_radius, field.width / 2 - player_radius)])
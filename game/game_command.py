import numpy as np

from game.game import Game

class GameCommand:

    def __init__(self, accel, kick):
        self.accel = accel
        self.kick = kick
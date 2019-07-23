
class Team:

    def __init__(self, players, color):
        self.players = players
        self.color = color
        self.score = 0
        
    def draw(self, surface, camera):
        for player in self.players:
            player.draw(surface, camera, self.color)
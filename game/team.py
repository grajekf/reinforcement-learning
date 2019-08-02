from game.player import Player
class Team:

    def __init__(self, players):
        self.players = players
        self.score = 0

    @classmethod
    def from_config(cls, config):
        return Team([Player.from_config(config) for i in range(config["team_size"])])
        
    def draw(self, surface, camera, color):
        for player in self.players:
            player.draw(surface, camera, color)
import numpy as np

from game.game import Game

class GameState:

    def __init__(self, first_team_players, second_team_players, ball):
        self.first_team_players = np.array(first_team_players)
        self.second_team_players = np.array(second_team_players)
        self.ball = np.array(ball)

    @classmethod
    def from_game(cls, game):
        first_team = []
        second_team = []
        ball = []

        for player in game.home_team.players:
            x, y = player.get_position()
            vx, vy = player.get_velocity()
            first_team.append([x, y, vx, vy])

        for player in game.away_team.players:
            x, y = player.get_position()
            vx, vy = player.get_velocity()
            second_team.append([x, y, vx, vy])

        ball = game.ball

        x, y = ball.get_position()
        vx, vy = ball.get_velocity()

        ball = [x, y, vx, vy]

        return GameState(first_team, second_team, ball)

    def get_complement(self):
        new_first_team = self.second_team_players * -1.0
        new_second_team = self.first_team_players * -1.0
        new_ball = self.ball * -1.0

        return GameState(new_first_team, new_second_team, new_ball)

        
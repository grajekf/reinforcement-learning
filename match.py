import pygame
import numpy as np

from game.game_state import GameState
from colors import *

class Match:

    def __init__(self, first_model, second_model, repeats, game, time_step):
        self.first_model = first_model
        self.second_model = second_model
        self.repeats = repeats
        self.game = game
        self.time_step = time_step

        self.final_scores = []

    def get_average_score(self):
        np.mean(map(self.final_scores, lambda score: score[0] - score[1]))

    def simulate(self, do_draw, **kwargs):

        self.game.init_physics()

        for i in range(self.repeats):
            clock = pygame.time.Clock()
            self.game.reset()
            self.game.init_physics()
            

            while not self.game.finished:
                first_team_state = GameState.from_game(self.game)
                second_team_state = first_team_state.get_complement()

                home_moves = self.first_model.get_next_moves(first_team_state)
                away_moves = self.second_model.get_next_moves(second_team_state)

                self.game.execute_commands(home_moves, away_moves)

                self.game.update(self.time_step)

                if do_draw:
                    surface = kwargs["surface"]
                    camera = kwargs["camera"]

                    surface.fill(BLACK)
                    self.game.draw(surface, camera)

                    fps = int(clock.get_fps())
                    font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
                    text_surface = font.render(f"FPS: {fps}",True, (255, 255, 255))
                    surface.blit(text_surface, (50, 5))

                    pygame.display.flip()

                clock.tick()
            
            self.final_scores.append((self.game.home_score, self.game.away_score))


    


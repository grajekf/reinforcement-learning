#!/usr/bin/env python3

import pygame
import numpy as np

import json
import random
import sys

from game.camera import Camera
from game.game import Game
from game.field import Field
from game.ball import Ball
from game.player import Player
from game.team import Team
from game.goal import Goal
from game.player_position_generator import RandomPlayerPositionGenerator

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PIXELS_PER_METER = 30
CAMERA_POS = (0, 0)

FIELD_LENGTH = 35
FIELD_WIDTH = 20
FIELD_COLOR =  (96, 128, 56)

OUTER_FIELD_LENGTH = FIELD_LENGTH + 5
OUTER_FIELD_WIDTH = FIELD_WIDTH + 5
OUTER_FIELD_COLOR = (82, 90, 96)

BALL_POS = (0, 0)
BALL_RADIUS = 0.2
BALL_WEIGHT = 0.5

TEAM_SIZE = 5
PLAYER_RADIUS = 0.4
KICK_RADIUS = 1.0
PLAYER_WEIGHT = 70
PLAYER_MAX_VELOCITY = 9
PLAYER_MAX_RUN_FORCE = 200
KICK_MAX_MOMENTUM = 30
KICK_WAIT_TIME = 0.5

GOAL_WIDTH = 4
GOAL_DEPTH = 1.5

HOME_TEAM_COLOR = (51, 102, 153)
AWAY_TEAM_COLOR = (204, 51, 51)

FRICTION = 0.6

def load_config(path):
    with open(path, 'r') as json_file:
        return json.load(json_file)


def main():
    size = (1400, 800)
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Test")

    done = False

    clock = pygame.time.Clock()

    camera = Camera(CAMERA_POS, PIXELS_PER_METER, size)
    # field = Field(FIELD_WIDTH, FIELD_LENGTH, GOAL_WIDTH, GOAL_DEPTH)
    # outer_field = Field(OUTER_FIELD_WIDTH, OUTER_FIELD_LENGTH, 0, 0)
    # ball = Ball(BALL_POS, BALL_RADIUS, BALL_WEIGHT)
    # home_goal = Goal([-FIELD_LENGTH/2 - GOAL_DEPTH/2, 0], GOAL_WIDTH, GOAL_DEPTH)
    # away_goal = Goal([FIELD_LENGTH/2 + GOAL_DEPTH/2, 0], GOAL_WIDTH, GOAL_DEPTH)
    # home_team_players = []
    # away_team_players = []

    # # random.seed(42)

    # for i in range(TEAM_SIZE):
    #     home_team_players.append(Player(
    #         [0, 0], 
    #         PLAYER_RADIUS, 
    #         PLAYER_WEIGHT, 
    #         KICK_RADIUS, 
    #         KICK_MAX_MOMENTUM,
    #         KICK_WAIT_TIME, 
    #         PLAYER_MAX_VELOCITY))
    #     away_team_players.append(Player(
    #         [0, 0], 
    #         PLAYER_RADIUS, 
    #         PLAYER_WEIGHT, 
    #         KICK_RADIUS,
    #         KICK_MAX_MOMENTUM,
    #         KICK_WAIT_TIME, 
    #         PLAYER_MAX_VELOCITY))

    # home_team = Team(home_team_players)
    # away_team = Team(away_team_players)

    # # ball.velocity = away_team_players[0].position
    # game = Game(ball, home_team, away_team, home_goal, away_goal, field, 90, FRICTION)

    if len(sys.argv) < 2:
        config_path = "configs/game/default.json"
    else:
        config_path = sys.argv[1]
    config = load_config(config_path)
    game = Game.from_config(config, RandomPlayerPositionGenerator())
    
    game.reset()
    game.init_physics()

    # ball.add_velocity(np.array([10, 8]))

    while not done and not game.finished:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    
        # Game logic should go here
        game.update(1 / 30.0)
    

        screen.fill(BLACK)
    
        # Drawing code should go here
        game.draw(screen, camera)

        fps = int(clock.get_fps())
        font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
        text_surface = font.render(f"FPS: {fps}",True, (255, 255, 255))
        screen.blit(text_surface, (50, 5))
    
        pygame.display.flip()

        clock.tick()

    pygame.quit()


if __name__ == "__main__":
    main()
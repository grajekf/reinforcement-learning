#!/usr/bin/env python3

import pygame
import numpy as np

import random

from camera import Camera
from game import Game
from field import Field
from ball import Ball
from player import Player
from team import Team

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PIXELS_PER_METER = 35
CAMERA_POS = (0, 0)

FIELD_LENGTH = 35
FIELD_WIDTH = 20

BALL_POS = (0, 0)
BALL_RADIUS = 0.2
BALL_WEIGHT = 0.5

TEAM_SIZE = 5
PLAYER_RADIUS = 0.4
KICK_RADIUS = 0.6
PLAYER_HEIGHT = 1.8
PLAYER_WEIGHT = 70

HOME_TEAM_COLOR = (51, 102, 153)
AWAY_TEAM_COLOR = (204, 51, 51)




def main():
    size = (1400, 800)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Test")

    done = False

    clock = pygame.time.Clock()

    camera = Camera(CAMERA_POS, PIXELS_PER_METER, size)
    field = Field([], [], FIELD_WIDTH, FIELD_LENGTH, 0, 0)
    ball = Ball(BALL_POS, BALL_RADIUS, BALL_WEIGHT)
    home_team_players = []
    away_team_players = []

    # random.seed(42)

    for i in range(TEAM_SIZE):
        home_team_players.append(Player([random.uniform(-FIELD_LENGTH/2, 0), random.uniform(-FIELD_WIDTH/2, FIELD_WIDTH/2)], PLAYER_RADIUS, KICK_RADIUS, PLAYER_HEIGHT, PLAYER_WEIGHT))
        away_team_players.append(Player([random.uniform(0, FIELD_LENGTH/2), random.uniform(-FIELD_WIDTH/2, FIELD_WIDTH/2)], PLAYER_RADIUS, KICK_RADIUS, PLAYER_HEIGHT, PLAYER_WEIGHT))

    home_team = Team(home_team_players, HOME_TEAM_COLOR)
    away_team = Team(away_team_players, AWAY_TEAM_COLOR)

    # ball.velocity = away_team_players[0].position
    ball.velocity = np.array([50, 12])
    game = Game(ball, home_team, away_team, field, 90, 0.3, 9.81)

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    
        # Game logic should go here
        game.update(1 / 120.0)
    

        screen.fill(BLACK)
    
        # Drawing code should go here
        game.draw(screen, camera)
    
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
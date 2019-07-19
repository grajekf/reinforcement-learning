#!/usr/bin/env python3

import pygame
import numpy as np

from camera import Camera
from game import Game
from field import Field
from ball import Ball

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PIXELS_PER_METER = 15
CAMERA_POS = (0, 0)

FIELD_LENGTH = 80
FIELD_WIDTH = 50

BALL_POS = (0, 0)
BALL_RADIUS = 0.2
BALL_WEIGHT = 0.5




def main():
    size = (1400, 800)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Test")

    done = False

    clock = pygame.time.Clock()

    camera = Camera(CAMERA_POS, PIXELS_PER_METER, size)
    field = Field([], [], FIELD_WIDTH, FIELD_LENGTH, 0, 0)
    ball = Ball(BALL_POS, BALL_RADIUS, BALL_WEIGHT)
    ball.velocity = np.array([2, 6])
    game = Game(ball, [], [], field, 90, 0.001, 9.81)

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    
        # Game logic should go here
        game.update(1 / 60.0)
    

        screen.fill(BLACK)
    
        # Drawing code should go here
        game.draw(screen, camera)
    
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
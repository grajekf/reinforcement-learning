#!/usr/bin/env python3

import argparse
import json

import pygame
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from game.player_position_generator import RandomPlayerPositionGenerator
from game.game import Game
from game.camera import Camera

from neural_net import FeedforwardModel
from match import Match


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--game_config", required=True)
    parser.add_argument("--train", action="store_true")

    args =  parser.parse_args()
    return args.game_config, args.train

def load_config(path):
    with open(path, 'r') as json_file:
        return json.load(json_file)

def main():
    game_config_path, do_train = args()

    game_config = load_config(game_config_path)
    player_position_generator = RandomPlayerPositionGenerator()
    game = Game.from_config(game_config, player_position_generator)

    first_player = FeedforwardModel.create([50, 50, 50, 50], 'tanh', game_config["team_size"])
    second_player = FeedforwardModel.create([50, 50, 50, 50], 'tanh', game_config["team_size"])

    repeats = 1
    time_step = 1/30.0

    match = Match(first_player, second_player, repeats, game, time_step)

#     size = (1400, 800)
#     pygame.init()
#     screen = pygame.display.set_mode(size)
#     pygame.display.set_caption("Test")
#     camera = Camera([0, 0], 35, size)

#     match.simulate(True, camera=camera, surface=screen)
    match.simulate(False)


if __name__ == "__main__":
    main()
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

from geneticalgorithm.populationgenerator import UniformFloatPopulationGenerator
from geneticalgorithm.model import Model
from geneticalgorithm.elitism import ElitismLayer
from geneticalgorithm.crossover import CrossoverLayer
from geneticalgorithm.mutation import MutationLayer
from geneticalgorithm.crossoverfunctions import OnePointCrossover
from geneticalgorithm.mutationfunctions import GaussianMutation
from geneticalgorithm.selectionfunctions import TournamentSelection


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--game_config", required=True)
    parser.add_argument("-e", "--evol_config", required=True)
    parser.add_argument("-n", "--nn_config", required=True)
    parser.add_argument("--train", action="store_true")

    args =  parser.parse_args()
    return args.game_config, args.evol_config, args.nn_config, args.train

def load_config(path):
    with open(path, 'r') as json_file:
        return json.load(json_file)

def create_genetic_algorithm(config):
    elitism = ElitismLayer(None, config["elitism"]) if config["elitism"] > 0 else None
    crossover = CrossoverLayer(None, 
        OnePointCrossover(), 
        TournamentSelection(config["tournament_size"]),
        config["population_size"] - config["elitism"])

    mutation = MutationLayer(crossover, GaussianMutation(config["mutation_rate"], config["mutation_variance"]))

    return Model(mutation if elitism is None else [mutation, elitism])

def create_initial_models(config, initial_population, team_size):
    models = [FeedforwardModel.create(config["layer_sizes"], config["activation"], team_size)]
    for model, weights in zip(models, initial_population):
        model.set_weights(weights)
    return models

def main():
    game_config_path, evol_config_path, nn_config_path, do_train = args()

    game_config = load_config(game_config_path)
    evol_config = load_config(evol_config_path)
    nn_config = load_config(nn_config_path)

    player_position_generator = RandomPlayerPositionGenerator()
    game = Game.from_config(game_config, player_position_generator)

    example_model = FeedforwardModel.create(nn_config["layer_sizes"], nn_config["activation"], game_config["team_size"])
    #Too lazy to do the math manually
    chromosome_length = example_model.get_weights().size

    initial_population = UniformFloatPopulationGenerator(-1, 1, chromosome_length).generate(game_config["team_size"])
    models = create_initial_models(nn_config, initial_population, game_config["team_size"])

    # first_player = FeedforwardModel.create([50, 50, 50, 50], 'tanh', game_config["team_size"])
    # second_player = FeedforwardModel.create([50, 50, 50, 50], 'tanh', game_config["team_size"])

    # test = first_player.get_weights()
    # print(test)
    # first_player.set_weights(test)

    # repeats = 1
    # time_step = 1/30.0

    # match = Match(first_player, second_player, repeats, game, time_step)

#     size = (1400, 800)
#     pygame.init()
#     screen = pygame.display.set_mode(size)
#     pygame.display.set_caption("Test")
#     camera = Camera([0, 0], 35, size)

#     match.simulate(True, camera=camera, surface=screen)
#     match.simulate(False)


if __name__ == "__main__":
    main()
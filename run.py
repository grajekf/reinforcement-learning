#!/usr/bin/env python3

import argparse
import json
import uuid
from collections import defaultdict

import pygame
import os
import numpy as np
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

def create_genetic_algorithm(config, fitness_func):
    elitism = ElitismLayer(None, config["elitism"]) if config["elitism"] > 0 else None
    crossover = CrossoverLayer(None, 
        OnePointCrossover(), 
        TournamentSelection(config["tournament_size"]),
        config["population_size"] - config["elitism"])

    mutation = MutationLayer(crossover, GaussianMutation(config["mutation_rate"], config["mutation_variance"]))

    return Model(mutation if elitism is None else [mutation, elitism], fitness_func)


def random_matches_fitness_generator(match_count, models, game, time_step, surface, camera):

    def inner(population):
        for model, weights in zip(models, population):
            model.set_weights(weights)

        results = defaultdict(list)

        did_visualize = False

        for i, model in enumerate(models):
            possible_opponents = models[:i] + models[i + 1:]
            oponents = np.random.choice(possible_opponents, match_count, replace=False)

            for oponent in oponents:
                match = Match(model, oponent, 1, game, time_step)
                if not did_visualize:
                    match.simulate(True, camera=camera, surface=surface)
                    did_visualize = True
                else:
                    match.simulate(False)

                score = match.get_average_score()

                print("FInal score is: ")
                print(score)
                results[model.id].append(score)
                results[oponent.id].append(-score)

        return [np.mean(scores) for scores in results.values()]

    return inner

def generation_count_stopping_criterion(max_generations):
    def inner(population, fitness, **kwargs):
        return kwargs["generation"] >= max_generations

    return inner

def create_initial_models(config, initial_population, team_size):
    models = [FeedforwardModel.create(str(uuid.uuid4()), config["layer_sizes"], config["activation"], team_size) for i in range(len(initial_population))]
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

    example_model = FeedforwardModel.create("test", nn_config["layer_sizes"], nn_config["activation"], game_config["team_size"])
    #Too lazy to do the math manually
    chromosome_length = example_model.get_weights().size

    initial_population = UniformFloatPopulationGenerator(-1, 1, chromosome_length).generate(evol_config["population_size"])
    models = create_initial_models(nn_config, initial_population, game_config["team_size"])

    size = (1400, 800)
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Test")
    camera = Camera([0, 0], 35, size)

    genetic_alg = create_genetic_algorithm(evol_config, random_matches_fitness_generator(3, models, game, 1/30.0, screen, camera))

    population, fitness = genetic_alg.run(initial_population, generation_count_stopping_criterion(10))

    best_model =  max(list(zip(population, fitness)), key=lambda p: p[1])[0]

    best_model.save(f"{best_model.id}.h5")
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
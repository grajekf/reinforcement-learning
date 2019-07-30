#!/usr/bin/env python3

import argparse
import json


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--game_config", required=True)
    parser.add_argument("--train", action="store_true")

    args =  parser.parse_args()
    return args.game_config, args.train


def main():
    game_config_path, do_train = args()

    with open(game_config_path) as json_file:
        game_config = json.load(json_file)

    print(game_config)



if __name__ == "__main__":
    main()
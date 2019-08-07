from keras import Input, Model
from keras.layers import Dense
from keras.models import save_model, load_model

import numpy as np

from game.game_command import GameCommand


class FeedforwardModel:

    def __init__(self, inner_model):
        self.model = inner_model

    @classmethod
    def create(cls, layer_sizes, activation, player_count):
        inputs = Input(shape=(8 * player_count + 4, ))

        layer = inputs

        for size in layer_sizes:
            layer = Dense(size, activation=activation)(layer)

        outputs = Dense(8 * player_count, activation=activation)(layer)

        model = Model(inputs=inputs, outputs=outputs)
        return FeedforwardModel(model)

    def save(self, path):
        save_model(self.model, path)

    @classmethod
    def load(cls, path):
        inner_model = load_model(path)
        return FeedforwardModel(inner_model)


    def get_next_moves(self, game_state):
        inputs = []

        for player in game_state.first_team_players:
            inputs.extend(player)

        for player in game_state.second_team_players:
            inputs.extend(player)

        ball = game_state.ball
        inputs.extend(ball)

        inputs = np.array(inputs)

        outputs = self.model.predict(np.array([inputs]))[0]

        return self.get_commands(outputs)

    def get_commands(self, outputs):
        commands = []
        for i in range(0, len(outputs), 4):
            accel = np.array([outputs[i], outputs[i+1]])
            kick = 0.0 if outputs[i+2] < 0 else (outputs[i + 3] + 1.0) / 2.0
            commands.append(GameCommand(accel, kick))

        return commands

    def get_weights(self):
        weights = np.array([])
        for layer_weights in self.model.get_weights():
            weights = np.hstack((weights, layer_weights.flatten().flatten()))
        return weights

    def set_weights(self, weights):
        weights_cutoff_indices = np.cumsum([layer_weights.size for layer_weights in self.model.get_weights()])
        splitted_weights = np.split(weights, weights_cutoff_indices)
        reshaped_weights = [new_weights.reshape(old_weights.shape) for new_weights, old_weights in zip(splitted_weights[:-1], self.model.get_weights())]
        self.model.set_weights(reshaped_weights)




        

        


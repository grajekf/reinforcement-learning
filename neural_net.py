from keras import Input, Model
from keras.layers import Dense

import numpy as np


class FeedforwardModel:

    def __init__(self, layer_sizes, activation, player_count):
        inputs = Input(shape=(8 * player_count + 4, ))

        layer = inputs

        for size in layer_sizes:
            layer = Dense(size, activation=activation)(layer)

        outputs = Dense(8 * player_count, activation=activation)(layer)

        self.model = Model(inputs=inputs, outputs=outputs)
        self.player_count = player_count


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

        print(outputs)




        

        


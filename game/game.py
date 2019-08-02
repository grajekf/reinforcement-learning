import numpy as np
import random

from Box2D import b2World
import pygame

from game.ball import Ball
from game.goal import Goal
from game.field import Field
from game.team import Team


class Game:

    def __init__(self, ball, home_team, away_team, home_goal, away_goal, field, duration, friction, player_position_generator):
        self.ball = ball
        self.home_team = home_team
        self.away_team = away_team
        self.home_goal = home_goal
        self.home_goal.subscribe(self.notify_home_goal)
        self.away_goal = away_goal
        self.away_goal.subscribe(self.notify_away_goal)
        self.field = field
        self.duration = duration
        self.finished = False
        self.current_time = 0.0
        self.friction = friction
        self.home_score = 0
        self.away_score = 0
        self.player_position_generator = player_position_generator

    @classmethod
    def from_config(cls, config, player_position_generator):
        ball = Ball.from_config(config)
        home_team = Team.from_config(config)
        away_team = Team.from_config(config)
        home_goal = Goal.from_config(config)
        away_goal = Goal.from_config(config)
        away_goal.position = -away_goal.position
        field = Field.from_config(config)
        duration = config["duration"]
        friction = config["friction"]

        return Game(ball, home_team, away_team, home_goal, away_goal, field, duration, friction, player_position_generator)


    # @classmethod
    # def team_from_config(cls, config):


    def init_physics(self):
        self.world = b2World(gravity=(0, 0))
        self.ball.register_in_world(self.world, self.friction)

        for player in self.home_team.players:
            player.register_in_world(self.world, self.friction)

        for player in self.away_team.players:
            player.register_in_world(self.world, self.friction)

        self.field.register_in_world(self.world)


    def update(self, passed_time):
        self.world.Step(passed_time, 6, 2)
        self.ball.update(passed_time)

        for player in self.home_team.players:
            player.update(passed_time)
            # player.do_kick(self.ball, 1.0)

        for player in self.away_team.players:
            player.update(passed_time) 
            # player.do_kick(self.ball, 1.0)

        self.home_goal.handle_collison(self.ball)
        self.away_goal.handle_collison(self.ball)

        self.current_time += passed_time
        if self.current_time >= self.duration:
            self.finished = True

    def get_time_minutes_and_seconds(self):
        minutes = int(self.current_time // 60)
        seconds = int(self.current_time % 60)

        return (minutes, seconds)

    def draw(self, surface, camera):
        self.field.draw(surface, camera, (96, 128, 56))
        self.home_goal.draw(surface, camera)
        self.away_goal.draw(surface, camera)
        self.ball.draw(surface, camera)
        self.home_team.draw(surface, camera, (51, 102, 153))
        self.away_team.draw(surface, camera, (204, 51, 51))

        #draw time and score
        font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
        minutes, seconds = self.get_time_minutes_and_seconds()
        text_surface = font.render(f"Time: {minutes:02d}:{seconds:02d}",True, (255, 255, 255))
        screen_width = surface.get_width()
        surface.blit(text_surface, (screen_width - 200, 5))

    def notify_home_goal(self, ball):
        print("Goal for the away team!")
        self.away_score += 1
        print(f"Score: {self.home_score} - {self.away_score}")
        self.reset_ball()
        self.reset_players()

    def notify_away_goal(self, ball):
        print("Goal for the home team!")
        self.home_score += 1
        print(f"Score: {self.home_score} - {self.away_score}")
        self.reset_ball()
        self.reset_players()

    def reset_ball(self):
        self.ball.set_position([0, 0])
        self.ball.set_velocity(np.array([0, 0]))
        self.ball.set_velocity(np.random.uniform(-10, 10, 2))

    def reset_players(self):
        for player in self.home_team.players:
            player.set_position(self.player_position_generator.get_position(self.field, player.radius))

        for player in self.away_team.players:
            player.set_position(-self.player_position_generator.get_position(self.field, player.radius))
        
    def reset(self):
        self.finished = False
        self.home_score = 0
        self.away_score = 0

        self.current_time = 0

        self.reset_ball()
        self.reset_players()

        del self.world


        
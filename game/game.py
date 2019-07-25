import numpy as np
from Box2D import b2World

class Game:

    def __init__(self, ball, home_team, away_team, home_goal, away_goal, field, outer_field, duration, friction):
        self.ball = ball
        self.home_team = home_team
        self.away_team = away_team
        self.home_goal = home_goal
        self.home_goal.subscribe(self.notify_home_goal)
        self.away_goal = away_goal
        self.away_goal.subscribe(self.notify_away_goal)
        self.field = field
        self.outer_field = outer_field
        self.duration = duration
        self.current_time = 0.0
        self.friction = friction
        self.home_score = 0
        self.away_score = 0
        self.world = b2World(gravity=(0, 0))

    def init_physics(self):
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

        for player in self.away_team.players:
            player.update(passed_time) 

        self.home_goal.handle_collison(self.ball)
        self.away_goal.handle_collison(self.ball)


    def draw(self, surface, camera):
        self.outer_field.draw(surface, camera)
        self.field.draw(surface, camera)
        self.home_goal.draw(surface, camera)
        self.away_goal.draw(surface, camera)
        self.ball.draw(surface, camera)
        self.home_team.draw(surface, camera)
        self.away_team.draw(surface, camera)

    def notify_home_goal(self, ball):
        print("Goal for the away team!")
        self.away_score += 1
        print(f"Score: {self.home_score} - {self.away_score}")
        self.reset_ball()

    def notify_away_goal(self, ball):
        print("Goal for the home team!")
        self.home_score += 1
        print(f"Score: {self.home_score} - {self.away_score}")
        self.reset_ball()

    def reset_ball(self):
        self.ball.set_position([0, 0])
        self.ball.set_velocity(np.random.uniform(-30, 30, 2))
        
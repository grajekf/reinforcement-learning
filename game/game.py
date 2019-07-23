import numpy as np

class Game:

    def __init__(self, ball, home_team, away_team, home_goal, away_goal, field, outer_field, duration, friction, gravity):
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
        self.gravity = gravity
        self.home_score = 0
        self.away_score = 0


    def update(self, passed_time):
        self.ball.update(passed_time, self.friction)

        for player in self.home_team.players:
            player.update(passed_time, self.friction)

        for player in self.away_team.players:
            player.update(passed_time, self.friction) 


        self.home_goal.handle_collison(self.ball)
        self.away_goal.handle_collison(self.ball)

        self.field.handle_collison(self.ball)
        
        for player in self.home_team.players:
            player.handle_ball_collision(self.ball)
            self.outer_field.handle_collison(player, 1.0)

        for player in self.away_team.players:
            player.handle_ball_collision(self.ball)
            self.outer_field.handle_collison(player, 1.0)

    def draw(self, surface, camera):
        self.outer_field.draw(surface, camera)
        self.field.draw(surface, camera)
        self.home_goal.draw(surface, camera)
        self.away_goal.draw(surface, camera)
        self.ball.draw(surface, camera)
        self.home_team.draw(surface, camera)
        self.away_team.draw(surface, camera)

    def notify_home_goal(self, ball):
        print("Goal for the home team!")
        self.home_score += 1
        print(f"Score: {self.home_score} - {self.away_score}")
        self.reset_ball()

    def notify_away_goal(self, ball):
        print("Goal for the away team!")
        self.away_score += 1
        print(f"Score: {self.home_score} - {self.away_score}")
        self.reset_ball()

    def reset_ball(self):
        self.ball.position = np.array([0, 0])
        self.ball.velocity = np.random.uniform(-30, 30, 2)
        
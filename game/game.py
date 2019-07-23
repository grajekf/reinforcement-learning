
class Game:

    def __init__(self, ball, home_team, away_team, field, outer_field, duration, friction, gravity):
        self.ball = ball
        self.home_team = home_team
        self.away_team = away_team
        self.field = field
        self.outer_field = outer_field
        self.duration = duration
        self.current_time = 0.0
        self.friction = friction
        self.gravity = gravity


    def update(self, passed_time):
        self.update_velocity(self.ball, passed_time)
        self.update_position(self.ball, passed_time)

        for player in self.home_team.players:
            self.update_position(player, passed_time)

        for player in self.away_team.players:
            self.update_position(player, passed_time)   

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
        self.ball.draw(surface, camera)
        self.home_team.draw(surface, camera)
        self.away_team.draw(surface, camera)
        

    def update_velocity(self, entity, passed_time):
        entity.velocity = entity.velocity * (1 - self.friction * passed_time)

    def update_position(self, entity, passed_time):
        entity.position = entity.position + entity.velocity * passed_time
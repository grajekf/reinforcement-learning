
import math
import numpy as np
from Box2D import b2FixtureDef, b2CircleShape, b2Transform

import game.physics

class Circle:

    def __init__(self, position, radius, weight, movable = True):
        self.position = np.array(position)
        self.velocity = np.array([0, 0])
        self.radius = radius
        self.weight = weight
        self.density = weight / (np.pi * radius**2)
        self.movable = movable

    def register_in_world(self, world, friction):
        if self.movable:
            self.body = world.CreateDynamicBody(
                fixtures=b2FixtureDef(
                    shape=b2CircleShape(radius=self.radius),
                    density=self.density, restitution=1.0, friction=0.0),
                bullet=True,
                position=self.position.tolist(),
                fixedRotation=True,
                angularDamping=5,
                linearDamping=friction)

            self.set_velocity(self.velocity)
        else:
            self.body = world.CreateStaticBody(position=self.position.tolist(), shapes=b2CircleShape(radius=self.radius))

    def update(self, passedTime):
        self.position = np.array(self.body.position)

    def apply_force(self, force):
        self.body.ApplyForce(force.tolist(), self.body.worldCenter, True)

    def add_velocity(self, velocity):
        self.body.ApplyLinearImpulse(velocity.tolist(), self.body.worldCenter, True)
        self.velocity = np.array(self.body.linearVelocity)

    def set_velocity(self, velocity):
        self.body.linearVelocity = velocity.tolist()
        self.velocity = velocity

    def set_position(self, position):
        self.position = np.array(position)
        self.body.transform = [self.position.tolist(), 0]

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.body.linearVelocity

    def get_left(self):
        return self.position[0] - self.radius

    def get_right(self):
        return self.position[0] + self.radius   

    def get_top(self):
        return self.position[1] - self.radius

    def get_bottom(self):
        return self.position[1] + self.radius   


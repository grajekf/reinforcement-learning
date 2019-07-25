
import math
import numpy as np
from Box2D import b2FixtureDef, b2CircleShape

import physics

class Entity:

    def __init__(self, position, radius, weight, movable = True):
        self.position = np.array(position)
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
                angularDamping=5)
        else:
            self.body = world.CreateStaticBody(position=self.position.tolist(), shapes=b2CircleShape(radius=self.radius))

    def update(self, passedTime):
        self.position = np.array(self.body.position)

    def set_velocity(self, velocity):
        self.body.ApplyLinearImpulse(velocity.tolist(), self.body.worldCenter, True)


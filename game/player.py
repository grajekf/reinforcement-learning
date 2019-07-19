
class Player:

    def __init__(self, position, radius, height):
        self.position = np.array(position)
        self.velocity = np.array([0.0, 0.0])
        self.radius = radius
        self.height = height
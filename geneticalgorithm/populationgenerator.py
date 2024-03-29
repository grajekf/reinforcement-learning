from abc import ABC
import numpy as np

class PopulationGenerator(ABC):
    def generate(self, size):
        pass

class UniformClippedPopulationGenerator(PopulationGenerator):
    def __init__(self, original, max_change, min_value, max_value):
        self.original = original
        self.max_change = max_change
        self.min_value = min_value
        self.max_value = max_value
    def generate(self, size):
        return [np.clip(self.original + np.random.randint(-self.max_change, self.max_change, size=self.original.shape), self.min_value, self.max_value)
            for i in range(size)]


class UniformFloatPopulationGenerator(PopulationGenerator):
    def __init__(self, min_value, max_value, chromosome_length):
        self.min_value = min_value
        self.max_value = max_value
        self.chromosome_length = chromosome_length

    def generate(self, size):
        return [np.random.uniform(self.min_value, self.max_value, self.chromosome_length) for i in range(size)]

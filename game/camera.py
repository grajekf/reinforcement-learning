import pygame
import numpy as np

class Camera:

    def __init__(self, position, pixels_per_meter, screen_size):
        self.position = np.array(position)
        self.pixels_per_meter = pixels_per_meter
        self.screen_size = np.array(screen_size)

    def dimension_to_camera_space(self, value):
        return value * self.pixels_per_meter

    def position_to_camera_space(self, position):
        return position * self.pixels_per_meter - self.position

    def camera_space_to_screen_space(self, position):
        return position + self.screen_size / 2.0

    def position_to_screen_space(self, position):
        return self.camera_space_to_screen_space(self.position_to_camera_space(position))

    def draw_rect(self, surface, color, rect, thickness = 0):
        rect_left_upper = np.array([rect.left, rect.top])
        x, y = self.position_to_screen_space(rect_left_upper)

        width = self.dimension_to_camera_space(rect.width)
        length = self.dimension_to_camera_space(rect.length)

        pygame.draw.rect(surface, color, (x, y, length, width), thickness)


    def draw_circle(self, surface, color, position, radius, thickness = 0):
        x, y = self.position_to_screen_space(position)
        radius = int(self.dimension_to_camera_space(radius))

        # print(position)
        # print(radius)
        # print(color)
        # print(thickness)
        pygame.draw.circle(surface, color, (int(x), int(y)), radius, thickness)

from enum import IntEnum

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *


class _CubeletColour(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 4
    ORANGE = 8
    YELLOW = 16
    WHITE = 32


class _Cubelet(object):
    __cube_size = -1

    __vertex_buffer = [np.array([-1, 1, -1]), np.array([1, 1, -1]),
                       np.array([-1, -1, -1]), np.array([1, -1, -1]),
                       np.array([-1, 1, 1]), np.array([1, 1, 1]),
                       np.array([-1, -1, 1]), np.array([1, -1, 1])]

    __index_buffer = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
                      (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]

    def __init__(self, x: int, y: int, z: int):
        if self.__cube_size == -1:
            raise ValueError("Cube size must be set before creating cubelets")

        self.colour = 0
        self._pos_offset = np.array([x, y, z]) * 2 - (self.__cube_size - 1)

    @classmethod
    def set_cube_size(cls, cube_size):
        cls.__cube_size = cube_size

    def add_colour(self, colour: _CubeletColour):
        self.colour |= int(colour)

    def is_valid(self):
        return self.colour != 0

    def draw(self):
        if not self.is_valid():
            return

        for idx1, idx2 in self.__index_buffer:
            glVertex3f(*(self.__vertex_buffer[idx1] + self._pos_offset))
            glVertex3f(*(self.__vertex_buffer[idx2] + self._pos_offset))


class Cube(object):

    def __init__(self, size: int = 3):
        if size < 2:
            raise ValueError("Cube size cannot be less than 2")

        self.cube = np.zeros(shape=(size, size, size), dtype=np.int)
        self.cubelets = []

        _Cubelet.set_cube_size(size)

        for x in range(size):
            for y in range(size):
                for z in range(size):
                    cubelet = _Cubelet(x, y, z)

                    if (x == 0):
                        cubelet.add_colour(_CubeletColour.GREEN)
                    if (x == size - 1):
                        cubelet.add_colour(_CubeletColour.BLUE)
                    if (y == 0):
                        cubelet.add_colour(_CubeletColour.WHITE)
                    if (y == size - 1):
                        cubelet.add_colour(_CubeletColour.YELLOW)
                    if (z == 0):
                        cubelet.add_colour(_CubeletColour.RED)
                    if (z == size - 1):
                        cubelet.add_colour(_CubeletColour.ORANGE)

                    if cubelet.is_valid():
                        cubelet_idx = x + size * (y + size * z)
                        self.cube[z, y, x] = cubelet_idx
                        self.cubelets.append(cubelet)
                    else:
                        self.cube[z, y, x] = -1

    def randomize(self):
        pass

    def draw(self):
        glBegin(GL_LINES)
        for cubelet in self.cubelets:
            cubelet.draw()
        glEnd()


def main():
    display_size = (800, 600)
    fov = 45
    z_near = 0.1
    z_far = 50.0

    cube_size = 3

    pygame.init()
    pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL)

    gluPerspective(fov, display_size[0]/display_size[1], z_near, z_far)
    glTranslatef(0.0, 0.0, -cube_size * 5)
    glRotatef(0, 0, 0, 0)

    cube = Cube(cube_size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cube.draw()

        pygame.display.flip()
        pygame.time.wait(10)


main()

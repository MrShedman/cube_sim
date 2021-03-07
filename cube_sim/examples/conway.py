#!/usr/bin/env python

# THIS DOES NOT WORK YET!!!

from cube_sim.application import Application
from cube_sim.led_cube import LEDCube, Face

import glm

import numpy as np
import time


# def life_step(X):
#     """Game of life step using generator expressions"""
#     nbrs_count = sum(np.roll(np.roll(X, i, 0), j, 1)
#                      for i in (-1, 0, 1) for j in (-1, 0, 1)
#                      if (i != 0 or j != 0))
#     return (nbrs_count == 3) | (X & (nbrs_count == 2))


def life_step(X):
    """Game of life step using scipy tools"""
    from scipy.signal import convolve2d
    nbrs_count = convolve2d(X, np.ones((3, 3)), mode='same', boundary='fill') - X
    return (nbrs_count == 3) | (X & (nbrs_count == 2))


class Conway(Application):
    def __init__(self):
        super().__init__(1280, 720, 60, 64)

        unbounded = [[1, 1, 1, 0, 1],
             [1, 0, 0, 0, 0],
             [0, 0, 0, 1, 1],
             [0, 1, 1, 0, 1],
             [1, 0, 1, 0, 1]]
        self.X = np.zeros((64, 64)).astype(bool)
        self.X[15:20, 18:23] = unbounded

        dims = (self.led_cube.size * self.led_cube.size, 3)
        self.tempSide = np.zeros(dims).astype(np.float32)


    def update(self, dt):

        self.X = life_step(self.X)

        # print(self.X)

        self.tempSide[:,0] = self.X.astype(np.float32).flatten()

        self.led_cube.updateFace(Face.BACK, self.tempSide)
        # self.led_cube.updateFace(Face.RIGHT, colours)
        # self.led_cube.updateFace(Face.BOTTOM, colours)
        self.led_cube.update()

        # time.sleep(0.1)

        # self.led_cube.updateFaces(cube_faces)
        # self.led_cube.update()
        # print(time.time())
        # self.led_cube.rotateAngleAxis(dt * 0.1, glm.vec3(0, 0, 1))


if __name__ == "__main__":
    app = Conway()
    app.run()
    del app
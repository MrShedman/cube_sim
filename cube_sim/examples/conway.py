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
        self.conway_back = np.zeros((self.led_cube.size+2, self.led_cube.size+2)).astype(bool)
        self.conway_left = np.zeros_like(self.conway_back)
        self.conway_top = np.zeros_like(self.conway_back)
       

        dims = (self.led_cube.size, self.led_cube.size, 3) # 64x64 RGB
        self.displayed_back = np.zeros(dims).astype(np.float32)
        self.displayed_left = np.zeros_like(self.displayed_back)
        self.displayed_top = np.zeros_like(self.displayed_back)  

        # Starting Configuration
        offset = 40
        self.conway_back[15:20, 18+offset:23+offset] = unbounded
        self.conway_left[15:20, 18:23] = unbounded
        self.conway_top[15+20 : 20+20, 18:23] = unbounded

        self.led_cube.rotateAngleAxis(np.deg2rad(45), glm.vec3(0, 0, 1))
        self.led_cube.rotateAngleAxis(np.deg2rad(-10), glm.vec3(1, 0, 0))
        self.led_cube.rotateAngleAxis(np.deg2rad(-10), glm.vec3(0, 1, 0))

    def update(self, dt):

        self.conway_back = life_step(self.conway_back)
        self.conway_left = life_step(self.conway_left)
        self.conway_top = life_step(self.conway_top)

        # Back-Left Join
        self.conway_left[:,0] = self.conway_back[:,-2]
        self.conway_back[:,-1] = self.conway_left[:,1]

        # Top-Back Join
        self.conway_top[:,0] = self.conway_back[-2,:]
        self.conway_back[-1,:] = self.conway_top[:,1]

        # Top-Left Join
        self.conway_top[0,:] = self.conway_left[-2,:]
        self.conway_left[-1,:] = self.conway_top[1,:]


     


        # print(self.conway_back)

        # a = self.conway_back.astype(np.float32)


        # a[-2,:] = 1
        # a[1:64,1:64] = 1



        # print(a)
        # print(a[1:67,1:67])

        self.displayed_back[:,:,0] = self.conway_back.astype(np.float32)[1:65,1:65]
        self.displayed_left[:,:,1] = self.conway_left.astype(np.float32)[1:65,1:65]
        self.displayed_top[:,:,2] = self.conway_top.astype(np.float32)[1:65,1:65]

        # Back/Left Join
        # self.displayed_back[:,-1,1] = 1       
        # self.displayed_left[:,0,1] = 1

        # Top-back Join
        # self.displayed_top[:,0,:] = 1
        # self.displayed_back[-1,:,:] = 1

        # Top-left Join
        # self.displayed_top[0,:,:] = 1
        # self.displayed_left[-1,:,:] = 1


        self.led_cube.updateFace(Face.BACK, self.displayed_back)
        self.led_cube.updateFace(Face.LEFT, self.displayed_left)
        self.led_cube.updateFace(Face.TOP, self.displayed_top)
        self.led_cube.update()

        # time.sleep(0.1)

        # self.led_cube.updateFaces(cube_faces)
        # self.led_cube.update()
        # print(time.time())
        # self.led_cube.rotateAngleAxis(np.deg2rad(45), glm.vec3(0, 0, 1))


if __name__ == "__main__":
    app = Conway()
    app.run()
    del app
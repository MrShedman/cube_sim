#!/usr/bin/env python



from cube_sim.application import Application
from cube_sim.led_cube import LEDCube, Face

import glm

import numpy as np
import time


import copy

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

        # TODO: Put into list     
        self.conway_back = np.zeros((self.led_cube.size+2, self.led_cube.size+2)).astype(bool)
        self.conway_left = np.zeros_like(self.conway_back)
        self.conway_top = np.zeros_like(self.conway_back)
        self.conway_bottom = np.zeros_like(self.conway_back)
        self.conway_right = np.zeros_like(self.conway_back)
        self.conway_front = np.zeros_like(self.conway_back)

        # Todo Put into list
        dims = (self.led_cube.size, self.led_cube.size, 3) # 64x64 RGB
        self.displayed_back = np.zeros(dims).astype(np.float32)
        self.displayed_left = np.zeros_like(self.displayed_back)
        self.displayed_top = np.zeros_like(self.displayed_back)  
        self.displayed_bottom = np.zeros_like(self.displayed_back) 
        self.displayed_right = np.zeros_like(self.displayed_back)
        self.displayed_front = np.zeros_like(self.displayed_back) 

        # Starting Configuration
        offset = 40
        self.conway_back[15:20, 18+offset:23+offset] = unbounded
        self.conway_left[15+30:20+30, 18:23] = unbounded
        self.conway_top[15+20 : 20+20, 18:23] = unbounded
        # self.conway_right[15+20 : 20+20, 18:23] = unbounded
        # self.conway_front[15+10 : 20+10, 18+40:23+40] = unbounded
        # self.conway_bottom[15+10 : 20+10, 18:23] = unbounded

        # self.led_cube.rotateAngleAxis(np.deg2rad(45), glm.vec3(0, 0, 1))
        # self.led_cube.rotateAngleAxis(np.deg2rad(-10), glm.vec3(1, 0, 0))
        # self.led_cube.rotateAngleAxis(np.deg2rad(-10), glm.vec3(0, 1, 0))
    def blockCorners(self, array):
        array[0,0] = 0
        array[-1,0] = 0
        array[-1,-1] = 0
        array[0, -1] = 0

    def update(self, dt):

        self.conway_back = life_step(self.conway_back)
        self.conway_left = life_step(self.conway_left)
        self.conway_top = life_step(self.conway_top)
        self.conway_bottom = life_step(self.conway_bottom)
        self.conway_right = life_step(self.conway_right)
        self.conway_front = life_step(self.conway_front)

 
        self.blockCorners(self.conway_back)
        self.blockCorners(self.conway_left)
        self.blockCorners(self.conway_top)
        self.blockCorners(self.conway_bottom)
        self.blockCorners(self.conway_right)
        self.blockCorners(self.conway_front)

        # TODO assert self.conway_back == temp MAKE SURE ARRAYS ARE BEING CHANGED IN BLOCK CORNERS

        # Back-Left Join
        self.conway_left[0,:] = self.conway_back[-2,:]
        self.conway_back[-1,:] = self.conway_left[1,:]

        # # Top-Back Join
        self.conway_top[0,:] = np.flip(self.conway_back[:,-2])
        self.conway_back[:,-1] = np.flip(self.conway_top[1,:])

        # # Top-Left Join
        self.conway_top[:,0] = self.conway_left[:,-2]
        self.conway_left[:,-1] = self.conway_top[:,1]

        # # Bottom-left Join
        self.conway_left[:,0] = self.conway_bottom[:,-2]
        self.conway_bottom[:,-1] = self.conway_left[:,1]

        # # Bottom-back Join
        self.conway_bottom[0,:] = self.conway_back[:,1]
        self.conway_back[:,0] = self.conway_bottom[1,:]

        # # Bottom-right Join
        self.conway_bottom[:,0] = np.flip(self.conway_right[:,1])
        self.conway_right[:,0] = np.flip(self.conway_bottom[:,1])

        # Top-right
        self.conway_top[:,-1] = np.flip(self.conway_right[:,-2])
        self.conway_right[:,-1] = np.flip(self.conway_top[:,-2])

        # Top-front
        self.conway_top[-1,:] = self.conway_front[:,-2]
        self.conway_front[:,-1] = self.conway_top[-2,:]

        # Front-left
        self.conway_front[0,:] = self.conway_left[-2,:]
        self.conway_left[-1,:] = self.conway_front[1,:]

        # Front-Bottom
        self.conway_front[:,0] = np.flip(self.conway_bottom[-2,:])
        self.conway_bottom[-1,:] = np.flip(self.conway_front[:,1])

        # Front-right
        self.conway_front[-1,:] = self.conway_right[1,:]
        self.conway_right[0,:] = self.conway_front[-2,:]

        # Back-right
        self.conway_back[0,:] = self.conway_right[-2,:]
        self.conway_right[-1,:] = self.conway_back[1,:]

        # Convert conway to colours
        self.displayed_back[:,:,0] = self.conway_back.astype(np.float32)[1:65,1:65]

        self.displayed_left[:,:,1] = self.conway_left.astype(np.float32)[1:65,1:65]

        self.displayed_top[:,:,1] = self.conway_top.astype(np.float32)[1:65,1:65]
        self.displayed_top[:,:,0] = self.conway_top.astype(np.float32)[1:65,1:65]

        self.displayed_bottom[:,:,1] = self.conway_bottom.astype(np.float32)[1:65,1:65]
        self.displayed_bottom[:,:,1] = self.conway_bottom.astype(np.float32)[1:65,1:65]

        self.displayed_right[:,:,0] = self.conway_right.astype(np.float32)[1:65,1:65]
        self.displayed_right[:,:,2] = self.conway_right.astype(np.float32)[1:65,1:65]  

        self.displayed_front[:,:,0] = self.conway_front.astype(np.float32)[1:65,1:65]
        self.displayed_front[:,:,1] = self.conway_front.astype(np.float32)[1:65,1:65]      

        # Back/Left Join
        # self.displayed_back[-1,1:5,1] = 1       
        # self.displayed_left[0,1:5,1] = 1

        # Top-back Join
        # self.displayed_top[0,1:5,:] = 1
        # self.displayed_back[1:5,-1,:] = 1

        # Top-left Join
        # self.displayed_top[1:5,0,:] = 1
        # self.displayed_left[1:5,-1,:] = 1

        # Bottom-left Join
        # self.displayed_left[1:5,0,:] = 1
        # self.displayed_bottom[1:5,-1,:] = 1

        # Bottom-back Join
        # self.displayed_bottom[0,:,:] = 1
        # self.displayed_back[:,0,:] = 1

        # Bottom-right Join
        # self.displayed_bottom[1:10,0,:] = 1
        # self.displayed_right[1:10,0,:] = 1

        # Top-right join
        # self.displayed_top[1:10,-1,:] = 1
        # self.displayed_right[1:10,-1,:] = 1

        # Top-front join
        # self.displayed_top[-1,1:10,:] = 1
        # self.displayed_front[1:10,-1,:] = 1

        # Front-left join
        # self.displayed_front[0,1:10,:] = 1
        # self.displayed_left[-1,1:10,:] = 1

        # Front-bottom join
        # self.displayed_front[1:10,0,:] = 1
        # self.displayed_bottom[-1,1:10,:] = 1

        # Front-right join
        # self.displayed_front[-1,1:10,:] = 1
        # self.displayed_right[0,1:10,:] = 1

        # Back-right
        # self.displayed_back[0,1:10,:] = 1
        # self.displayed_right[-1,1:10,:] = 1



        self.led_cube.updateFace(Face.BACK, self.displayed_back)
        self.led_cube.updateFace(Face.LEFT, self.displayed_left)
        self.led_cube.updateFace(Face.TOP, self.displayed_top)
        self.led_cube.updateFace(Face.BOTTOM, self.displayed_bottom)
        self.led_cube.updateFace(Face.RIGHT, self.displayed_right)
        self.led_cube.updateFace(Face.FRONT, self.displayed_front)
        self.led_cube.update()

        # Todo check if patttern has existed in the last N interations. If so, start new pattern
        # deque

        # time.sleep(0.1)

        # self.led_cube.updateFaces(cube_faces)
        # self.led_cube.update()
        # print(time.time())
        # self.led_cube.rotateAngleAxis(np.deg2rad(45), glm.vec3(0, 0, 1))


if __name__ == "__main__":
    app = Conway()
    app.run()
    del app
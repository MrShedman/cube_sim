#!/usr/bin/env python

from cube_sim.application import Application
from cube_sim.camera import Camera
from cube_sim.led_cube import LEDCube, Face
from cube_sim.endless_surface import Cell, MovingCell, EndlessSurface
from cube_sim.color import *

import numpy as np
import pygame as pg
import glm
import math
import random
import time

MAX_SPEED = 0.0075

class Glyph(MovingCell):
    def __init__(self, surface):
        self.surface = surface
        f = Face.TOP
        p = glm.vec2(random.uniform(0, surface.dims), random.uniform(0, surface.dims))

        speed = random.uniform(MAX_SPEED*0.2, MAX_SPEED)
        direction = random.choice([-1, 1])
        axis = random.choice([0, 1])
        v = glm.vec2()
        v[axis] = speed * direction

        super().__init__(f, p, v)
        self.col = glm.vec3(0, 1, 0)
        self.length = random.randint(8, 25)
        self.tail = list()
        self.speckle_strength = 0.8
        self.speckle_speed = 10
        self.speckle_time = time.time() - self.speckle_speed
        self.genSpeckle()

    def step(self, dt):
        self.fpos += self.vel / dt

        if self.surface.update(self):
            self.tail = [Cell(self.face, self.ipos, self.col)] + self.tail   #add new at front
            if len(self.tail) > self.length:
                self.tail = self.tail[:-1]      #remove last
            if self.tail[-1].face == Face.BOTTOM:
                self.__init__(self.surface)

        self.genSpeckle()

    def genSpeckle(self):
        tnow = time.time()
        if (tnow - self.speckle_time) > 1.0/self.speckle_speed:        
            self.speckle = np.random.random_sample(self.length) * self.speckle_strength + (1 - self.speckle_strength)
            self.speckle_time = tnow
            for i, c in enumerate(self.tail):
                fade = (1 - (i / self.length)) *  self.speckle[i]
                c.col = glm.vec3(fadeColour(self.col, fade, 0.15))

class Matrix(Application):
    def __init__(self):
        super().__init__(1280, 720, 60, 64)
        self.surface = EndlessSurface(self.led_cube.size)
        self.glyphs = []
        for i in range(500):
            self.glyphs.append(Glyph(self.surface))

    def update(self, dt):
        t0 = time.time()
        cube_faces = self.led_cube.getCubeArrayAsColour([0.1, 0.1, 0.1])

        for g in self.glyphs:
            g.step(dt)
            for cell in g.tail:
                if cell.face is not Face.TOP and cell.face is not Face.BOTTOM:
                    cube_faces[cell.face, cell.ipos.x, cell.ipos.y] = cell.col

        self.led_cube.updateFaces(cube_faces)
        self.led_cube.update()
        t1 = time.time()
        print((t1-t0)*1000)

if __name__ == "__main__":
    app = Matrix()
    app.run()
    del app
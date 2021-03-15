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
        self.speckle_speed = 10
        self.speckle_time = time.time() - self.speckle_speed
        self.genSpeckle()

    def step(self, dt):
        self.fpos += self.vel / dt

        ipos = glm.ivec2(glm.floor(self.fpos))
        movedCell = False
        if ipos != self.ipos:
            movedCell = True
        self.ipos = ipos

        self.surface.update(self)

        if movedCell:
            pos = glm.ivec2(self.fpos)
            if len(self.tail) > 0:
                frontCell = self.tail[0]
                # something is causing duplicates to be added to the front triggering self intersection
                if frontCell.face != self.face or frontCell.ipos != pos:
                    self.tail = [Cell(self.face, pos)] + self.tail   #add new at front
                    if len(self.tail) > self.length:
                        self.tail = self.tail[:-1]      #remove last
            else:
                self.tail = [Cell(self.face, pos)] + self.tail   #add new at front
        
        if len(self.tail) > 0:
            if self.tail[-1].face == Face.BOTTOM:
                self.__init__(self.surface)

        self.genSpeckle()

    def genSpeckle(self):
        tnow = time.time()
        if (tnow - self.speckle_time) > 1.0/self.speckle_speed:        
            self.speckle = np.random.random_sample(self.length) * (1 - 0.5) + 0.5
            self.speckle_time = tnow

    def getPosition(self, i):
        return self.tail[i]

    def getColourFaded(self, i):
        col = fadeColour(self.col, 1 - (i / self.length), 0.15)
        col[1] *= self.speckle[i]
        return col

class Matrix(Application):
    def __init__(self):
        super().__init__(1280, 720, 60, 64)
        self.surface = EndlessSurface(self.led_cube.size)
        self.glyphs = []
        for i in range(200):
            self.glyphs.append(Glyph(self.surface))

    def update(self, dt):
        cube_faces = self.led_cube.getCubeArrayAsColour([0.1, 0.1, 0.1])

        for g in self.glyphs:
            g.step(dt)
            for i in range(len(g.tail)):
                cell = g.getPosition(i)
                if cell.face != Face.TOP:
                    cube_faces[cell.face, cell.ipos.x, cell.ipos.y] = g.getColourFaded(i)

        self.led_cube.updateFaces(cube_faces)
        self.led_cube.update()

if __name__ == "__main__":
    app = Matrix()
    app.run()
    del app
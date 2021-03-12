#!/usr/bin/env python

from cube_sim.application import Application
from cube_sim.camera import Camera
from cube_sim.led_cube import LEDCube, Face
from cube_sim.color import *

import numpy as np
import glm
import math
import random

MAX_SPEED = 0.0025

class Particle():
    def __init__(self):
        self.face = Face.LEFT
        self.pos = glm.vec2(32, 32)
        self.ipos = glm.ivec2(glm.floor(self.pos))
        #self.vel = glm.vec2(0, MAX_SPEED)#random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
        self.vel = glm.vec2(-MAX_SPEED, 0)
        self.col = genRandomStrongColour()
        self.age = 0.0
        self.eol = random.uniform(1, 3) # end of life

    def update(self, dt):
        self.pos += self.vel / dt
        self.ipos = glm.ivec2(glm.floor(self.pos))
        self.age += dt
        print(self.face, self.pos, self.ipos)
        if (self.face == Face.BACK and self.ipos.y > 63):
            self.face = Face.TOP
            self.pos = glm.vec2(0, self.pos.x)
            self.vel.x, self.vel.y = self.vel.y, self.vel.x
        if (self.face == Face.BACK and self.ipos.y < 0):
            self.face = Face.BOTTOM
            self.pos = glm.vec2(0, self.pos.x)
            self.vel.x, self.vel.y = -self.vel.y, self.vel.x
        if (self.face == Face.BACK and self.ipos.x > 63):
            self.face = Face.LEFT
            self.pos = glm.vec2(0, self.pos.y)
        if (self.face == Face.BACK and self.ipos.x < 0):
            self.face = Face.RIGHT
            self.pos = glm.vec2(0, self.pos.y)

        if (self.face == Face.FRONT and self.ipos.x > 63):
            self.face = Face.RIGHT
            self.pos = glm.vec2(0, self.pos.y)
        if (self.face == Face.FRONT and self.ipos.x < 0):
            self.face = Face.LEFT
            self.pos = glm.vec2(0, self.pos.y)
        if (self.face == Face.FRONT and self.ipos.y > 63):
            self.face = Face.TOP
            self.pos = glm.vec2(63, self.pos.x)
            self.vel.x, self.vel.y = -self.vel.y, self.vel.x
        if (self.face == Face.FRONT and self.ipos.y < 0):
            self.face = Face.BOTTOM
            self.pos = glm.vec2(0, self.pos.x)
            self.vel.x, self.vel.y = self.vel.y, self.vel.x
 
        if (self.face == Face.LEFT and self.ipos.y > 63):
            self.face = Face.TOP
            self.pos = glm.vec2(self.pos.x, 0)
        if (self.face == Face.LEFT and self.ipos.y < 0):
            self.face = Face.BOTTOM
            self.pos = glm.vec2(self.pos.x, 63)
        if (self.face == Face.LEFT and self.ipos.x > 63):
            self.face = Face.FRONT
            self.pos = glm.vec2(0, self.pos.y)
        if (self.face == Face.LEFT and self.ipos.x < 0):
            self.face = Face.BACK
            self.pos = glm.vec2(63, self.pos.y)

    def getPosition(self):
        self.ipos = glm.ivec2(glm.floor(self.pos))
        return self.face, self.ipos

    def getColourFaded(self):
        return self.col#fadeColour(self.col, 1 - (self.age / self.eol))

class EndlessSurface(Application):
    def __init__(self):
        super().__init__(1280, 720, 60, 64)

        self.particles = []
        for i in range(1):
            self.particles.append(Particle())

    def update(self, dt):
        cube_faces = self.led_cube.getCubeArrayAsColour([0.1, 0.1, 0.1])

        for p in self.particles:
            p.update(dt)
            face_id, coords = p.getPosition()
            # face_id, uv_vec = getIndexFromSphereCoords(p.pos.x, p.pos.y)
            # uv_vec = glm.ivec2(glm.floor(uv_vec * self.led_cube.size))
            cube_faces[face_id, coords.x, coords.y] = p.getColourFaded()

        self.led_cube.updateFaces(cube_faces)
        self.led_cube.update()

if __name__ == "__main__":
    app = EndlessSurface()
    app.run()
    del app
#!/usr/bin/env python

from cube_sim.application import Application
from cube_sim.camera import Camera
from cube_sim.led_cube import LEDCube, Face
from cube_sim.color import *

import numpy as np
import pygame as pg
import glm
import math
import random

MAX_SPEED = 0.0075#15

class Particle():
    def __init__(self, dims):
        self.dims = dims - 1
        self.face = random.choice(list(Face))
        self.pos = glm.vec2(random.uniform(0, self.dims), random.uniform(0, self.dims))
        self.ipos = glm.ivec2(glm.floor(self.pos))

        speedx = random.uniform(MAX_SPEED*0.2, MAX_SPEED)
        speedy = random.uniform(MAX_SPEED*0.2, MAX_SPEED)
        signx = (random.randint(0, 1) * 2) - 1
        signy = (random.randint(0, 1) * 2) - 1
        self.vel = glm.vec2(speedx * signx, speedy * signy)
        self.col = genRandomStrongColour()
        self.trail = random.uniform(8, 64)
        i = np.argmax(self.vel)
        self.vel[i] = self.vel[i]
        self.vel[i^1] = 0
        self.pos_list = list()
        self.addNewPos(self.face, self.pos)

    def update(self, dt):
        self.pos += self.vel / dt
        ipos2 = glm.ivec2(glm.floor(self.pos))
        add2list = False
        if ipos2 != self.ipos:
            add2list = True
        self.ipos = ipos2

        if (self.face == Face.BACK and self.ipos.x > self.dims):
            self.face = Face.LEFT
            self.pos = glm.vec2(0, self.ipos.y)
        elif (self.face == Face.BACK and self.ipos.x < 0):
            self.face = Face.RIGHT
            self.pos = glm.vec2(self.dims, self.ipos.y)
        elif (self.face == Face.BACK and self.ipos.y > self.dims):
            self.face = Face.TOP
            self.pos = glm.vec2(0, self.dims - self.ipos.x)
            self.vel.x, self.vel.y = self.vel.y, -self.vel.x
        elif (self.face == Face.BACK and self.ipos.y < 0):
            self.face = Face.BOTTOM
            self.pos = glm.vec2(0, self.ipos.x)
            self.vel.x, self.vel.y = -self.vel.y, self.vel.x

        elif (self.face == Face.FRONT and self.ipos.x > self.dims):
            self.face = Face.RIGHT
            self.pos = glm.vec2(0, self.ipos.y)
        elif (self.face == Face.FRONT and self.ipos.x < 0):
            self.face = Face.LEFT
            self.pos = glm.vec2(self.dims, self.ipos.y)
        elif (self.face == Face.FRONT and self.ipos.y > self.dims):
            self.face = Face.TOP
            self.pos = glm.vec2(self.dims, self.ipos.x)
            self.vel.x, self.vel.y = -self.vel.y, self.vel.x
        elif (self.face == Face.FRONT and self.ipos.y < 0):
            self.face = Face.BOTTOM
            self.pos = glm.vec2(self.dims, self.dims - self.ipos.x)
            self.vel.x, self.vel.y = self.vel.y, -self.vel.x
 
        elif (self.face == Face.LEFT and self.ipos.x > self.dims):
            self.face = Face.FRONT
            self.pos = glm.vec2(0, self.ipos.y)
        elif (self.face == Face.LEFT and self.ipos.x < 0):
            self.face = Face.BACK
            self.pos = glm.vec2(self.dims, self.ipos.y)
        elif (self.face == Face.LEFT and self.ipos.y > self.dims):
            self.face = Face.TOP
            self.pos = glm.vec2(self.ipos.x, 0)
        elif (self.face == Face.LEFT and self.ipos.y < 0):
            self.face = Face.BOTTOM
            self.pos = glm.vec2(self.ipos.x, self.dims)

        elif (self.face == Face.RIGHT and self.ipos.x > self.dims):
            self.face = Face.BACK
            self.pos = glm.vec2(0, self.ipos.y)
        elif (self.face == Face.RIGHT and self.ipos.x < 0):
            self.face = Face.FRONT
            self.pos = glm.vec2(self.dims, self.ipos.y)
        elif (self.face == Face.RIGHT and self.ipos.y > self.dims):
            self.face = Face.TOP
            self.pos = glm.vec2(self.dims - self.ipos.x, self.dims)
            self.vel = -self.vel
        elif (self.face == Face.RIGHT and self.ipos.y < 0):
            self.face = Face.BOTTOM
            self.pos = glm.vec2(self.dims - self.ipos.x, 0)
            self.vel = -self.vel

        elif (self.face == Face.TOP and self.ipos.x > self.dims):
            self.face = Face.FRONT
            self.pos = glm.vec2(self.ipos.y, self.dims)
            self.vel.x, self.vel.y = self.vel.y, -self.vel.x
        elif (self.face == Face.TOP and self.ipos.x < 0):
            self.face = Face.BACK
            self.pos = glm.vec2(self.dims - self.ipos.y, self.dims)
            self.vel.x, self.vel.y = -self.vel.y, self.vel.x
        elif (self.face == Face.TOP and self.ipos.y > self.dims):
            self.face = Face.RIGHT
            self.pos = glm.vec2(self.dims - self.ipos.x, self.dims)
            self.vel = -self.vel
        elif (self.face == Face.TOP and self.ipos.y < 0):
            self.face = Face.LEFT
            self.pos = glm.vec2(self.ipos.x, self.dims)

        elif (self.face == Face.BOTTOM and self.ipos.x > self.dims):
            self.face = Face.FRONT
            self.pos = glm.vec2(self.dims - self.ipos.y, 0)
            self.vel.x, self.vel.y = -self.vel.y, self.vel.x
        elif (self.face == Face.BOTTOM and self.ipos.x < 0):
            self.face = Face.BACK
            self.pos = glm.vec2(self.ipos.y, 0)
            self.vel.x, self.vel.y = self.vel.y, -self.vel.x
        elif (self.face == Face.BOTTOM and self.ipos.y > self.dims):
            self.face = Face.LEFT
            self.pos = glm.vec2(self.ipos.x, 0)
        elif (self.face == Face.BOTTOM and self.ipos.y < 0):
            self.face = Face.RIGHT
            self.pos = glm.vec2(self.dims - self.ipos.x, 0)
            self.vel = -self.vel

        if add2list:
            self.addNewPos(self.face, self.pos)
            # if random.uniform(0, 9) > 8:
            #     # self.vel.x, self.vel.y = self.vel.y, self.vel.x
            #     rot = random.randint(-1, 1) * math.pi/2.0
            #     t = glm.rotate(glm.mat4(1), rot, glm.vec3(0, 0, 1))
            #     self.vel = (glm.vec4(self.vel, 0, 0) * t).xy

        if self.selfIntersect():
            self.__init__(self.dims+1)

    def left(self):
        t = glm.rotate(glm.mat4(1), math.pi/2, glm.vec3(0, 0, 1))
        self.vel = (glm.vec4(self.vel, 0, 0) * t).xy
 
    def right(self):
        t = glm.rotate(glm.mat4(1), -math.pi/2, glm.vec3(0, 0, 1))
        self.vel = (glm.vec4(self.vel, 0, 0) * t).xy

    def selfIntersect(self):
        return len(self.pos_list) != len(set(self.pos_list))

    def addNewPos(self, face, pos):
        pos = glm.ivec2(pos)
        if len(self.pos_list) > 0:
            f, p = self.pos_list[0]
            if f != face or p != pos: # something is causing duplicates to be added to the front triggering self intersection
                self.pos_list = [(face, pos)] + self.pos_list   #add new at front
                if len(self.pos_list) > self.trail:
                    self.pos_list = self.pos_list[:-1]      #remove last
        else:
            self.pos_list = [(face, pos)] + self.pos_list   #add new at front

    def getPosition(self, i):
        return self.pos_list[i]

    def getColourFaded(self, i):
        return fadeColour(self.col, 1 - (i / self.trail))

class EndlessSurface(Application):
    def __init__(self):
        super().__init__(1280, 720, 60, 64)

        self.particles = []
        for i in range(50):
            self.particles.append(Particle(self.led_cube.size))

    def handleEvent(self, event):
        if (event.type == pg.KEYDOWN and event.key == pg.K_a):
            self.particles[0].left() 
        if (event.type == pg.KEYDOWN and event.key == pg.K_d):
            self.particles[0].right()

    def update(self, dt):
        cube_faces = self.led_cube.getCubeArrayAsColour([0.1, 0.1, 0.1])

        for p in self.particles:
            p.update(dt)
            for i in range(len(p.pos_list)):
                face_id, coords = p.getPosition(i)
                cube_faces[face_id, coords.x, coords.y] = p.getColourFaded(i)

        self.led_cube.updateFaces(cube_faces)
        self.led_cube.update()

if __name__ == "__main__":
    app = EndlessSurface()
    app.run()
    del app
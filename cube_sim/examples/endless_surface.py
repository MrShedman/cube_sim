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

MAX_SPEED = 0.0075

class Cell():
    def __init__(self, face, pos):
        self.ipos = glm.ivec2(pos)
        self.face = face

class MovingCell(Cell):
    def __init__(self, face, pos, vel):
        self.fpos = glm.vec2(pos)
        self.vel = glm.vec2(vel)
        super().__init__(face, glm.floor(self.fpos))

class Snake(MovingCell):
    def __init__(self, surface):
        self.surface = surface
        f = random.choice(list(Face))
        p = glm.vec2(random.uniform(0, surface.dims), random.uniform(0, surface.dims))

        speed = random.uniform(MAX_SPEED*0.2, MAX_SPEED)
        direction = random.choice([-1, 1])
        axis = random.choice([0, 1])
        v = glm.vec2()
        v[axis] = speed * direction

        super().__init__(f, p, v)
        self.col = genRandomStrongColour()
        self.length = random.uniform(2, 4)
        self.tail = list()

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

    def eat(self, food):
        for f in food:
            if self.face == f.face and self.ipos == f.ipos:
                self.length += 1
                food.remove(f)

    def left(self):
        t = glm.rotate(glm.mat4(1), math.pi/2, glm.vec3(0, 0, 1))
        self.vel = (glm.vec4(self.vel, 0, 0) * t).xy
 
    def right(self):
        t = glm.rotate(glm.mat4(1), -math.pi/2, glm.vec3(0, 0, 1))
        self.vel = (glm.vec4(self.vel, 0, 0) * t).xy

    def collide(self):
        for c in self.tail[1:]: # the tail also contains the head
            if self.face == c.face and self.ipos == c.ipos:
                self.__init__(self.surface)

    def getPosition(self, i):
        return self.tail[i]

    def getColourFaded(self, i):
        return fadeColour(self.col, 1 - (i / self.length))

class EndlessCubeSurface():
    def __init__(self, size):
        self.dims = size - 1

    def getRandomCell(self):
        f = random.choice(list(Face))
        p = glm.vec2(random.uniform(0, self.dims), random.uniform(0, self.dims))
        return Cell(f, p)

    def update(self, mcell):
        hasVel = issubclass(type(mcell), MovingCell)

        if (mcell.face == Face.BACK and mcell.ipos.x > self.dims):
            mcell.face = Face.LEFT
            mcell.fpos = glm.vec2(0, mcell.ipos.y)
        elif (mcell.face == Face.BACK and mcell.ipos.x < 0):
            mcell.face = Face.RIGHT
            mcell.fpos = glm.vec2(self.dims, mcell.ipos.y)
        elif (mcell.face == Face.BACK and mcell.ipos.y > self.dims):
            mcell.face = Face.TOP
            mcell.fpos = glm.vec2(0, self.dims - mcell.ipos.x)
            if hasVel:
                mcell.vel.x, mcell.vel.y = mcell.vel.y, -mcell.vel.x
        elif (mcell.face == Face.BACK and mcell.ipos.y < 0):
            mcell.face = Face.BOTTOM
            mcell.fpos = glm.vec2(0, mcell.ipos.x)
            if hasVel:
                mcell.vel.x, mcell.vel.y = -mcell.vel.y, mcell.vel.x

        elif (mcell.face == Face.FRONT and mcell.ipos.x > self.dims):
            mcell.face = Face.RIGHT
            mcell.fpos = glm.vec2(0, mcell.ipos.y)
        elif (mcell.face == Face.FRONT and mcell.ipos.x < 0):
            mcell.face = Face.LEFT
            mcell.fpos = glm.vec2(self.dims, mcell.ipos.y)
        elif (mcell.face == Face.FRONT and mcell.ipos.y > self.dims):
            mcell.face = Face.TOP
            mcell.fpos = glm.vec2(self.dims, mcell.ipos.x)
            if hasVel:
                mcell.vel.x, mcell.vel.y = -mcell.vel.y, mcell.vel.x
        elif (mcell.face == Face.FRONT and mcell.ipos.y < 0):
            mcell.face = Face.BOTTOM
            mcell.fpos = glm.vec2(self.dims, self.dims - mcell.ipos.x)
            if hasVel:
                mcell.vel.x, mcell.vel.y = mcell.vel.y, -mcell.vel.x
 
        elif (mcell.face == Face.LEFT and mcell.ipos.x > self.dims):
            mcell.face = Face.FRONT
            mcell.fpos = glm.vec2(0, mcell.ipos.y)
        elif (mcell.face == Face.LEFT and mcell.ipos.x < 0):
            mcell.face = Face.BACK
            mcell.fpos = glm.vec2(self.dims, mcell.ipos.y)
        elif (mcell.face == Face.LEFT and mcell.ipos.y > self.dims):
            mcell.face = Face.TOP
            mcell.fpos = glm.vec2(mcell.ipos.x, 0)
        elif (mcell.face == Face.LEFT and mcell.ipos.y < 0):
            mcell.face = Face.BOTTOM
            mcell.fpos = glm.vec2(mcell.ipos.x, self.dims)

        elif (mcell.face == Face.RIGHT and mcell.ipos.x > self.dims):
            mcell.face = Face.BACK
            mcell.fpos = glm.vec2(0, mcell.ipos.y)
        elif (mcell.face == Face.RIGHT and mcell.ipos.x < 0):
            mcell.face = Face.FRONT
            mcell.fpos = glm.vec2(self.dims, mcell.ipos.y)
        elif (mcell.face == Face.RIGHT and mcell.ipos.y > self.dims):
            mcell.face = Face.TOP
            mcell.fpos = glm.vec2(self.dims - mcell.ipos.x, self.dims)
            if hasVel:
                mcell.vel = -mcell.vel
        elif (mcell.face == Face.RIGHT and mcell.ipos.y < 0):
            mcell.face = Face.BOTTOM
            mcell.fpos = glm.vec2(self.dims - mcell.ipos.x, 0)
            if hasVel:
                mcell.vel = -mcell.vel

        elif (mcell.face == Face.TOP and mcell.ipos.x > self.dims):
            mcell.face = Face.FRONT
            mcell.fpos = glm.vec2(mcell.ipos.y, self.dims)
            if hasVel:
                mcell.vel.x, mcell.vel.y = mcell.vel.y, -mcell.vel.x
        elif (mcell.face == Face.TOP and mcell.ipos.x < 0):
            mcell.face = Face.BACK
            mcell.fpos = glm.vec2(self.dims - mcell.ipos.y, self.dims)
            if hasVel:
                mcell.vel.x, mcell.vel.y = -mcell.vel.y, mcell.vel.x
        elif (mcell.face == Face.TOP and mcell.ipos.y > self.dims):
            mcell.face = Face.RIGHT
            mcell.fpos = glm.vec2(self.dims - mcell.ipos.x, self.dims)
            if hasVel:
                mcell.vel = -mcell.vel
        elif (mcell.face == Face.TOP and mcell.ipos.y < 0):
            mcell.face = Face.LEFT
            mcell.fpos = glm.vec2(mcell.ipos.x, self.dims)

        elif (mcell.face == Face.BOTTOM and mcell.ipos.x > self.dims):
            mcell.face = Face.FRONT
            mcell.fpos = glm.vec2(self.dims - mcell.ipos.y, 0)
            if hasVel:
                mcell.vel.x, mcell.vel.y = -mcell.vel.y, mcell.vel.x
        elif (mcell.face == Face.BOTTOM and mcell.ipos.x < 0):
            mcell.face = Face.BACK
            mcell.fpos = glm.vec2(mcell.ipos.y, 0)
            if hasVel:
                mcell.vel.x, mcell.vel.y = mcell.vel.y, -mcell.vel.x
        elif (mcell.face == Face.BOTTOM and mcell.ipos.y > self.dims):
            mcell.face = Face.LEFT
            mcell.fpos = glm.vec2(mcell.ipos.x, 0)
        elif (mcell.face == Face.BOTTOM and mcell.ipos.y < 0):
            mcell.face = Face.RIGHT
            mcell.fpos = glm.vec2(self.dims - mcell.ipos.x, 0)
            if hasVel:
                mcell.vel = -mcell.vel

class EndlessSurface(Application):
    def __init__(self):
        super().__init__(1280, 720, 60, 64)
        self.surface = EndlessCubeSurface(self.led_cube.size)
        self.snakes = []
        self.food = []
        for i in range(1):
            self.snakes.append(Snake(self.surface))
        for i in range(100):
            self.food.append(self.surface.getRandomCell())

    def handleEvent(self, event):
        if (event.type == pg.KEYDOWN and event.key == pg.K_a):
            self.snakes[0].left() 
        if (event.type == pg.KEYDOWN and event.key == pg.K_d):
            self.snakes[0].right()

    def update(self, dt):
        cube_faces = self.led_cube.getCubeArrayAsColour([0.1, 0.1, 0.1])

        for f in self.food:
            cube_faces[f.face, f.ipos.x, f.ipos.y] = [1, 1, 1]

        for s in self.snakes:
            s.step(dt)
            s.collide()
            s.eat(self.food)
            for i in range(len(s.tail)):
                cell = s.getPosition(i)
                cube_faces[cell.face, cell.ipos.x, cell.ipos.y] = s.getColourFaded(i)

        self.led_cube.updateFaces(cube_faces)
        self.led_cube.update()

if __name__ == "__main__":
    app = EndlessSurface()
    app.run()
    del app
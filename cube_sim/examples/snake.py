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

MAX_SPEED = 0.0075

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
        self.length = random.randint(2, 4)
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
        return fadeColour(self.col, 1 - (i / self.length), 0.15)

class SnakeGame(Application):
    def __init__(self):
        super().__init__(1280, 720, 60, 64)
        self.surface = EndlessSurface(self.led_cube.size)
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
    app = SnakeGame()
    app.run()
    del app
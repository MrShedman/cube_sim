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
        self.length = random.randint(10, 20)
        self.tail = list()

    def step(self, dt):
        self.fpos += self.vel / dt

        if self.surface.update(self):
            self.tail = [Cell(self.face, self.ipos)] + self.tail   #add new at front
            if len(self.tail) > self.length:
                self.tail = self.tail[:-1]      #remove last
            for i, c in enumerate(self.tail):
                c.col = fadeColour(self.col, 1 - (i / self.length), 0.15)

    def eat(self, food):
        for f in food:
            if self.face == f.face and self.ipos == f.ipos:
                self.length += 1
                food.remove(f)

    def left(self):
        self.vel *= glm.mat2x2([[0, 1], [-1, 0]])
 
    def right(self):
        self.vel *= glm.mat2x2([[0, -1], [1, 0]])

    def collide(self):
        for c in self.tail[1:]: # the tail also contains the head
            if self.face == c.face and self.ipos == c.ipos:
                self.__init__(self.surface)

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
            cube_faces[f.face, f.ipos.x, f.ipos.y] = f.col

        for s in self.snakes:
            s.step(dt)
            s.collide()
            s.eat(self.food)
            for c in s.tail:
                cube_faces[c.face, c.ipos.x, c.ipos.y] = c.col

        self.led_cube.updateFaces(cube_faces)
        self.led_cube.update()

if __name__ == "__main__":
    app = SnakeGame()
    app.run()
    del app
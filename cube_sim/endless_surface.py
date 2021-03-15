#!/usr/bin/env python

from cube_sim.led_cube import Face

import glm
import random

class Cell():
    def __init__(self, face, pos, col = glm.vec3(1, 1, 1)):
        self.ipos = glm.ivec2(pos)
        self.face = face
        self.col = col

class MovingCell(Cell):
    def __init__(self, face, pos, vel):
        self.fpos = glm.vec2(pos)
        self.vel = glm.vec2(vel)
        super().__init__(face, glm.floor(self.fpos))

class EndlessSurface():
    def __init__(self, size):
        self.dims = size - 1

    def getRandomCell(self):
        f = random.choice(list(Face))
        p = glm.vec2(random.uniform(0, self.dims), random.uniform(0, self.dims))
        return Cell(f, p)

    def update(self, mcell):
        hasVel = issubclass(type(mcell), MovingCell)

        ipos = glm.ivec2(glm.floor(mcell.fpos))
        movedCell = False
        if ipos != mcell.ipos:
            movedCell = True
        mcell.ipos = ipos

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
        
        mcell.ipos = glm.ivec2(mcell.fpos)
        return movedCell
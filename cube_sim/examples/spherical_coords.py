#!/usr/bin/env python

from cube_sim.application import Application
from cube_sim.transform import Transform
from cube_sim.shader import Shader
from cube_sim.camera import Camera
from cube_sim.mesh import Mesh
from cube_sim.mesh_view import MeshView
from cube_sim.led_cube import LEDCube, Face
from cube_sim.grid import Grid

import pygame as pg
import numpy as np
import glm
import math
import random

MAX_SPEED = 0.001

class Particle():
    def __init__(self):
        self.pos = glm.vec2(math.pi, math.pi)
        self.vel = glm.vec2(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
        self.col = glm.vec3(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
        self.age = 0.0

    def update(self, dt):
        self.pos += self.vel / dt
        self.pos = glm.mod(self.pos, 2.0 * math.pi)
        # self.vel += 
        self.age += dt

    def getIndexInRange(self, range):
        id_vec = glm.floor(self.pos / (2.0 * math.pi) * range)
        return int(id_vec.x + id_vec.y * range)

class SphericalCoords(Application):
    def __init__(self):
        super().__init__(1280, 720, 60)
   
        self.camera = Camera()
        self.camera.setPosition(glm.vec3(-5.0, 0.0, 2.0))
        self.camera.setPitch(math.radians(-20))

        self.shader = Shader('model.vert', 'model.frag')

        self.led_cube = LEDCube(64)
        self.led_cube.buildMesh()
        self.led_cube.buildMeshOutline()
        self.led_cube.setPosition(glm.vec3(0, 0, 1))

        self.grid = Grid()
        self.grid.buildMesh()

        self.particles = []
        for i in range(100):
            self.particles.append(Particle())

        self.wireframe = True
        self.cube_state = True

    def handleEvent(self, event):
        if (event.type == pg.KEYDOWN and event.key == pg.K_m):
            self.wireframe = not self.wireframe  
        if (event.type == pg.KEYDOWN and event.key == pg.K_c):
            self.cube_state = not self.cube_state 
            if self.cube_state:
                self.led_cube.makeCube()
            else:
                self.led_cube.makeSphere()          
        self.camera.handleEvent(event)

    def update(self, dt):
        dims = (self.led_cube.subdivision * self.led_cube.subdivision, 3)
        colours = np.zeros(dims).astype(np.float32)

        for p in self.particles:
            p.update(dt)
            colours[p.getIndexInRange(64)] = np.array(p.col)

        self.led_cube.updateFace(Face.BACK, colours)
        self.led_cube.update()

        self.camera.update(dt)

    def render(self):
        MeshView(self.led_cube, self.shader, self.camera).render(True, self.wireframe)
        MeshView(self.grid, self.shader, self.camera).render(True, False, True)

if __name__ == "__main__":
    app = SphericalCoords()
    app.run()
    del app
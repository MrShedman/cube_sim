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

class RandomSide(Application):
    def __init__(self):
        super().__init__(1280, 720, 60)
   
        self.camera = Camera()
        self.camera.setPosition(glm.vec3(-3.0, 0.0, 0.0))

        self.shader = Shader('model.vert', 'model.frag')

        self.led_cube = LEDCube(64)
        self.led_cube.buildMesh()
        self.led_cube.buildMeshOutline()

        self.grid = Grid()
        self.grid.buildMesh()

        self.wireframe = False
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
        colours = np.random.uniform(0, 1, dims).astype(np.float32)
        self.led_cube.updateFace(Face.LEFT, colours)
        self.led_cube.updateFace(Face.RIGHT, colours)
        self.led_cube.updateFace(Face.BOTTOM, colours)
        self.led_cube.update()

        self.camera.update(dt)

    def render(self):
        MeshView(self.led_cube, self.shader, self.camera).render(True, self.wireframe)
        MeshView(self.grid, self.shader, self.camera).render(True, False, True)

if __name__ == "__main__":
    app = RandomSide()
    app.run()
    del app
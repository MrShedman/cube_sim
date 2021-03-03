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

class RandomSide(Application):
    def __init__(self):
        super().__init__(1280, 720, 60, 64)

    def update(self, dt):
        dims = (self.led_cube.size * self.led_cube.size, 3)
        colours = np.random.uniform(0, 1, dims).astype(np.float32)
        self.led_cube.updateFace(Face.LEFT, colours)
        self.led_cube.updateFace(Face.RIGHT, colours)
        self.led_cube.updateFace(Face.BOTTOM, colours)
        self.led_cube.update()

if __name__ == "__main__":
    app = RandomSide()
    app.run()
    del app
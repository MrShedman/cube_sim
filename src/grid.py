#!/usr/bin/env python

import glm
import numpy as np
import OpenGL.GL as GL

from transform import Transform
from mesh import Mesh

class Grid(Transform):
    def __init__(self, interval = 0.5):
        super().__init__()
        self.interval = interval
        self.count = 0

    def addVertex(self, x, y, z):
        self.mesh.addVertex(x, y, z, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0)
        self.mesh.addIndex(self.count)
        self.count += 1

    def build(self):
        extent = 100
        segments, step = np.linspace(-extent, extent, int(extent / self.interval), False, True)

        self.mesh = Mesh(int(4 * step * len(segments)))
        self.mesh.mode = GL.GL_LINES

        for ix in segments:
            self.addVertex(ix, -extent, 0.0)
            self.addVertex(ix,  extent, 0.0)

        for iy in segments:
            self.addVertex( extent, iy, 0.0)
            self.addVertex(-extent, iy, 0.0)
        
        self.mesh.complete()
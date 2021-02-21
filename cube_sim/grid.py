#!/usr/bin/env python

import glm
import numpy as np
import OpenGL.GL as GL

from cube_sim.transform import Transform
from cube_sim.mesh import Mesh

class Grid(Transform):
    def __init__(self, interval = 0.5, extent = 50.0):
        super().__init__()
        self.interval = interval
        self.extent = extent
        self.count = 0

    def addVertex(self, x, y, z):
        self.mesh.addVertex(x, y, z, 0.0, 0.0, 1.0, 0.4, 0.4, 0.4)
        self.mesh.addIndex(self.count)
        self.count += 1

    def buildMesh(self):
        segments = np.linspace(-self.extent, self.extent, int((self.extent+0.5) / self.interval), endpoint=True)

        self.mesh = Mesh(4 * len(segments))
        self.mesh.mode = GL.GL_LINES

        for ix in segments:
            self.addVertex(ix, -self.extent, 0.0)
            self.addVertex(ix,  self.extent, 0.0)

        for iy in segments:
            self.addVertex( self.extent, iy, 0.0)
            self.addVertex(-self.extent, iy, 0.0)

        self.mesh.complete()
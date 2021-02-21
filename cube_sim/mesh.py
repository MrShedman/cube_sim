#!/usr/bin/env python

import OpenGL.GL as GL
import OpenGL.GLU as GLU
import ctypes
import glm
from cube_sim.vbo import VBO
from OpenGL.arrays import vbo
import numpy as np

class Mesh():
    def __init__(self, size):
        self.mode = GL.GL_TRIANGLES
        self.vcount = 0
        self.icount = 0

        self.positions = np.zeros(size, dtype=(np.float32, 3))
        self.normals = np.zeros(size, dtype=(np.float32, 3))
        self.colours = np.zeros(size, dtype=(np.float32, 3))
        self.indices = np.zeros(size, dtype=np.uint32)

    def __del__(self):
        GL.glDeleteVertexArrays(1, [self.vao])
        
    def addVertex(self, x, y, z, nx, ny, nz, r, g, b):
        self.positions[self.vcount] = np.array([x, y, z])
        self.normals[self.vcount] = np.array([nx, ny, nz])
        self.colours[self.vcount] = np.array([r, g, b])
        self.vcount += 1

    def addIndex(self, i):
        self.indices[self.icount] = i
        self.icount += 1

    def complete(self):
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)
        
        self.vbo_position = VBO(GL.GL_ARRAY_BUFFER, GL.GL_DYNAMIC_DRAW)
        self.vbo_position.data(self.positions.nbytes, self.positions)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 12, None)
        
        self.vbo_normal = VBO(GL.GL_ARRAY_BUFFER, GL.GL_DYNAMIC_DRAW)
        self.vbo_normal.data(self.normals.nbytes, self.normals)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 12, None)
        
        self.vbo_colour = VBO(GL.GL_ARRAY_BUFFER, GL.GL_DYNAMIC_DRAW)
        self.vbo_colour.data(self.colours.nbytes, self.colours)
        GL.glEnableVertexAttribArray(2)
        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, False, 12, None)

        self.ibo = VBO(GL.GL_ELEMENT_ARRAY_BUFFER, GL.GL_STATIC_DRAW)
        self.ibo.data(self.indices.nbytes, self.indices)

        GL.glBindVertexArray(0)

    def updatePositions(self):
        if len(self.positions) == self.vcount:
            self.vbo_position.sub_data(self.positions.nbytes, self.positions)

    def updateNormals(self):
        if len(self.normals) == self.vcount:
            self.vbo_normal.sub_data(self.normals.nbytes, self.normals)

    def updateColours(self):
        #if len(self.colours) == self.vcount:
        self.vbo_colour.sub_data(self.colours.nbytes, self.colours)

    def draw(self):
        GL.glBindVertexArray(self.vao)
        GL.glDrawElements(self.mode, len(self.indices), GL.GL_UNSIGNED_INT, None)

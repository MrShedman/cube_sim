#!/usr/bin/env python

import OpenGL.GL as GL
import OpenGL.GLU as GLU
import ctypes
import glm
from vbo import VBO
from OpenGL.arrays import vbo
import numpy as np

class Mesh():
    def __init__(self, size):
        self.vbo = VBO(GL.GL_ARRAY_BUFFER, GL.GL_STATIC_DRAW)
        self.ibo = VBO(GL.GL_ELEMENT_ARRAY_BUFFER, GL.GL_STATIC_DRAW)
        self.mode = GL.GL_TRIANGLES
        self.vcount = 0
        self.icount = 0

        self.vertices = np.zeros(size, [("position", np.float32, 3),("normal", np.float32, 3), ("colour", np.float32, 4)])
        self.indices = np.zeros(size, dtype=np.uint32)

    # def __del__(self):
    #     GL.glDeleteVertexArrays(1, [self.vao])
        
    def addVertex(self, x, y, z, nx, ny, nz, r, g, b, a):
        self.vertices[self.vcount] = np.array([([x, y, z], [nx, ny, nz], [r, g, b, a])], dtype=self.vertices.dtype)
        self.vcount += 1

    def addIndex(self, i):
        self.indices[self.icount] = i
        self.icount += 1

    def complete(self):
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        self.vbo.data(self.vertices.nbytes, self.vertices)
        self.ibo.data(self.indices.nbytes, self.indices)

        self.vbo.bind()
        self.ibo.bind()

        stride = self.vertices.strides[0]

        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, stride, ctypes.c_void_p(0))

        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, stride, ctypes.c_void_p(12))

        GL.glEnableVertexAttribArray(2)
        GL.glVertexAttribPointer(2, 4, GL.GL_FLOAT, False, stride, ctypes.c_void_p(24))

        GL.glBindVertexArray(0)

    def update(self):
        self.vbo.sub_data(self.vertices.nbytes, self.vertices)
        self.ibo.sub_data(self.indices.nbytes, self.indices)

    def getVertex(self, id):
        return self.vertices[id]

    def getPosition(self, id):
        return self.getVertex(id)[0]

    def getNormal(self, id):
        return self.getVertex(id)[1]

    def getColour(self, id):
        return self.getVertex(id)[2]

    def draw(self):
        GL.glBindVertexArray(self.vao)
        GL.glDrawElements(self.mode, len(self.indices), GL.GL_UNSIGNED_INT, None)

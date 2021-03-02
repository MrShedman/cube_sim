#!/usr/bin/env python

import OpenGL.GL as GL

class VBO:
    def __init__(self, target, usage):
        self.target = target
        self.usage = usage
        self.vbo = GL.glGenBuffers(1)

    def __del__(self):
        try:
            GL.glDeleteBuffers(1, [self.vbo])
        except:
            pass

    def bind(self):
        GL.glBindBuffer(self.target, self.vbo)

    def unbind(self):
        GL.glBindBuffer(self.target, 0)

    def data(self, data_size, data):
        self.bind()
        GL.glBufferData(self.target, data_size, data, self.usage)

    def sub_data(self, data_size, data):
        self.bind()
        GL.glBufferSubData(self.target, 0, data_size, data)

    def set_slot(self, slot, size):
        GL.glEnableVertexAttribArray(slot)
        GL.glVertexAttribPointer(slot, size, GL.GL_FLOAT, False, 0, None)
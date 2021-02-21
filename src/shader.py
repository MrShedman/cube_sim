#!/usr/bin/env python

import OpenGL.GL as GL
import OpenGL.GLU as GLU
import numpy as np
import glm

class Shader():
    def __init__(self, vertexFilename, fragmentFilename):
        self.load(vertexFilename, fragmentFilename)
        self.uniforms = dict()

    # def __del__(self):
    #     GL.glDeleteProgram(1, [self.program])

    def name(self):
        return self.program
    
    def bind(self):
        GL.glUseProgram(self.program)

    def unbind(self):
        GL.glUseProgram(None)

    def load(self, vertexFilename, fragmentFilename):
        vertex_code = open(vertexFilename, 'r').read()
        fragment_code = open(fragmentFilename, 'r').read()

        self.program = GL.glCreateProgram()
        vertex = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        fragment = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(vertex, vertex_code)
        GL.glCompileShader(vertex)

        # this logs issues the shader compiler finds.
        log = GL.glGetShaderInfoLog(vertex)
        if isinstance(log, bytes):
            log = log.decode()
        for line in log.split("\n"):
            print(line)

        GL.glAttachShader(self.program, vertex)
        GL.glShaderSource(fragment, fragment_code)
        GL.glCompileShader(fragment)

        # this logs issues the shader compiler finds.
        log = GL.glGetShaderInfoLog(fragment)
        if isinstance(log, bytes):
            log = log.decode()
        for line in log.split("\n"):
            print(line)

        GL.glAttachShader(self.program, fragment)
        GL.glValidateProgram(self.program)
        GL.glLinkProgram(self.program)

        GL.glDetachShader(self.program, vertex)
        GL.glDetachShader(self.program, fragment)
        self.bind()

    def cacheUniform(self, uniform):
        if uniform not in self.uniforms:
            self.uniforms[uniform] = GL.glGetUniformLocation(self.name(), uniform)

    def setUniform1f(self, uniform, scalar):
        self.cacheUniform(uniform)
        GL.glUniform1f(self.uniforms[uniform], scalar)

    def setUniform2f(self, uniform, vec2f):
        self.cacheUniform(uniform)
        GL.glUniform2f(self.uniforms[uniform], vec2f.x, vec2f.y)

    def setUniform3f(self, uniform, vec3f):
        self.cacheUniform(uniform)
        GL.glUniform3f(self.uniforms[uniform], vec3f.x, vec3f.y, vec3f.z)

    def setUniform4f(self, uniform, vec4f):
        self.cacheUniform(uniform)
        GL.glUniform4f(self.uniforms[uniform], vec4f.x, vec4f.y, vec4f.z, vec4f.w)

    def setUniformMatrix4f(self, uniform, mat4x4):
        self.cacheUniform(uniform)
        GL.glUniformMatrix4fv(self.uniforms[uniform], 1, False, np.array(mat4x4))
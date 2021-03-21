#!/usr/bin/env python

import OpenGL.GL as GL
import numpy as np
import glm

from cube_sim.resource import getResource

class Shader():
    def __init__(self, vertexFilename, fragmentFilename):
        self.load(vertexFilename, fragmentFilename)
        self.uniforms = dict()

    def __del__(self):
        try:
            GL.glDeleteProgram(self.program)
        except:
            pass
        
    def name(self):
        return self.program
    
    def bind(self):
        GL.glUseProgram(self.program)

    def unbind(self):
        GL.glUseProgram(None)

    def load(self, vertexFilename, fragmentFilename):
        self.program = GL.glCreateProgram()
        vertex = self.compile(GL.GL_VERTEX_SHADER, vertexFilename)
        fragment = self.compile(GL.GL_FRAGMENT_SHADER, fragmentFilename)

        GL.glValidateProgram(self.program)
        GL.glLinkProgram(self.program)

        GL.glDetachShader(self.program, vertex)
        GL.glDetachShader(self.program, fragment)

    def compile(self, shader_type, file):
        shader_code = open(getResource(file), 'r').read()
        shader_obj = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader_obj, shader_code)
        GL.glCompileShader(shader_obj)

        # this logs issues the shader compiler finds.
        log = GL.glGetShaderInfoLog(shader_obj)
        if isinstance(log, bytes):
            log = log.decode()
        if len(log) > 0:
            for line in log.split("\n"):
                print(line)

        GL.glAttachShader(self.program, shader_obj)
        return shader_obj

    def isLinked(self):
        return GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS, None) == 1

    def cacheUniform(self, uniform):
        if uniform not in self.uniforms:
            self.uniforms[uniform] = GL.glGetUniformLocation(self.name(), uniform)

    def setUniform1f(self, uniform, scalar):
        self.cacheUniform(uniform)
        GL.glUniform1f(self.uniforms[uniform], scalar)

    def setUniform2f(self, uniform, vec2f):
        self.cacheUniform(uniform)
        GL.glUniform2f(self.uniforms[uniform], vec2f[0], vec2f[1])

    def setUniform3f(self, uniform, vec3f):
        self.cacheUniform(uniform)
        GL.glUniform3f(self.uniforms[uniform], vec3f[0], vec3f[1], vec3f[2])

    def setUniform4f(self, uniform, vec4f):
        self.cacheUniform(uniform)
        GL.glUniform4f(self.uniforms[uniform], vec4f[0], vec4f[1], vec4f[2], vec4f[3])

    def setUniformMatrix4f(self, uniform, mat4x4):
        self.cacheUniform(uniform)
        GL.glUniformMatrix4fv(self.uniforms[uniform], 1, False, np.array(mat4x4))
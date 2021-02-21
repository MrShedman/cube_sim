#!/usr/bin/env python

import OpenGL.GL as GL
import OpenGL.GLU as GLU
import glm
from mesh import Mesh
from shader import Shader
from camera import Camera

class MeshView():
    def __init__(self, renderable, shader, camera):
        self.renderable = renderable
        self.shader = shader
        self.camera = camera

    def render(self, solid=True, wireframe=False, fade=False):
        self.shader.setUniformMatrix4f("view", self.camera.getViewMatrix())
        self.shader.setUniformMatrix4f("projection", self.camera.getProjectionMatrix())

        self.shader.setUniform3f("lightColour", glm.vec3(1.0, 1.0, 1.0))
        self.shader.setUniform3f("viewPos", self.camera.getPosition())

        if fade:
            self.shader.setUniform1f("fade", 1.0)
            self.shader.setUniform3f("lightPos", glm.vec3(0.5, 0.5, 20.0))
        else:
            self.shader.setUniform1f("fade", 0.0)
            self.shader.setUniform3f("lightPos", self.camera.getPosition())

        if solid:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
            self.shader.setUniform1f("wireframe", 1.0)
            self.shader.setUniformMatrix4f("model", self.renderable.getTransform())
            self.renderable.mesh.draw()
        
        if wireframe:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
            self.shader.setUniform1f("wireframe", 0.0)
            old_scale = self.renderable.getScale()
            self.renderable.setScale(old_scale * 1.001)
            self.shader.setUniformMatrix4f("model", self.renderable.getTransform())
            self.renderable.setScale(old_scale)
            self.renderable.mesh.draw()
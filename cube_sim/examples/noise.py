#!/usr/bin/env python

from cube_sim.application import Application
from cube_sim.shader import Shader
from cube_sim.mesh_view import MeshView
from cube_sim.camera import Camera
from cube_sim.vbo import VBO
from cube_sim.led_cube import LEDCube

import OpenGL.GL as GL
import pygame as pg
import numpy as np
import glm

class Noise(Application):
    def __init__(self):
        super().__init__(1280, 720, 60, 64)
        self.life = 0.0
        self.noise_shader = Shader('noise.vert', 'simplex_noise.frag')

        self.vpos = np.repeat(self.led_cube.sphere_positions[::6], 6, axis=0)
        GL.glBindVertexArray(self.led_cube.mesh.vao)
        self.vbo = VBO(GL.GL_ARRAY_BUFFER, GL.GL_DYNAMIC_DRAW)
        self.vbo.data(self.vpos.nbytes, self.vpos)
        self.vbo.set_slot(3, 3)

        self.noise_scale = 1.0
        self.noise_speed = 1.0

    def handleEvent(self, event):
        if (event.type == pg.KEYDOWN and event.key == pg.K_r):
            self.noise_scale += 0.1  
        if (event.type == pg.KEYDOWN and event.key == pg.K_f):
            self.noise_scale -= 0.1
        if (event.type == pg.KEYDOWN and event.key == pg.K_t):
            self.noise_speed += 0.1  
        if (event.type == pg.KEYDOWN and event.key == pg.K_g):
            self.noise_speed -= 0.1

    def update(self, dt):
        self.life += dt * self.noise_speed
        self.led_cube.rotateAngleAxis(dt * 0.1, glm.vec3(0, 0, 1))
    
    def render(self):
        self.noise_shader.bind()
        self.noise_shader.setUniform1f("time", self.life)
        self.noise_shader.setUniform1f("scale", self.noise_scale)
        MeshView(self.led_cube, self.noise_shader, self.camera).render(True, False)
        MeshView(self.led_cube, self.shader, self.camera).render(False, self.wireframe)

if __name__ == "__main__":
    app = Noise()
    app.run()
    del app
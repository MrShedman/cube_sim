#!/usr/bin/env python

import math
import time
import ctypes
import signal

import pygame as pg
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import numpy as np
import glm

from transform import Transform
from shader import Shader
from camera import Camera
from mesh import Mesh
from mesh_view import MeshView
from sphere import Sphere
from grid import Grid

class Application():
    def __init__(self):
        self.is_open = True
        self.timePerFrame = 1.0 / 60.0
        signal.signal(signal.SIGINT, self.close)
                
        self.rotation = Transform()
        self.camera = Camera()
        self.camera.setPosition(glm.vec3(-3.0, 0.0, 0.0))

        self.shader = Shader('shaders/model.vert', 'shaders/model.frag')

        self.sphere = Sphere(1.0, 16)
        self.sphere.buildFromCube()

        self.grid = Grid()
        self.grid.build()

        self.wireframe = True
        self.cube_state = True

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_STENCIL_TEST)
        GL.glDepthFunc(GL.GL_LEQUAL) # for wireframe rendering
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glLineWidth(1.0)

    def getInput(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.close()
            if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.close()
            if (event.type == pg.KEYDOWN and event.key == pg.K_m):
                self.wireframe = not self.wireframe  
            if (event.type == pg.KEYDOWN and event.key == pg.K_c):
                self.cube_state = not self.cube_state 
                if self.cube_state:
                    self.sphere.makeCube()
                else:
                    self.sphere.makeSphere()          
            if event.type == pg.WINDOWRESIZED:
                GL.glViewport(0, 0, event.dict['x'], event.dict['y'])
            self.camera.handleEvent(event)

    def update(self, dt):
        #self.sphere.rotateAngleAxis(dt * 0.1, glm.vec3(0.0, 1.0, 0.0))
        #self.sphere.rotateAngleAxis(dt * 0.1, glm.vec3(1.0, 0.0, 0.0))

        self.sphere.update()

        self.camera.update(dt)

    def render(self):
        GL.glClearColor(0.2, 0.2, 0.2, 0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        MeshView(self.sphere, self.shader, self.camera).render(True, self.wireframe)
        MeshView(self.grid, self.shader, self.camera).render(True, False, True)

    def run(self):
        timeSinceLastUpdate = 0.0
        lastTime = time.time()
  
        # Start loop
        while self.is_open:
            dt = time.time() - lastTime
            lastTime = time.time()
            timeSinceLastUpdate += dt

            while timeSinceLastUpdate > self.timePerFrame:
                timeSinceLastUpdate -= self.timePerFrame
                self.getInput()
                self.update(self.timePerFrame)

            self.render()
            pg.display.flip()

    def close(self, signum = 0, frame = 0):
        self.is_open = False

if __name__ == "__main__":

    pg.init()

    gl_version = (3, 2)

    pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, gl_version[0])
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, gl_version[1])
    pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)
    pg.display.gl_set_attribute(pg.GL_DOUBLEBUFFER, 1)
    pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
    pg.display.gl_set_attribute(pg.GL_STENCIL_SIZE, 8)

    display_size = (1280, 720)
    pg.display.set_mode(display_size, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
    pg.display.set_caption('led cube simulator')

    app = Application()
    app.run()
    del app

    pg.quit()
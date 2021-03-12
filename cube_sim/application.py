#!/usr/bin/env python

import math
import time
import ctypes
import signal

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import OpenGL.GL as GL
import numpy as np
import glm
from cube_sim.resource import getResource
from cube_sim.camera import CameraFPS, CameraOrbit
from cube_sim.grid import Grid
from cube_sim.led_cube import LEDCube
from cube_sim.shader import Shader
from cube_sim.mesh_view import MeshView

class Application():
    def __init__(self, w = 1280, h = 720, hz = 60, cube_size = 64):
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

        display_size = (w, h)
        pg.display.set_mode(display_size, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        pg.display.set_caption('led cube simulator')
        programIcon = pg.image.load(getResource('icon.png'))
        pg.display.set_icon(programIcon)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_STENCIL_TEST)
        GL.glDepthFunc(GL.GL_LEQUAL) # for wireframe rendering
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glLineWidth(1.0)

        self.is_open = True
        self.timePerFrame = 1/hz
        signal.signal(signal.SIGINT, self.close)

        self.camera = CameraOrbit()
        self.camera.setPosition(glm.vec3(-5.0, 0.0, 1.0))
        #self.camera = CameraFPS()
        #self.camera.setPosition(glm.vec3(-5.0, 0.0, 2.0))
        #self.camera.rotateAngleAxis(math.radians(-15), glm.vec3(0, 1, 0))

        self.shader = Shader('model.vert', 'model.frag')

        self.grid = Grid()
        self.grid.buildMesh()

        self.led_cube = LEDCube(cube_size)
        self.led_cube.buildMesh()
        self.led_cube.buildMeshOutline()
        self.led_cube.setPosition(glm.vec3(0, 0, 1))

        self.wireframe = True
        self.cube_state = True

    def __del__(self):
        pg.quit()

    def handleEvent(self, event):
        pass

    def update(self, dt):
        pass

    def render(self):
        MeshView(self.led_cube, self.shader, self.camera).render(True, self.wireframe)
    
    def priv_handleEvent(self):
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
                    self.led_cube.makeCube()
                else:
                    self.led_cube.makeSphere()
            if event.type == pg.WINDOWRESIZED:
                GL.glViewport(0, 0, event.dict['x'], event.dict['y'])        
            self.camera.handleEvent(event)
            self.handleEvent(event)

    def priv_update(self, dt):
        self.camera.update(dt)
        self.update(dt)

    def priv_render(self):
        MeshView(self.grid, self.shader, self.camera).render(True, False, True)
        self.render()

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
                self.priv_handleEvent()
                self.priv_update(self.timePerFrame)

            GL.glClearColor(0.2, 0.2, 0.2, 0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            self.priv_render()
            pg.display.flip()

    def close(self, signum = 0, frame = 0):
        self.is_open = False
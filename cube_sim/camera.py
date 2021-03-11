#!/usr/bin/env python

from cube_sim.transform import Transform
from math import radians, pi
from time import time
import pygame as pg
import OpenGL.GL as GL
import glm

class Filter():
    def __init__(self, cut_off_hz):
        self.RC = 1.0 / (2.0 * pi * cut_off_hz)
        self.last_update = time()
        self.state = 0.0

    def update(self, input):
        t_now = time()
        dt = t_now - self.last_update
        self.last_update = t_now
        k = dt / (self.RC + dt)
        self.state = self.state + k * (input - self.state)
        return self.state

class Camera(Transform):
    def __init__(self):
        super().__init__()
        self.fov = radians(45.0)
        width, height = pg.display.get_window_size()
        self.aspect = width / height
        self.nearPlaneDistance = 0.1
        self.farPlaceDistance = 100.0
        self.updateProjectionMatrix()
    
    def updateProjectionMatrix(self):
       self.projection = glm.perspective(self.fov, self.aspect, self.nearPlaneDistance, self.farPlaceDistance)

    def getProjectionMatrix(self):
        return self.projection

    def getViewMatrix(self):
        return glm.lookAt(self.position, self.position + self.getForward(), self.getUp())

    def handleEvent(self, event):
        if event.type == pg.WINDOWRESIZED:
            self.aspect = event.dict['x'] / event.dict['y']
            self.updateProjectionMatrix()

    def update(self, dt):
        pass

class CameraOrbit(Camera):
    def __init__(self):
        super().__init__()
        self.mouseClipped = False
        self.mouseMovedThisFrame = False

        self.f_cut = 4.0
        self.xfilter = Filter(self.f_cut)
        self.yfilter = Filter(self.f_cut)

        self.lookVelocity = glm.vec2(0.0, 0.0)
        self.lookAcceleration = glm.vec2(0.0, 0.0)
        self.relativeMouseMotion = glm.vec2(0.0, 0.0)
        self.brake = 0.85

    def isEngaged(self):
        return self.mouseClipped

    def makeEngaged(self):
        self.mouseClipped = True

    def cancelEngaged(self):
        self.mouseClipped = False

    def handleEvent(self, event):
        super().handleEvent(event)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.makeEngaged()
        
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.cancelEngaged()

        if event.type == pg.MOUSEWHEEL:
            self.position += self.getForward() * event.dict['y'] * 0.1
        
        if event.type == pg.MOUSEMOTION and self.isEngaged():
            self.relativeMouseMotion.x, self.relativeMouseMotion.y = event.dict['rel']
            self.mouseMovedThisFrame = True

    def update(self, dt):
        if not self.mouseMovedThisFrame:
            self.relativeMouseMotion.x = 0.0
            self.relativeMouseMotion.y = 0.0
        self.mouseMovedThisFrame = False

        self.lookAcceleration.x = self.xfilter.update(self.relativeMouseMotion.x) * 0.1
        self.lookAcceleration.y = self.yfilter.update(self.relativeMouseMotion.y) * 0.1

        self.lookVelocity += self.lookAcceleration * dt

        self.rotateAroundPoint(self.lookVelocity.y, self.getRight(), glm.vec3(0, 0, 1))
        self.rotateAngleAxis(self.lookVelocity.y, self.getRight())
        self.rotateAroundPoint(self.lookVelocity.x, glm.vec3(0, 0, 1), glm.vec3(0, 0, 1))
        self.rotateAngleAxis(self.lookVelocity.x, glm.vec3(0, 0, 1))

        self.lookVelocity *= self.brake

class CameraFPS(Camera):
    def __init__(self):
        super().__init__()
        self.mouseClipped = False
        self.mouseMovedThisFrame = False

        self.f_cut = 4.0
        self.xfilter = Filter(self.f_cut)
        self.yfilter = Filter(self.f_cut)

        self.lookVelocity = glm.vec2(0.0, 0.0)
        self.lookAcceleration = glm.vec2(0.0, 0.0)
        self.relativeMouseMotion = glm.vec2(0.0, 0.0)
        self.brake = 0.85

    def isEngaged(self):
        return self.mouseClipped

    def makeEngaged(self):
        self.mouseClipped = True
        pg.mouse.set_visible(not self.mouseClipped)
        pg.event.set_grab(self.mouseClipped)

    def cancelEngaged(self):
        self.mouseClipped = False
        pg.mouse.set_visible(not self.mouseClipped)
        pg.event.set_grab(self.mouseClipped)
    
    def handleEvent(self, event):
        super().handleEvent(event)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.makeEngaged()
        
        if event.type == pg.KEYDOWN and (event.key == pg.K_ESCAPE or event.key == pg.K_e):
            self.cancelEngaged()
            w, h = pg.display.get_window_size()
            pg.mouse.set_pos(w / 2, h / 2)

        if event.type == pg.MOUSEWHEEL:
            self.fov = self.fov - radians(event.dict['y'])
            self.updateProjectionMatrix()
        
        if event.type == pg.MOUSEMOTION and self.isEngaged():
            self.relativeMouseMotion.x, self.relativeMouseMotion.y = event.dict['rel']
            self.mouseMovedThisFrame = True
    
    def update(self, dt):
        if not self.mouseMovedThisFrame:
            self.relativeMouseMotion.x = 0.0
            self.relativeMouseMotion.y = 0.0
        self.mouseMovedThisFrame = False

        self.lookAcceleration.x = self.xfilter.update(self.relativeMouseMotion.x) * 0.1
        self.lookAcceleration.y = self.yfilter.update(self.relativeMouseMotion.y) * 0.1

        if self.isEngaged():
            self.lookVelocity += self.lookAcceleration * dt
    
            self.rotateAngleAxis(self.lookVelocity.y, self.getRight())
            self.rotateAngleAxis(self.lookVelocity.x, glm.vec3(0, 0, 1))

        self.lookVelocity *= self.brake

        mult = 1.0
        if pg.key.get_pressed()[pg.K_LSHIFT]:
            mult = 3.0

        if pg.key.get_pressed()[pg.K_LCTRL]:
            mult = 0.33
        
        movAmt = dt * mult

        if pg.key.get_pressed()[pg.K_SPACE]:
            self.position += glm.vec3(0, 0, 1) * movAmt

        if pg.key.get_pressed()[pg.K_w]:
            self.position += self.getForward() * movAmt

        if pg.key.get_pressed()[pg.K_s]:
            self.position -= self.getForward() * movAmt

        if pg.key.get_pressed()[pg.K_a]:
            self.position -= self.getRight() * movAmt

        if pg.key.get_pressed()[pg.K_d]:
            self.position += self.getRight() * movAmt
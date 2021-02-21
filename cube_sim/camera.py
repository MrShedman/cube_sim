#!/usr/bin/env python

from cube_sim.transform import Transform
from math import sin, cos, radians, pi
from time import time
import pygame as pg
import OpenGL.GL as GL
import OpenGL.GLU as GLU
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

class Camera():

    def __init__(self):
        self.mouseClipped = False
        self.mouseMovedThisFrame = False

        self.f_cut = 4.0
        self.xfilter = Filter(self.f_cut)
        self.yfilter = Filter(self.f_cut)

        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.front = glm.vec3(1.0, 0.0, 0.0)
        self.up = glm.vec3(0.0, 0.0, 1.0)
        self.worldUp = glm.vec3(0.0, 0.0, 1.0)

        self.pitch = 0.0
        self.yaw = 0.0

        self.lookVelocity = glm.vec2(0.0, 0.0)
        self.lookAcceleration = glm.vec2(0.0, 0.0)
        self.relativeMouseMotion = glm.vec2(0.0, 0.0)
        self.brake = 0.85

        self.fov = radians(45.0)
        width, height = pg.display.get_window_size()
        self.aspect = width / height

        self.nearPlaneDistance = 0.1
        self.farPlaceDistance = 100.0

        self.updateProjectionMatrix()
        self.updateCameraVectors()

    def getPosition(self):
        return self.position

    def setPosition(self, pos):
        self.position = pos

    def updateProjectionMatrix(self):
       self.projection = glm.perspective(self.fov, self.aspect, self.nearPlaneDistance, self.farPlaceDistance)

    def updateCameraVectors(self):
        # calculate the new Front vector
        front = glm.vec3()
        front.x = cos(self.yaw) * cos(self.pitch)
        front.y = sin(self.yaw) * cos(self.pitch)
        front.z = sin(self.pitch)
        
        self.front = glm.normalize(front)
        # also re-calculate the Right and Up vector
        # normalize the vectors, because their length gets closer to 0 the more you look up or down which results in slower movement.
        self.right = glm.normalize(glm.cross(self.front, self.worldUp))
        self.up    = glm.normalize(glm.cross(self.right, self.front))

    def getViewMatrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def getProjectionMatrix(self):
        return self.projection

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
        if event.type == pg.WINDOWRESIZED:
            self.aspect = event.dict['x'] / event.dict['y']
            self.updateProjectionMatrix()

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

        self.lookAcceleration.x = self.xfilter.update(self.relativeMouseMotion.x) * 0.1
        self.lookAcceleration.y = self.yfilter.update(self.relativeMouseMotion.y) * 0.1

        self.mouseMovedThisFrame = False

        if self.isEngaged():
            self.lookVelocity += self.lookAcceleration * dt
    
            self.pitch -= self.lookVelocity.y
            self.yaw -= self.lookVelocity.x

            pitchLimit = glm.radians(89.0)
            self.pitch = max(-pitchLimit, min(pitchLimit, self.pitch))

        self.lookVelocity *= self.brake
        
        mult = 1.0
        if pg.key.get_pressed()[pg.K_LSHIFT]:
            mult = 3.0

        if pg.key.get_pressed()[pg.K_LCTRL]:
            mult = 0.33
        
        movAmt = dt * mult

        if pg.key.get_pressed()[pg.K_SPACE]:
            self.position += self.up * movAmt

        if pg.key.get_pressed()[pg.K_w]:
            self.position += self.front * movAmt

        if pg.key.get_pressed()[pg.K_s]:
            self.position -= self.front * movAmt

        if pg.key.get_pressed()[pg.K_a]:
            self.position -= self.right * movAmt

        if pg.key.get_pressed()[pg.K_d]:
            self.position += self.right * movAmt

        self.updateCameraVectors() 
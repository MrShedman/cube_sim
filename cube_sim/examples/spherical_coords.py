#!/usr/bin/env python

from cube_sim.application import Application
from cube_sim.transform import Transform
from cube_sim.shader import Shader
from cube_sim.camera import Camera
from cube_sim.mesh import Mesh
from cube_sim.mesh_view import MeshView
from cube_sim.led_cube import LEDCube, Face
from cube_sim.grid import Grid

import pygame as pg
import numpy as np
import glm
import math
import random

MAX_SPEED = 0.0001

def sphere2cartesian(r, theta, phi):
    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)
    return glm.vec3(x, y, z)

def getIndexFromSphereCoords(theta, phi):
    pos = sphere2cartesian(1.0, theta, phi)
    x = pos.x
    y = pos.y
    z = pos.z
    absX = abs(pos.x)
    absY = abs(pos.y)
    absZ = abs(pos.z)
  
    isXPositive = 1 if pos.x > 0 else 0
    isYPositive = 1 if pos.y > 0 else 0
    isZPositive = 1 if pos.z > 0 else 0
  
    # POSITIVE X
    if isXPositive and absX >= absY and absX >= absZ:
        # u (0 to 1) goes from +z to -z
        # v (0 to 1) goes from -y to +y
        maxAxis = absX
        uc = -z
        vc = y
        index = 0

    # NEGATIVE X
    if not isXPositive and absX >= absY and absX >= absZ:
        # u (0 to 1) goes from -z to +z
        # v (0 to 1) goes from -y to +y
        maxAxis = absX
        uc = z
        vc = y
        index = 1
    
    # POSITIVE Y
    if isYPositive and absY >= absX and absY >= absZ:
        # u (0 to 1) goes from -x to +x
        # v (0 to 1) goes from +z to -z
        maxAxis = absY
        uc = x
        vc = -z
        index = 2

    # NEGATIVE Y
    if not isYPositive and absY >= absX and absY >= absZ:
        # u (0 to 1) goes from -x to +x
        # v (0 to 1) goes from -z to +z
        maxAxis = absY
        uc = x
        vc = z
        index = 3

    # POSITIVE Z
    if isZPositive and absZ >= absX and absZ >= absY:
        # u (0 to 1) goes from -x to +x
        # v (0 to 1) goes from -y to +y
        maxAxis = absZ
        uc = x
        vc = y
        index = 4

    # NEGATIVE Z
    if not isZPositive and absZ >= absX and absZ >= absY:
        # u (0 to 1) goes from +x to -x
        # v (0 to 1) goes from -y to +y
        maxAxis = absZ
        uc = -x
        vc = y
        index = 5

    # Convert range from -1 to 1 to 0 to 1
    u = 0.5 * (uc / maxAxis + 1.0)
    v = 0.5 * (vc / maxAxis + 1.0)
    return index, glm.vec2(u, v)

class Particle():
    def __init__(self):
        self.pos = glm.vec2(0, 0)
        self.vel = glm.vec2(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
        self.col = glm.vec3(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
        self.age = 0.0

    def update(self, dt):
        self.pos += self.vel / dt
        self.pos = glm.mod(self.pos, 2.0 * math.pi)
        # self.vel += 
        self.age += dt

class SphericalCoords(Application):
    def __init__(self):
        super().__init__(1280, 720, 60, 64)

        self.particles = []
        for i in range(500):
            self.particles.append(Particle())

    def update(self, dt):
        dims = (self.led_cube.size * self.led_cube.size, 3)
        col_zmin = np.ones(dims).astype(np.float32)
        col_zmax = np.ones(dims).astype(np.float32)
        col_ymin = np.ones(dims).astype(np.float32)
        col_ymax = np.ones(dims).astype(np.float32)
        col_xmin = np.ones(dims).astype(np.float32)
        col_xmax = np.ones(dims).astype(np.float32)

        for p in self.particles:
            p.update(dt)
            face_id, uv_vec = getIndexFromSphereCoords(p.pos.x, p.pos.y)
            uv_vec = glm.floor(uv_vec * self.led_cube.size)
            uv = int(uv_vec.x + uv_vec.y * self.led_cube.size)

            if face_id == 0:
                col_xmax[uv] = p.col
            if face_id == 1:
                col_xmin[uv] = p.col
            if face_id == 2:
                col_ymax[uv] = p.col
            if face_id == 3:
                col_ymin[uv] = p.col
            if face_id == 4:
                col_zmax[uv] = p.col
            if face_id == 5:
                col_zmin[uv] = p.col

        # y and z are flipped around because opengl
        self.led_cube.updateFace(Face.BOTTOM,   col_ymin)
        self.led_cube.updateFace(Face.TOP,      col_ymax)
        self.led_cube.updateFace(Face.RIGHT,    col_zmin)
        self.led_cube.updateFace(Face.LEFT,     col_zmax)
        self.led_cube.updateFace(Face.BACK,     col_xmin)
        self.led_cube.updateFace(Face.FRONT,    col_xmax)
        self.led_cube.update()

        self.led_cube.rotateAngleAxis(dt * 0.1, glm.vec3(0, 0, 1))

if __name__ == "__main__":
    app = SphericalCoords()
    app.run()
    del app
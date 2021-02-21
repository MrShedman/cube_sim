#!/usr/bin/env python

import glm
import numpy as np

from transform import Transform
from mesh import Mesh

class Sphere(Transform):
    def __init__(self, radius, subdivision):
        super().__init__()
        self.radius = radius
        self.subdivision = subdivision
        self.count = 0

    def addVertex(self, x, y, z, normal):
        self.count += 1
        self.mesh.addVertex(x, y, z, normal[0], normal[1], normal[2], normal[0], normal[1], normal[2], 1.0)

    def buildFromCube(self):
        self.mesh = Mesh(6 * 6 * self.subdivision * self.subdivision)

        segments, step = np.linspace(-1, 1, self.subdivision, False, True)

        # Z TOP
        normal = np.array([0.0, 0.0, 1.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step
                self.addVertex(left, top, -1.0, normal)
                self.addVertex(right, bottom, -1.0, normal)
                self.addVertex(right, top, -1.0, normal)

                self.addVertex(left, top, -1.0, normal)
                self.addVertex(left, bottom, -1.0, normal)
                self.addVertex(right, bottom, -1.0, normal)

        # Z BOTTOM
        normal = np.array([0.0, 0.0, -1.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step

                self.addVertex(left, top, 1.0, normal)
                self.addVertex(right, bottom, 1.0, normal)
                self.addVertex(right, top, 1.0, normal)

                self.addVertex(left, top, 1.0, normal)
                self.addVertex(left, bottom, 1.0, normal)
                self.addVertex(right, bottom, 1.0, normal)
    
        # X FRONT
        normal = np.array([1.0, 0.0, 0.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step

                self.addVertex(1.0, left, top, normal)
                self.addVertex(1.0, right, bottom, normal)
                self.addVertex(1.0, right, top, normal)

                self.addVertex(1.0, left, top, normal)
                self.addVertex(1.0, left, bottom, normal)
                self.addVertex(1.0, right, bottom, normal)

        # X BACK
        normal = np.array([-1.0, 0.0, 0.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step

                self.addVertex(-1.0, left, top, normal)
                self.addVertex(-1.0, right, bottom, normal)
                self.addVertex(-1.0, right, top, normal)

                self.addVertex(-1.0, left, top, normal)
                self.addVertex(-1.0, left, bottom, normal)
                self.addVertex(-1.0, right, bottom, normal)

        # Y LEFT
        normal = np.array([0.0, 1.0, 0.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step

                self.addVertex(left, 1.0, top, normal)
                self.addVertex(right, 1.0, bottom, normal)
                self.addVertex(right, 1.0, top, normal)

                self.addVertex(left, 1.0, top, normal)
                self.addVertex(left, 1.0, bottom, normal)
                self.addVertex(right, 1.0, bottom, normal)

        # Y RIGHT
        normal = np.array([0.0, -1.0, 0.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step

                self.addVertex(left, -1.0, top, normal)
                self.addVertex(right, -1.0, bottom, normal)
                self.addVertex(right, -1.0, top, normal)

                self.addVertex(left, -1.0, top, normal)
                self.addVertex(left, -1.0, bottom, normal)
                self.addVertex(right, -1.0, bottom, normal)

        self.mesh.indices = np.linspace(0, len(self.mesh.indices), len(self.mesh.indices), False, dtype=np.uint32)

        for i, colour in enumerate(self.mesh.vertices["colour"]):
            self.mesh.vertices["colour"][i] = np.absolute(colour)

        for i, position in enumerate(self.mesh.vertices["position"]):
            self.mesh.vertices["position"][i] = np.array(glm.normalize(glm.vec3(position)) * self.radius)
            self.mesh.vertices["normal"][i] = np.array(glm.normalize(glm.vec3(position)))

        self.mesh.complete()

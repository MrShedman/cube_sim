#!/usr/bin/env python

import glm
import numpy as np
from enum import IntEnum
from math import sqrt

from cube_sim.transform import Transform
from cube_sim.mesh import Mesh

class Face(IntEnum):
    TOP = 0
    BOTTOM = 1
    FRONT = 2
    BACK = 3
    LEFT = 4
    RIGHT = 5

class LEDCube(Transform):
    def __init__(self, subdivision):
        super().__init__()
        self.subdivision = subdivision
        self.count = 0

    def addVertex(self, x, y, z, normal):
        self.count += 1
        self.mesh.addVertex(x, y, z, normal[0], normal[1], normal[2], normal[0], normal[1], normal[2])

    def update(self):
        length = self.subdivision * self.subdivision
        cols = np.random.uniform(0,1,(length, 3)).astype(np.float32)
        self.updateFace(Face.LEFT, cols)
        self.updateFace(Face.RIGHT, cols)
        self.updateFace(Face.BOTTOM, cols)
        self.mesh.updateColours()

    def updateFace(self, face, colours):
        length = int(len(self.mesh.colours)/6)
        start = int(length*int(face.value))
        end = int(length*(int(face.value)+1))
        self.mesh.colours[start:end] = np.repeat(colours, 6, axis=0)

    def makeCube(self):
        self.mesh.positions = self.cube_positions
        self.mesh.normals = self.cube_normals
        self.mesh.updatePositions()
        self.mesh.updateNormals()

    def makeSphere(self):
        self.mesh.positions = self.sphere_positions
        self.mesh.normals = self.sphere_normals
        self.mesh.updatePositions()
        self.mesh.updateNormals()

    def buildMesh(self):
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

                self.addVertex(left, top, 1.0, normal)
                self.addVertex(right, bottom, 1.0, normal)
                self.addVertex(right, top, 1.0, normal)

                self.addVertex(left, top, 1.0, normal)
                self.addVertex(left, bottom, 1.0, normal)
                self.addVertex(right, bottom, 1.0, normal)

        # Z BOTTOM
        normal = np.array([0.0, 0.0, -1.0])
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

        self.mesh.colours = np.absolute(self.mesh.colours)

        self.cube_positions = self.mesh.positions
        self.cube_normals = self.mesh.normals
        self.sphere_positions = self.mesh.positions / np.linalg.norm(self.mesh.positions, axis=1, keepdims=True) * sqrt(3.0)
        self.sphere_normals = self.mesh.positions

        self.mesh.complete()
#!/usr/bin/env python

import glm
import time
import numpy as np
import OpenGL.GL as GL

from enum import IntEnum
from math import sqrt

from cube_sim.transform import Transform
from cube_sim.mesh import Mesh
from cube_sim.resource import getResource

class Face(IntEnum):
    FRONT = 0
    BACK = 1
    LEFT = 2
    RIGHT = 3
    TOP = 4
    BOTTOM = 5

class LEDCube(Transform):
    def __init__(self, subdivision):
        super().__init__()
        self.subdivision = subdivision
        self.fill_count = 0
        self.outline_count = 0
        self.mesh =         Mesh(self.subdivision * self.subdivision * 6 * 6)
        self.mesh_outline = Mesh(self.subdivision * (self.subdivision + 1) * 4 * 6)
        self.mesh_outline.mode = GL.GL_LINES

    def update(self):
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
        self.mesh_outline.positions = self.cube_outline_positions
        self.mesh_outline.normals = self.cube_outline_normals
        self.mesh_outline.updatePositions()
        self.mesh_outline.updateNormals()

    def makeSphere(self):
        self.mesh.positions = self.sphere_positions
        self.mesh.normals = self.sphere_normals
        self.mesh.updatePositions()
        self.mesh.updateNormals()
        self.mesh_outline.positions = self.sphere_outline_positions
        self.mesh_outline.normals = self.sphere_outline_normals
        self.mesh_outline.updatePositions()
        self.mesh_outline.updateNormals()

    def buildMesh(self):
        filename = 'mesh' + str(self.subdivision) + 'x' + str(self.subdivision) + 'f.npz'
        path = getResource(filename)
        try:
            npzfile = np.load(path)
        except IOError:
            self.generateMesh()
            np.savez(path, positions=self.mesh.positions, normals=self.mesh.normals, colours=self.mesh.colours, indices=self.mesh.indices)
        else:
            self.mesh.positions = npzfile['positions']
            self.mesh.normals = npzfile['normals']
            self.mesh.colours = npzfile['colours']
            self.mesh.indices = npzfile['indices']

        self.cube_positions = self.mesh.positions
        self.cube_normals = self.mesh.normals
        self.sphere_positions = self.mesh.positions / np.linalg.norm(self.mesh.positions, axis=1, keepdims=True) * sqrt(3.0)
        self.sphere_normals = self.mesh.positions

        self.mesh.complete()

    def buildMeshOutline(self):
        filename = 'mesh' + str(self.subdivision) + 'x' + str(self.subdivision) + 'o.npz'
        path = getResource(filename)
        try:
            npzfile = np.load(path)
        except IOError: 
            self.generateMeshOutline()
            np.savez(path, positions=self.mesh_outline.positions, normals=self.mesh_outline.normals, colours=self.mesh_outline.colours, indices=self.mesh_outline.indices)
        else:
            self.mesh_outline.positions = npzfile['positions']
            self.mesh_outline.normals = npzfile['normals']
            self.mesh_outline.colours = npzfile['colours']
            self.mesh_outline.indices = npzfile['indices']
        self.cube_outline_positions = self.mesh_outline.positions
        self.cube_outline_normals = self.mesh_outline.normals
        self.sphere_outline_positions = self.mesh_outline.positions / np.linalg.norm(self.mesh_outline.positions, axis=1, keepdims=True) * sqrt(3.0)
        self.sphere_outline_normals = self.mesh_outline.positions

        self.mesh_outline.complete()

    def generateMesh(self):
        def addVertex(x, y, z, normal):
            self.mesh.addVertex(x, y, z, normal[0], normal[1], normal[2], normal[0], normal[1], normal[2])
            self.fill_count += 1

        segments, step = np.linspace(-1, 1, self.subdivision, False, True)
    
        # X FRONT
        normal = np.array([1.0, 0.0, 0.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step

                addVertex(1.0, left, top, normal)
                addVertex(1.0, right, bottom, normal)
                addVertex(1.0, right, top, normal)

                addVertex(1.0, left, top, normal)
                addVertex(1.0, left, bottom, normal)
                addVertex(1.0, right, bottom, normal)

        # X BACK
        normal = np.array([-1.0, 0.0, 0.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step

                addVertex(-1.0, left, top, normal)
                addVertex(-1.0, right, bottom, normal)
                addVertex(-1.0, right, top, normal)

                addVertex(-1.0, left, top, normal)
                addVertex(-1.0, left, bottom, normal)
                addVertex(-1.0, right, bottom, normal)

        # Y LEFT
        normal = np.array([0.0, 1.0, 0.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step

                addVertex(left, 1.0, top, normal)
                addVertex(right, 1.0, bottom, normal)
                addVertex(right, 1.0, top, normal)

                addVertex(left, 1.0, top, normal)
                addVertex(left, 1.0, bottom, normal)
                addVertex(right, 1.0, bottom, normal)

        # Y RIGHT
        normal = np.array([0.0, -1.0, 0.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step

                addVertex(left, -1.0, top, normal)
                addVertex(right, -1.0, bottom, normal)
                addVertex(right, -1.0, top, normal)

                addVertex(left, -1.0, top, normal)
                addVertex(left, -1.0, bottom, normal)
                addVertex(right, -1.0, bottom, normal)

        # Z TOP
        normal = np.array([0.0, 0.0, 1.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step

                addVertex(left, top, 1.0, normal)
                addVertex(right, bottom, 1.0, normal)
                addVertex(right, top, 1.0, normal)

                addVertex(left, top, 1.0, normal)
                addVertex(left, bottom, 1.0, normal)
                addVertex(right, bottom, 1.0, normal)

        # Z BOTTOM
        normal = np.array([0.0, 0.0, -1.0])
        for i in segments:
            for j in segments:
                top = i
                bottom = i + step
                left = j
                right = j + step
                addVertex(left, top, -1.0, normal)
                addVertex(right, bottom, -1.0, normal)
                addVertex(right, top, -1.0, normal)

                addVertex(left, top, -1.0, normal)
                addVertex(left, bottom, -1.0, normal)
                addVertex(right, bottom, -1.0, normal)

        self.mesh.indices = np.linspace(0, len(self.mesh.indices), len(self.mesh.indices), False, dtype=np.uint32)
        self.mesh.colours = np.absolute(self.mesh.colours)

    def generateMeshOutline(self):
        def addVertex(x, y, z, normal):
            self.mesh_outline.addVertex(x, y, z, normal[0], normal[1], normal[2], 0.0, 0.0, 0.0)
            self.outline_count += 1

        extent = 1
        interval = 2 / (self.subdivision + 1)
        segments = np.linspace(-extent, extent, int((extent+1) / interval), True)

        # Z TOP and BOTTOM
        normal = np.array([0.0, 0.0, 1.0])
        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(n1, c, extent, normal)
                addVertex(n2, c, extent, normal)
                addVertex(c, n1, extent, normal)
                addVertex(c, n2, extent, normal)
                addVertex(n1, c, -extent, -normal)
                addVertex(n2, c, -extent, -normal)
                addVertex(c, n1, -extent, -normal)
                addVertex(c, n2, -extent, -normal)

        # X FRONT and BACK
        normal = np.array([1.0, 0.0, 0.0])
        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(extent, n1, c, normal)
                addVertex(extent, n2, c, normal)
                addVertex(extent, c, n1, normal)
                addVertex(extent, c, n2, normal)
                addVertex(-extent, n1, c, -normal)
                addVertex(-extent, n2, c, -normal)
                addVertex(-extent, c, n1, -normal)
                addVertex(-extent, c, n2, -normal)

        # Y LEFT and RIGHT
        normal = np.array([0.0, 1.0, 0.0])
        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(n1, extent, c, normal)
                addVertex(n2, extent, c, normal)
                addVertex(c, extent, n1, normal)
                addVertex(c, extent, n2, normal)
                addVertex(n1, -extent, c, -normal)
                addVertex(n2, -extent, c, -normal)
                addVertex(c, -extent, n1, -normal)
                addVertex(c, -extent, n2, -normal)

        self.mesh_outline.indices = np.linspace(0, len(self.mesh_outline.indices), len(self.mesh_outline.indices), False, dtype=np.uint32)
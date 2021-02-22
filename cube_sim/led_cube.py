#!/usr/bin/env python

import glm
import numpy as np
import OpenGL.GL as GL

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
        self.fill_count = 0
        self.outline_count = 0

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
        def addVertex(x, y, z, normal):
            self.mesh.addVertex(x, y, z, normal[0], normal[1], normal[2], normal[0], normal[1], normal[2])
            self.fill_count += 1

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

        self.mesh.indices = np.linspace(0, len(self.mesh.indices), len(self.mesh.indices), False, dtype=np.uint32)

        self.mesh.colours = np.absolute(self.mesh.colours)

        self.cube_positions = self.mesh.positions
        self.cube_normals = self.mesh.normals
        self.sphere_positions = self.mesh.positions / np.linalg.norm(self.mesh.positions, axis=1, keepdims=True) * sqrt(3.0)
        self.sphere_normals = self.mesh.positions

        self.mesh.complete()

    def buildMeshOutline(self):
        def addVertex(x, y, z, normal):
            self.mesh_outline.addVertex(x, y, z, normal[0], normal[1], normal[2], 0.0, 0.0, 0.0)
            self.outline_count += 1

        extent = 1
        interval = 2 / (self.subdivision + 1)
        segments = np.linspace(-extent, extent, int((extent+1) / interval), True)
        fc = extent
        self.mesh_outline = Mesh(len(segments) * (len(segments)-1) * 4 * 6)
        self.mesh_outline.mode = GL.GL_LINES

        # Z TOP
        normal = np.array([0.0, 0.0, 1.0])
        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(n1, c, fc, normal)
                addVertex(n2, c, fc, normal)

        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(c, n1, fc, normal)
                addVertex(c, n2, fc, normal)

        # Z BOTTOM
        normal = np.array([0.0, 0.0, -1.0])
        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(n1, c, -fc, normal)
                addVertex(n2, c, -fc, normal)

        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(c, n1, -fc, normal)
                addVertex(c, n2, -fc, normal)

        # X FRONT
        normal = np.array([1.0, 0.0, 0.0])
        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(fc, n1, c, normal)
                addVertex(fc, n2, c, normal)

        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(fc, c, n1, normal)
                addVertex(fc, c, n2, normal)

        # X BACK
        normal = np.array([-1.0, 0.0, 0.0])
        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(-fc, n1, c, normal)
                addVertex(-fc, n2, c, normal)

        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(-fc, c, n1, normal)
                addVertex(-fc, c, n2, normal)

        # Y LEFT
        normal = np.array([0.0, 1.0, 0.0])
        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(n1, fc, c, normal)
                addVertex(n2, fc, c, normal)

        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(c, fc, n1, normal)
                addVertex(c, fc, n2, normal)

        # Y RIGHT
        normal = np.array([0.0, -1.0, 0.0])
        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(n1, -fc, c, normal)
                addVertex(n2, -fc, c, normal)

        for c in segments:
            for n1, n2 in zip(segments, segments[1:]):
                addVertex(c, -fc, n1, normal)
                addVertex(c, -fc, n2, normal)

        self.mesh_outline.indices = np.linspace(0, len(self.mesh_outline.indices), len(self.mesh_outline.indices), False, dtype=np.uint32)

        self.cube_outline_positions = self.mesh_outline.positions
        self.cube_outline_normals = self.mesh_outline.normals
        self.sphere_outline_positions = self.mesh_outline.positions / np.linalg.norm(self.mesh_outline.positions, axis=1, keepdims=True) * sqrt(3.0)
        self.sphere_outline_normals = self.mesh_outline.positions

        self.mesh_outline.complete()
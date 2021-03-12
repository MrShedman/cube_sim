#!/usr/bin/env python

import glm

class Transform():

    def __init__(self):
        self.reset()

    def reset(self):
        self.origin = glm.vec3()
        self.position = glm.vec3()
        self.scale = glm.vec3(1.0, 1.0, 1.0)
        self.rotation = glm.quat(1.0, 0.0, 0.0, 0.0)
        self.transform = glm.mat4(1.0)
        self.inv_transform = glm.mat4(1.0)
        self.transform_dirty = True
        self.inv_transform_dirty = True

    def setPosition(self, pos):
        self.position = pos
        self.transform_dirty = True
        self.inv_transform_dirty = True

    def move(self, offset):
        self.setPosition(self.position + offset)

    def setRotation(self, rotation):
        self.rotation = glm.normalize(rotation)
        self.transform_dirty = True
        self.inv_transform_dirty = True

    def setRotationAngleAxis(self, angle, axis):
        rot = glm.angleAxis(angle, glm.normalize(axis))
        self.setRotation(rot)

    def rotate(self, rotation):
        self.setRotation(self.rotation * rotation)

    def rotateAngleAxis(self, angle, axis):
        rot = glm.angleAxis(angle, glm.normalize(axis))
        self.setRotation(self.rotation * rot)

    def rotateAroundPoint(self, angle, axis, pivot):
        rot = glm.angleAxis(angle, glm.normalize(axis))
        vec = self.position - self.origin - pivot
        self.setPosition(pivot + vec * rot + self.origin)

    def setScale(self, factor):
        self.scale = factor
        self.transform_dirty = True
        self.inv_transform_dirty = True

    def setOrigin(self, origin):
        self.origin = origin
        self.transform_dirty = True
        self.inv_transform_dirty = True

    def getPosition(self):
        return self.position

    def getRotation(self):
        return self.rotation

    def getScale(self):
        return self.scale
    
    def getOrigin(self):
        return self.origin

    def getUp(self):
        return glm.vec3(0, 0, 1) * self.getRotation()

    def getDown(self):
        return glm.vec3(0, 0, -1) * self.getRotation()

    def getLeft(self):
        return glm.vec3(0, 1, 0) * self.getRotation()

    def getRight(self):
        return glm.vec3(0, -1, 0) * self.getRotation()

    def getForward(self):
        return glm.vec3(1, 0, 0) * self.getRotation()

    def getBack(self):
        return glm.vec3(-1, 0, 0) * self.getRotation()

    def getTransform(self):
        if self.transform_dirty:
            translationMat = glm.translate(glm.mat4(1.0), self.position - self.origin)
            scaleMat = glm.scale(glm.mat4(1.0), self.scale)
            rotationMat = glm.mat4_cast(self.rotation)

            self.transform = translationMat * rotationMat * scaleMat
            self.transform_dirty = False
        return self.transform
    
    def getInverseTransform(self):
        if self.inv_transform_dirty:
            self.inv_transform = glm.inverse(self.getTransform())
            self.inv_transform_dirty = False
        return self.inv_transform
#!/usr/bin/env python

import colorsys
import random
import numpy as np

def genRandomRGB():
    r = random.uniform(0, 1)
    g = random.uniform(0, 1)
    b = random.uniform(0, 1)
    return np.array(r, g, b)

def genRandomStrongColour():
    hue = random.uniform(0, 1)
    return np.array(colorsys.hsv_to_rgb(hue, 1.0, 1.0))

def fadeColour(colour, fade=0.99):
    h, s, v = colorsys.rgb_to_hsv(colour[0], colour[1], colour[2])
    v *= fade
    return np.array(colorsys.hsv_to_rgb(h, s, v))
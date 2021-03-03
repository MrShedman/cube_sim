#!/usr/bin/env python

import colorsys
import random

def genRandomRGB():
    r = random.uniform(0, 1)
    g = random.uniform(0, 1)
    b = random.uniform(0, 1)
    r, g, b

def genRandomStrongColour():
    hue = random.uniform(0, 1)
    return colorsys.hsv_to_rgb(hue, 1.0, 1.0)
#!/usr/bin/env python

from pathlib import Path

def getResource(resource):
    here = Path(__file__).parent.parent
    fname = here/'res'/resource
    return fname
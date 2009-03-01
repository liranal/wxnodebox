#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

#from PathElement import *
from math import pi

CENTER = "center"
CORNER = "corner"

class Transform():
    """
    WxNodebox implementation of NodeBox drawing state
    """
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = 0.
        self.y = 0.
        self.radians = 0.
        self.mode = CENTER
        # CENTER or CORNER
    
    def transform( self, mode = CENTER):
        self.mode = mode
        
    def translate( self, x, y):
        self.x += x
        self.y += y
    
    def rotate( self, degrees = 0, radians = 0):
        if degrees != 0 and radians != 0:
            # error !!!
            pass
        if degrees != 0:
            self.radians += degrees * pi / 180.
        elif radians != 0:
            self.radians += radians

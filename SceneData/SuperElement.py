#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

# story of Doom : http://doom.wikia.com/wiki/Entryway
# http://diablo2.judgehype.com/index.php

from euclid import *
from Element import *

class MovingElement(Element):
    def __init__(self):
        Element.__init__(self)
        self.position = Point2(0.,0.)
        self.direction = 0.
        self.size = 0.5
        self.state = 1
        self.speed = 0.
        self.angle = 0.
        self.aim = Point2(0.,0.)
        
class StaticElement(Element):
    def __init__(self):
        Element.__init__(self)
        self.position = Point2(0.,0.)
        self.direction = 0.
        self.size = 1.
        self.state = 1

class Creature(MovingElement):
    def __init__(self):
        """
        Initialize monster attribs
        position :
        direction :
        speed : 
        state :
        aim : object that he wants to get
        ##history_position :
        """
        MovingElement.__init__(self)

class Actor(MovingElement):
    def __init__(self):
        MovingElement.__init__(self)
        self.angle_pref = 1.
        
    
#if __name__ == '__main__':
#    print 'start test'
#    print 'end test'

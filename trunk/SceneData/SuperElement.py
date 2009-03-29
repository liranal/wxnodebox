#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

# story of Doom : http://doom.wikia.com/wiki/Entryway
# http://diablo2.judgehype.com/index.php

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


class MovingElement(Element):
    def __init__(self):
        Element.__init(self)
        self.position = Vector2(0.,0.)
        self.direction = 0.
        self.state = 1
        self.speed = 0.
        
class StaticElement(Element):
    def __init__(self):
        Element.__init(self)
        self.position = Vector2(0.,0.)
        self.direction = 0.
        self.state = 1

class Actor(MovingElement):
    def __init__(self):
        MovingElement.__init__(self)
        
    
#if __name__ == '__main__':
#    print 'start test'
#    print 'end test'

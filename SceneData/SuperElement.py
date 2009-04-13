#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

# story of Doom : http://doom.wikia.com/wiki/Entryway
# http://diablo2.judgehype.com/index.php

from euclid import *
from Element import *

class MovingElement(Element):
    def __init__(self):
        Element.__init__(self)
        self.position = Point2(0,0)
        self.direction = 0.
	self.size = Vector2(10,10)
        self.state = 1
        self.speed = 0.
        self.angle = 0.
        self.aim = Point2(0,0)
	self.past_increment = None
        
    def find_increment(self):
        ## actor.increments = [ Vector2(), ... ]
	increment = Vector2(0,0)
	vector = self.aim - self.position
	if vector.x == 0 and vector.y == 0:
	    return increment
        if len(self.increments) == 0:
	    # define increment vector
	    if abs(vector.x) >= abs(vector.y):
		if vector.x > 0:
		    increment.x = 1
		else:
		    increment.x = -1
	    else:
		if vector.y > 0:
		    increment.y = 1
		else:
		    increment.y = -1
	    if self.past_increment != None and self.past_increment == -1 * increment:
		old_increment = increment
		increment = Vector2(0,0)
		if old_increment.x != 0:
		    # we have to increment in y
		    if vector.y >=0:
			increment.y = 1
		    else:
			increment.y = -1
		else:
		    # we have to increment in x
		    if vector.x >=0:
			increment.x = 1
		    else:
			increment.x = -1
	else:
	    # find a way
	    tries_number = len(self.increments)
	    if tries_number == 1:
		old_increment = self.increments[0]
		if self.past_increment != None and self.past_increment != old_increment:
		    increment = self.past_increment
		elif old_increment.x != 0:
		    # we have to increment in y
		    if vector.y >=0:
			increment.y = 1
		    else:
			increment.y = -1
		else:
		    # we have to increment in x
		    if vector.x >=0:
			increment.x = 1
		    else:
			increment.x = -1
	    elif tries_number == 2:
		if self.past_increment != None and self.past_increment == self.increments[1]:
		    increment = -1 * self.increments[0]
		else:
		    old_increment = self.increments[1]
		    if old_increment.x != 0:
			# we have to increment in opposite x
			increment.x = old_increment.x * -1
		    else:
			# we have to increment in opposite y
			increment.y = old_increment.y * -1
	    elif tries_number == 3:
		if self.past_increment != None and self.past_increment == self.increments[1]:
		    increment = -1 * self.past_increment
		else:
		    # we have to increment in opposite [0]
		    increment = -1 * self.increments[0]
	return increment
	
class StaticElement(Element):
    def __init__(self):
        Element.__init__(self)
        self.position = Point2(0,0)
        self.direction = 0.
        self.size = 10
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
	self.life = 10

class Actor(MovingElement):
    def __init__(self):
        MovingElement.__init__(self)
	self.status = None
        
    def manage_collision(self, new_position, collision, events_manager):
	pass
	
class Bullet(MovingElement):
    def __init__(self, actor):
        MovingElement.__init__(self)
	#self.status = None
	self.position = actor.position + actor.size/2
	self.size = Vector2(1,1)
	self.aim = actor.gunfire_aim
	self.speed = 1000
	self.strength = 3

    def manage_collision(self, new_position, collision, events_manager):
	if isinstance(collision.element, Creature):
	    # event
	    event = events_manager.create_event( "GUNFIRE_IMPACT")
	    event.impact = collision.element
	    event.bullet = self
	
    def find_increment(self):
	pass
    
    
#if __name__ == '__main__':
#    print 'start test'
#    print 'end test'

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

    def __repr__(self):
        return 'MovingElement(id=%d, name=%s, position=%r, direction=%.2f, size=%r, state=%d, speed=%.2f, angle=%.2f, aim=%r, past_increment=%r)' \
               % (self.id, self.name, self.position, self.direction, self.size, self.state, self.speed, self.angle, self.aim, self.past_increment)

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

    def __repr__(self):
        return 'StaticgElement(id=%d, name=%s, position=%r, direction=%.2f, size=%r, state=%d)' \
               % (self.id, self.name, self.position, self.direction, self.size, self.state)


class Creature(MovingElement):
    
    status_acts = {}
    
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
	self.status = 'move'
	# movement algo
	self.increments = []
	self.moving_increments = [] # 2 elements max
	self.increments_count = 0
	self.increments_maxcount = 300

    def __repr__(self):
        return 'Creature(id=%d, name=%s, position=%r, direction=%.2f, size=%r, state=%d, speed=%.2f, angle=%.2f, aim=%r, past_increment=%r, life=%d)' \
               % (self.id, self.name, self.position, self.direction, self.size, self.state, self.speed, self.angle, self.aim, self.past_increment, self.life)

    physics = None
    
    def connect_physics(self, physicsengine):
	Creature.physics = physicsengine
    
    def act(self):
	self.status_acts[self.status](self)
    
    def act_wait(self):
	pass
	
    def act_move(self):
	self.physics.world.remove_element( self)
	self.aim = self.physics.world.actor.position
	movement = self.speed
	self.increments = list(self.moving_increments)
	count = 0
	while movement > 0 and count < 4:
	    count += 1
	    vector = self.aim - self.position
	    increment = self.find_increment()
	    ## TODO : dans le cas d'aucune direction possible
	    if increment.x == 0 and increment.y == 0:
		if vector.x == 0 and vector.y == 0:
		    break
		else:
		    if len(self.increments) > 0:
			self.increments = self.increments[1:]
			if len(self.moving_increments) > 0:
			    self.moving_increments = self.moving_increments[1:]
		    continue
	    # new position
	    self.new_position = self.position + increment
	    # check position
	    collisions_list = self.physics.simpleraymapping.update_collisions( self)
	    #for element in collisions_list:
	    if len(collisions_list) == 0:
		self.position = self.new_position
		##self.past_increment = increment
		back = -increment
		## TODO
		#if len(self.moving_increments) == 2 and self.moving_increments[-1] != back:
		if len(self.moving_increments) == 2:
		    # changement de direction
		    # si les directions interdites sont les deux directions attractives alors
		    # on supprime la dernière
		    def_increments = self.define_increments( vector)
		    ## TODO les - sont superflux
		    if (self.moving_increments[0] == def_increments[0] and self.moving_increments[1] == def_increments[1]) or \
		       (self.moving_increments[0] == def_increments[1] and self.moving_increments[1] == def_increments[0]):
			self.moving_increments = [ self.moving_increments[1] ]
		    
		##self.increments = [ back ]
		if len(filter( lambda x: x==back, self.moving_increments)) == 0:
		    if len(self.moving_increments) == 2:
			self.moving_increments = [ self.moving_increments[1], back]
		    else:
			self.moving_increments.append( back)
		else:
		    self.moving_increments = filter( lambda x: x!=back, self.moving_increments)
		    self.moving_increments.append( back)
		movement -= 1
		count = 0
		self.increments_count += 1
		if self.increments_count >= self.increments_maxcount:
		    self.increments_count = 0
		    if len(self.moving_increments) == 2:
			self.moving_increments=[self.moving_increments[1]]
		    else:
			self.moving_increments=[]
		self.increments = list(self.moving_increments)
	    else:
		self.increments_count = 0
		self.increments += [ increment ]
		if len(self.increments) >= 4:
		    self.increments = self.increments[1:]
		    if len(self.moving_increments) >= 4:
			self.moving_increments = self.moving_increments[1:]
	# end while
	self.physics.world.add_element( self)
	# specific creature actions
	##if abs( self.physics.world.actor.position - self.position) < 20:
	##    self.status = 'dead'
	##   self.act()
	##    #gworld.remove_element( self)
	##    #self.position = Point2(621.00, 48.00)
	##    #gworld.add_element( self)
	
    def act_hurt(self):
	bullet = self.impact
	self.life -= bullet.strength
	self.status = 'move'
	if self.life < 0:
	    self.status = 'dead'
    
    def act_dead(self):
	#self.physics.world.remove_element( self)
	pass
	
    #status_acts = { 'wait':Creature.act_wait, 'move':Creature.act_move, 'dead':Creature.act_dead}
    status_acts = { 'wait':act_wait, 'move':act_move, 'hurt':act_hurt, 'dead':act_dead}

    def define_increments(self, vector):
	if vector.y == 0:
	    if vector.x > 0:
		l_increments =  [ Vector2(1,0), Vector2(0,1), Vector2(0,-1), Vector2(-1,0) ]
	    else:
		l_increments =  [ Vector2(-1,0), Vector2(0,-1), Vector2(0,1), Vector2(1,0) ]
	elif vector.x == 0:
	    if vector.y > 0:
		l_increments =  [ Vector2(0,1), Vector2(1,0), Vector2(-1,0), Vector2(0,-1) ]
	    else:
		l_increments =  [ Vector2(0,-1), Vector2(-1,0), Vector2(1,0), Vector2(0,1) ]
	else:
	    # le cas classique
	    l_increments = []
	    gradient = abs(vector.x / vector.y)
	    if gradient >= 1:
		# direction = x
		if vector.x > 0:
		    l_increments.append( Vector2(1,0))
		else:
		    l_increments.append( Vector2(-1,0))
		if vector.y > 0:
		    l_increments.append( Vector2(0,1))
		else:
		    l_increments.append( Vector2(0,-1))
	    else:
		# direction = y
		if vector.y > 0:
		    l_increments.append( Vector2(0,1))
		else:
		    l_increments.append( Vector2(0,-1))
		if vector.x > 0:
		    l_increments.append( Vector2(1,0))
		else:
		    l_increments.append( Vector2(-1,0))
	    l_increments.append( - l_increments[1])
	    l_increments.append( - l_increments[0])
	return l_increments
    
    def find_increment(self):
        ## actor.increments = [ Vector2(), ... ]
        increment = Vector2(0,0)
        vector = self.aim - self.position
        if vector.x == 0 and vector.y == 0:
            return increment
	l_increments = self.define_increments( vector)
	if len(self.increments)==4:
	    return increment
	find = False
	index = 0
	while find == False:
	    increment = l_increments[index]
	    if len(filter( lambda x: x==increment, self.increments)) == 0:
		find = True
	    else:
		index += 1
	return increment
    
    
class Actor(MovingElement):
    ##status_list = ( 'wait', 'walk1', 'walk2', 'walk3', 'fire1', 'fire2', 'hurt', 'dead')
    status_list = ( 'wait', 'walk', 'fire', 'hurt', 'dead')
    
    def __init__(self):
        MovingElement.__init__(self)
        self.status = 'wait'
	
    def manage_collision(self, new_position, collision):
	pass

    def __repr__(self):
        return 'Actor(id=%d, name=%s, position=%r, direction=%.2f, size=%r, state=%d, speed=%.2f, angle=%.2f, aim=%r, past_increment=%r, status=%r)' \
               % (self.id, self.name, self.position, self.direction, self.size, self.state, self.speed, self.angle, self.aim, self.past_increment, self.status)

    physics = None
    
    def connect_physics(self, physicsengine):
	Actor.physics = physicsengine
    
    def act(self):
	self.status_acts[self.status](self)
	
    def act_wait(self):
	pass
    
    def act_fire(self):
        """status='fire'"""
	self.speed = 0
	self.status = 'wait'
	bullet = Bullet( self)
	bullet.connect_physics( self.physics)
	bullet.act()
	
    def act_move(self):
	#self.physics.raymapping.move_element( self)
	if self.speed <= 0:
	    return
	movement = self.speed
	vector = self.aim - self.position
	new_vector = movement * vector.normalized()
	if abs(vector) > abs(new_vector):
		vector = new_vector
	(new_position, collision) = self.physics.raymapping.update_element_position( self, vector)
	old_position = self.position.copy()
	self.position.x = int(new_position.x)
	self.position.y = int(new_position.y)
	if collision == None:
	    return
	real_vector = self.position - old_position
	if vector.x != 0:
	    dt = 1 - real_vector.x / vector.x
	else:
	    dt = 1 - real_vector.y / vector.y
	size_diff = (collision.element.size + self.size) / 2.
	pos_diff = collision.element.position - self.position
	chooseWay = True
	if abs(pos_diff.x) < size_diff.x:
	    new_vector = Vector2( dt * vector.x,0)
	else:
	    new_vector = Vector2( 0, dt * vector.y)
	    if abs(pos_diff.y) >= size_diff.y:
		# we have to try 2 ways !!
		chooseWay = False
	(new_position, collision) = self.physics.raymapping.update_element_position( self, new_vector)
	if chooseWay == False and new_position == self.position:
	    new_vector = Vector2( dt * vector.x,0)
	    (new_position, collision) = self.physics.raymapping.update_element_position( self, new_vector)
	# new position
	self.position.x = int(new_position.x)
	self.position.y = int(new_position.y)
	##actor.manage_collision( new_position, collision)
	## update status
	if old_position == self.position:
	    self.status='wait'
	
	
    status_acts = { 'wait':act_wait, 'move':act_move, 'fire':act_fire}
    

	
class Bullet(MovingElement):
    status_list = ( 'move', 'explode')
    def __init__(self, actor):
        MovingElement.__init__(self)
        #self.status = None
        self.position = actor.position + actor.size/2
        self.size = Vector2(1,1)
        self.aim = actor.gunfire_aim
        self.speed = 1000
        self.strength = 3
	self.status = 'move'

    def __repr__(self):
        return 'Actor(id=%d, name=%s, position=%r, direction=%.2f, size=%r, state=%d, speed=%.2f, angle=%.2f, aim=%r, past_increment=%r, strength=%r)' \
               % (self.id, self.name, self.position, self.direction, self.size, self.state, self.speed, self.angle, self.aim, self.past_increment, self.strength)

    def manage_collision(self, new_position, collision):
        if collision == None:
            return
        if isinstance(collision.element, Creature):
	    creature = collision.element
	    creature.status = 'hurt'
	    creature.impact = self
	    #creature.act()
	    #event = events_manager.create_event( "GUNFIRE_IMPACT")
            #event.impact = collision.element
            #event.bullet = self
	self.status = 'impact'

    def find_increment(self):
        pass

    physics = None
    
    def connect_physics(self, physicsengine):
	Bullet.physics = physicsengine
    
    def act(self):
	self.status_acts[self.status](self)

    def act_move(self):
	self.physics.raymapping.move_element( self)
	
    def act_impact(self):
	pass
    
    status_acts = { 'move':act_move, 'impact':act_impact}

	
#if __name__ == '__main__':
#    print 'start test'
#    print 'end test'

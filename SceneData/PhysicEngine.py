#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

import math
from euclid import *

from copy import copy
from threading import Thread

from World import *
from EventsManager import *

X = 0
Y = 1

class PhysicEngine:
	def __init__(self, world, events_manager):
		assert isinstance(world, World)
		assert isinstance(events_manager, EventsManager)
		self.world = world
		self.events_manager = events_manager
		self.raymapping = Raymapping( world, events_manager)
		self.simpleraymapping = SimpleAlgoRaymapping( world)
		self.time = 0
		#global gengine

	def connect(self):
		self.world.actor.connect_physics( self)
		for creature in self.world.creatures_list:
			creature.connect_physics(self)

	def read_events(self):
		"""extern events"""
		events = self.events_manager.events
		while len(events) != 0:
			event = events.pop()
			if event.subject == 'ACTOR_AIM':
				actor = self.world.actor
				# update actor aim
				actor.aim = actor.position + event.aim
				# update actor speed
				actor.speed = 5
				# status
				actor.status = 'move'
				## update actor angle
				##actor.angle = math.atan2( event.aim.y, event.aim.x)
			if event.subject == 'ACTOR_GUNFIRE':
				actor = self.world.actor
				# update actor aim
				actor.gunfire_aim = actor.position + event.aim
				# update actor speed
				actor.status = 'fire'
			##if event.subject == 'GUNFIRE_IMPACT':
				##impact = event.impact
				##bullet = event.bullet
				#### lost life point
				##impact.life -= bullet.strength
				##impact.speed = 0
				##if impact.life <= 0:
					##impact.status = 'DEAD'
					### event
					##event = self.events_manager.create_event( "KILLED")
					##event.killed = impact
			##if event.subject == 'KILLED':
				##x = event.killed

	def turn(self):
		# delta time of the turn
		self.time += 1
		# read events
		self.read_events()
		# move actor
		self.world.actor.act()
		# move creature
		creatures_list = self.world.creatures_list
		for creature in creatures_list:
			creature.act()
				
				
## TODO
## il faut réfléchir à remplacer le isHorizontal et isVertical par une valeur faible mais non null de direction_vect

class Raymapping:
	""" algorithme de raymapping pour déterminer les collisions entre éléments.
	Cette algo retourne
	>> main procedure : def calculate_collision()
	"""
	def __init__(self, world, events_manager):
		self.world = world
		self.area_size = self.world.area_size
		self.events_manager = events_manager

		
	def move_element(self, actor):
		if actor.speed <= 0:
			return
		movement = actor.speed
		vector = actor.aim - actor.position
		new_vector = movement * vector.normalized()
		if abs(vector) > abs(new_vector):
			vector = new_vector
		(new_position, collision) = self.update_element_position( actor, vector)
		# new position
		actor.manage_collision( new_position, collision)
		
		
	def update_element_position(self, actor, direction_vector):
		'''MAIN PROCEDURE : Recherche si elle existe la collision entre un élément mouvant et son environnement
		moving_element = MovingElement()
		direction_vect = Vector2()
		world = World()
		return = ( element_position, collision)
		NO --> Exit > moving_element.position is updated'''
		# initialize direction
		direction = self.define_direction( direction_vector)
		isRight, isUp, isHorizontal, isVertical = direction
		# init delta time
		dt0 = 0
		# find corner
		g_to_corner = Vector2( actor.size.x * int(isRight), \
							   actor.size.y * int(isUp) )
		element_position = actor.position.copy()
		path = direction_vector.copy()

		area_next_collisions_list = []
		#########################################################
		while dt0 < 1.:
			# corner point coordinate
			corner_point = element_position + g_to_corner
			# areas borders
			areas_bounds = self.define_areas_box( element_position, actor.size)
			areas_to_check = self.select_areas_to_check( areas_bounds, direction)

			# prepare futur next area (and get max dt1)
			next_area_collision = self.calculate_next_area( areas_bounds, direction, corner_point, path)
			dt1 = min( next_area_collision[2], 1.)
			dt0 = 0.

			# get collision in this area group
			collisions_list = self.calculate_actor_collisions \
							( corner_point, direction, path, (dt0, dt1), \
							  actor.size, areas_to_check)

			# if no collision, go to the next position
			if len(collisions_list) == 0:
				# move_element to the next area
				dt0 = dt1
				element_position = element_position + dt0 * path
				path = (1 - dt0) * path
				collision = None
			else:
				# if collision, select the dt minus one
				collision = reduce(lambda x,y: min(x,y, lambda c: c.dt), collisions_list)
				element_position = Point2(collision.x, collision.y) - g_to_corner
				dt0=1.
		#########################################################
		# stop of the moving element
		# update element position
		##moving_element.position = element_position
		return (element_position, collision)
	
	
	def define_direction(self, direction_vector):
		""" Définit la direction au format boolean à partir d'un vecteur:
		direction_vector = Vector2()
		return = (isRight, isUp, isHorizontal, isVertical) = (boolean, boolean, boolean, boolean)
		"""
		##isRight, isUp, isHorizontal, isVertical = False, False, False, False
		isRight = (direction_vector.x > 0.)
		isUp = (direction_vector.y > 0.)
		isHorizontal = (direction_vector.y == 0.)
		isVertical = (direction_vector.x == 0.)
		return (isRight, isUp, isHorizontal, isVertical)

	
	def define_areas_box(self, element_position, element_size):
		"""Calcule les coordonnées des deux zones extrêmes contenant l'élément (la zone min et la zone max)
		element_position = Point2()
		element_size = float
		return = ( (indexXmin, indexYmin), (indexXmax, indexYmax))
		"""
		return ( ( int((element_position.x-1)              / self.area_size),   \
				   int((element_position.y-1)              / self.area_size) ), \
				 ( int((element_position.x+element_size.x) / self.area_size), \
				   int((element_position.y+element_size.y) / self.area_size)  ) )	
	
	
	def select_areas_to_check(self, areas_box, direction):
		"""Détermine la liste des coordonnées de zone à contrôler pour la collision
		areas_box = ( (indexXmin, indexYmin), (indexXmax, indexYmax)) >> def define_areas_box()
		direction = (isRight, isUp, isHorizontal, isVertical) >> def define_direction()
		"""
		(isRight, isUp, isHorizontal, isVertical) = direction
		if isHorizontal:
			return [ (areas_box[int(isRight)][X], y) for y in range( areas_box[0][Y], areas_box[1][Y]+1) ]
		elif isVertical:
			return [ (x, areas_box[int(isUp)][Y]) for x in range( areas_box[0][X], areas_box[1][X]+1) ]
		else:
			return [ (areas_box[int(isRight)][X], y) for y in range( areas_box[0][Y], areas_box[1][Y]+1) ] + \
				   [ (x, areas_box[int(isUp)][Y]) for x in range( areas_box[0][X] + int(not isRight), areas_box[1][X] + int(not isRight)) ]
		
		
	def calculate_next_area(self, areas_box, direction, corner_point, direction_vector):
		"""Calcule les coordonnées de la prochaine zone à être intersectée pour le point d'angle
		areas_box = ( (indexXmin, indexYmin), (indexXmax, indexYmax)) >> def define_areas_box()
		direction = (isRight, isUp, isHorizontal, isVertical) >> def define_direction()
		corner_point = Point2()
		direction_vector = Vector2()
		world = World()
		return = ( X area index, Y area index, delta time)
		"""
		isRight, isUp, isHorizontal, isVertical = direction
		# go to next area
		if isVertical:
			dtX = 9999999.
		else:
			dtX = ( ( (areas_box[isRight][X] + int(isRight)) * self.area_size ) \
					- corner_point.x) / float(direction_vector.x)
		if isHorizontal:
			dtY = 9999999.
		else:
			dtY = ( ( (areas_box[isUp][Y] + int(isUp)) * self.area_size ) \
					- corner_point.y) / float(direction_vector.y)
		dt = min(dtX, dtY)
		rayX = corner_point.x + dt * direction_vector.x
		rayY = corner_point.y + dt * direction_vector.y
		# correction
		return ( int(rayX) - int(not isRight), \
				 int(rayY) - int(not isUp   ), dt)

	
	def calculate_actor_collisions(self, corner_point, direction, direction_vector, delta_time, \
								   actor_size, areas_to_check):
		"""Calcule les collisions avec l'élément mobile dans les zones listées uniquement.
		L'ensemble des collisions détectées d'une zone est stocké dans la liste temp.
		corner_point = Point2()
		direction_vector = Vector2()
		delta_time = (t0, t1)
		areas_to_check = ( ( X area index, Y area index),...)
		return ( collision, ...) 
		  with collision = ( area X, area Y, dt, element in collision)
		"""
		collisions_list = []
		# for each area get collisions
		for area_index in areas_to_check:
			# init - get area
			areaX = area_index[X]
			areaY = area_index[Y]
			area = self.world.area( areaX, areaY)
			##area_tested = filter(lambda x: x.index_x==areaX and x.index_y==areaY, temp_collisions)
			##if len(area_tested) != 0:
			##	area_collisions = area_tested
			# get collision in this area
			collisions_list += self.calculate_area_collisions( areaX, areaY, area, direction, \
															   corner_point, direction_vector, actor_size)
		return collisions_list

	
	def calculate_area_collisions(self, areaX, areaY, area, \
								  direction, corner_point, direction_vector, \
								  actor_size):
		"""Calcule les collisions dans une zone
		area = Area()
		direction = (isRight, isUp, isHorizontal, isVertical) >> def define_direction()
		corner_point = Point2()
		direction_vector = Vector2()
		"""
		area_collisions = []
		isRight, isUp, isHorizontal, isVertical = direction
		# elements in area > we list all collisions
		for element in area.linked_elements:
			isNearX = False
			isCollisionX = False
			if not isVertical:
				dt = (element.border()[not isRight][X] - corner_point.x) / direction_vector.x
				if dt >= 0 and dt < 1:
					isNearX = True
					rayX = element.border()[not isRight][X]
					rayY = corner_point.y + dt * direction_vector.y
					# vérifier la collision entre le segment de l'objet element et le segment du corner_point
					if isUp:
						segment = ( rayY - actor_size.y + 1, rayY)
					else:
						segment = ( rayY, rayY + actor_size.y - 1)
					isCollisionX = self.isSegmentCollision \
								 ( segment, \
								   (element.border()[0][Y], element.border()[1][Y]-1))
			isNearY = False
			isCollisionY = False
			if isCollisionX == False and not isHorizontal:
				dt = (element.border()[not isUp][Y] - corner_point.y) / direction_vector.y
				# dt between 0. and 1.
				if dt >= 0 and dt < 1:
					isNearY = True
					rayX = corner_point.x + dt * direction_vector.x
					rayY = element.border()[not isUp][Y]
					if isRight:
						segment = ( rayX-actor_size.x +1, rayX)
					else:
						segment = ( rayX, rayX+actor_size.x -1)
					isCollisionY = self.isSegmentCollision \
								 ( segment, \
								   (element.border()[0][X], element.border()[1][X]-1))
			if isCollisionX == True or isCollisionY == True:
				# there is collision in (rayX,rayY) point with (dt) time
				# but is it the right area ?
				epsilonX = -1 * (not isRight)
				epsilonY = -1 * (not isUp)
				collision = Collision( rayX, rayY, int(rayX+epsilonX), int(rayY+epsilonY), dt, element)
				##if collision.index_x == areaX and collision.index_y == areaY:
				area_collisions.append( collision )
				## TO DO : optimisation à prévoir
		# end of for element in world.area( areaX, areaY).linked_elements:
		return area_collisions

	
	def isSegmentCollision(self, segmentA, segmentB):
		"""
		segmentA : couple de float (xA1, xA2)
		segmentB : couple de float (xB1, xB2)
		"""
		if segmentB[0] <= segmentA[0] <= segmentB[1]:
			return True
		if segmentB[0] <= segmentA[1] <= segmentB[1]:
			return True
		if segmentA[0] <= segmentB[0] <= segmentA[1]:
			return True
		if segmentA[0] <= segmentB[1] <= segmentA[1]:
			return True
		return False
		
	
class Collision:
	def __init__(self):
		self.x = 0.
		self.y = 0.
		self.index_x = 0
		self.index_y = 0
		self.dt = 0.
		self.element = None

	def __init__(self, x, y, index_x, index_y, dt, element):
		self.x, self.y, self.index_x, self.index_y, self.dt, self.element = \
			x, y, index_x, index_y, dt, element

	def __repr__(self):
		return 'Collision(x=%.2f, y=%.2f, index_x=%d, index_y=%d, dt=%.2f, %r)' \
			   % (self.x, self.y, self.index_x, self.index_y, self.dt, self.element)



##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

class SimpleAlgoRaymapping:

	def __init__(self, world):
		self.world = world
		#self.area_size = 10
		self.area_size = self.world.area_size
	
	def move_element(self, actor, world):
		movement = actor.speed
		actor.increments = []
		while movement > 0:
			increment = actor.find_increment()
			if increment.x == 0 and increment.y == 0:
				break
			# new position
			actor.new_position = actor.position + increment
			movement -= 1
			# check position
			collisions_list = self.update_collisions( actor, world)
			#for element in collisions_list:
			if len(collisions_list) == 0:
				actor.position = actor.new_position
				actor.past_increment = increment
				actor.increments = []
			else:
				actor.increments += [ increment ]
		
	def update_element_position(self, actor, direction_vector):
		collision = None
		new_position = actor.position
		
		# collisions list
		collisions = []
		# actor bounds
		box = self.define_new_box( actor)
		rangey = range( int(box[0].y), int(box[1].y)+1)
		rangex = range( int(box[0].x), int(box[1].x)+1)
		for y in rangey:
			for x in rangex:
				collisions += self.find_new_collisions( actor, self.world.area(x,y))
		#return collisions
		
		return (new_position, collision)
				
	def update_collisions(self, actor):
		# collisions list
		collisions = []
		# actor bounds
		box = self.define_new_box( actor)
		rangey = range( int(box[0].y), int(box[1].y)+1)
		rangex = range( int(box[0].x), int(box[1].x)+1)
		for y in rangey:
			for x in rangex:
				collisions += self.find_new_collisions( actor, self.world.area(x,y))
		return collisions

	def define_new_box(self, element):
		"""Calcule les coordonnées des deux zones extrêmes contenant l'élément (la zone min et la zone max)
		element_position = Point2()
		element_size = float
		return = ( (indexXmin, indexYmin), (indexXmax, indexYmax))
		"""
		## la zone (0,0) va de 0 à 9:
		## = 10 positions de 1 unité
		return ( element.new_position / self.area_size, \
				 (element.new_position + element.size - Vector2(1,1)) / self.area_size )

	def find_new_collisions(self, actor, area):
		collisions = []
		for element in area.linked_elements:
			isXCollision = self.isSegmentCollision( ( actor.new_position.x, actor.new_position.x + actor.size.x - 1), \
											   ( element.position.x, element.position.x + element.size.x - 1))
			if isXCollision == True:
				isYCollision = self.isSegmentCollision( ( actor.new_position.y, actor.new_position.y + actor.size.y - 1), \
												   ( element.position.y, element.position.y + element.size.y - 1))
				if isYCollision == True:
					collisions.append( element)
		return collisions
		
	def isSegmentCollision(self, segmentA, segmentB):
		"""
		segmentA : couple de float (xA1, xA2)
		segmentB : couple de float (xB1, xB2)
		"""
		if segmentB[0] <= segmentA[0] <= segmentB[1]:
			return True
		if segmentB[0] <= segmentA[1] <= segmentB[1]:
			return True
		if segmentA[0] <= segmentB[0] <= segmentA[1]:
			return True
		if segmentA[0] <= segmentB[1] <= segmentA[1]:
			return True
		return False

	
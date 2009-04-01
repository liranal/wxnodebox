#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

import math
from euclid import *

X = 0
Y = 1


def distance( elementA, elementB):
	vector = elementA.position - elementB.position
	return abs(vector)
	#dist = (elementA.position(X) - elementB.position(X))**2 \
	#	 + (elementA.position(Y) - elementB.position(Y))**2
	#dist = math.sqrt(dist)
	#return dist

def isCollision( my_object, objects_list):
	for element in objects_list:
		# calcul distance between two elements
		dist = distance(my_object, element);
		if dist < my_object.size + element.size:
			return True
	return False


class PhysicEngine:
	def __init__(self):
		self.world = None
		#self.objects_list = []
		self.actor = None
		#self.creatures_list = []
	
	def initialize(self, my_world, my_actor):
		self.world = my_world
		self.actor = my_actor
		
	def add_map(self, my_map):
		self.world = my_map
		
	def turn(self):
		delta_time = 0.5
		# move actor
		self.move_actor( self.actor, delta_time)
		# move creatures
		creatures_list = self.world.creatures_list
		for element in creatures_list:
			self.move_creature( element, delta_time)
		# Actifitial Intelligence
		# event
		## TO DO - ?? which ??
		
	def move_actor(self, actor, delta_time):
		old_position = actor.position
		# calculate direction vector
		direction_vect = self.calculate_direction_vector( actor, delta_time)
		# remove actor from old area
		self.detach_element_in_world( self.actor)
		# update position
		algo = Raymapping()
		algo.update_element_position( actor, direction_vect, self.world)
		# add actor to new area
		self.attach_element_in_world( self.actor)

	def move_moving_element(self, element, delta_time):
		old_position = element.position
		# calculate direction vector
		direction_vect = self.calculate_direction_vector( element, delta_time)
		# remove actor from old area
		self.detach_element_in_world( self.element)
		# update position
		algo = Raymapping()
		algo.update_element_position( element, direction_vect, self.world)
		# add actor to new area
		self.attach_element_in_world( self.element)
		
	def calculate_direction_vector(self, element, delta_time):
		"""Calcule le vecteur de mouvement de l'élément
		"""
		assert isinstance( element, MovingElement)
		return Vector2( element.speed * delta_time, 0.).rotate( element.angle)
		
			
	def calculate_new_position(self, element, delta_time):
		initial_position = element.position()
		# angle in radian : angle=0 => X direction . angle=pi/2 => Y direction
		angle = element.direction()
		speed = element.speed()
		new_position = element.position \
					 + Vector2( speed * delta_time, 0.).rotate( angle)
		return new_position
	
	def attach_element_in_world( actor):
		position = actor.position
		size = actor.size
		# begin area part
		areaXb = int(position.x - size)
		areaYb = int(position.y - size)
		# end area part
		areaXe = int(position.x + size)
		areaYe = int(position.y + size)
		for posy in range( areaYb, areaYe):
			for posx in range( areaXb, areaXe):
				self.world.area(posx, posy).add_linked_element(actor)
	
	def detach_element_in_world( element):
		position = element.position
		size = element.size
		# begin area part
		areaXb = int(position.x - size)
		areaYb = int(position.y - size)
		# end area part
		areaXe = int(position.x + size)
		areaYe = int(position.y + size)
		for posy in range( areaYb, areaYe):
			for posx in range( areaXb, areaXe):
				self.world.area(posx, posy).remove_linked_element(element)

				
class SimpleAlgoRaymapping:
	## TO DO the more simple way
	def update_element_position(self, moving_element, direction_vect, world):
		"""
		"""
		old_position = actor.position
		new_position = self.calculate_new_position( actor, delta_time)
		# check collision with elements
		# find direction : left or right (x) then up or down (y)
		isRight = (new_position.x > old_position.x)
		isHorizontal = (new_position.x == old_position.x)
		isUp = (new_position.y < old_position.y)
		isVertical = (new_position.y == old_position.y)
		box_field = []
		box_field.append( (old_position.x-size, old_position.y-size))
		box_field.append( (old_position.x+size, old_position.y+size))
		box_field.append( (new_position.x-size, new_position.y-size))
		box_field.append( (new_position.x+size, new_position.y+size))
		min_box = reduce(lambda x,y: ( min(x[0],y[0]), min(x[1],y[1])), box_field)
		max_box = reduce(lambda x,y: ( max(x[0],y[0]), max(x[1],y[1])), box_field)
		
		if isUp == True:
			# action
			pass
		elif isHorizontal == True:
			# action
			pass
		else:
			# action
			pass
		
		# check collision with map
		# check collision with objects
		# check collision with creatures
		# if ok then update position
		if isCollision == False:
			self.actor.update_position( new_position)
		else:
			self.actor.keep_position()


## TODO
## il faut réfléchir à remplacer le isHorizontal et isVertical par une valeur faible mais non null de direction_vect
	
class Raymapping:
	""" algorithme de raymapping pour déterminer les collisions entre éléments.
	Cette algo retourne
	>> main procedure : def calculate_collision()
	"""
	
	def define_areas_box(self, element):
		"""Calcule les coordonnées des deux zones extrêmes contenant l'élément (la zone min et la zone max)
		element = Element()
		return = ( (indexXmin, indexYmin), (indexXmax, indexYmax))
		"""
		return ( (int(element.position.x-element.size), int(element.position.y-element.size)), \
				 (int(element.position.x+element.size), int(element.position.y+element.size)) )

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
				   [ (x, areas_box[int(isUp)][Y]) for x in range( areas_box[0][X], areas_box[1][X]) ]

	def define_direction(self, direction_vect):
		""" Définit la direction au format boolean à partir d'un vecteur:
		direction_vect = Vector2()
		return = (isRight, isUp, isHorizontal, isVertical) = (boolean, boolean, boolean, boolean)
		"""
		isRight, isUp, isHorizontal, isVertical = False, False, True, True
		if direction_vect.x == 0.:
			isHorizontal = False
		elif direction_vect.x > 0.:
			isRight = True
		if direction_vect.y == 0.:
			isVertical = False
		elif direction_vect.y > 0.:
			isUp = True
		return (isRight, isUp, isHorizontal, isVertical)
		
	def calculate_next_area(self, areas_box, direction, corner_point, direction_vect, world):
		"""Calcule les coordonnées de la prochaine zone à être intersectée pour le point d'angle
		areas_box = ( (indexXmin, indexYmin), (indexXmax, indexYmax)) >> def define_areas_box()
		direction = (isRight, isUp, isHorizontal, isVertical) >> def define_direction()
		corner_point = Point2()
		direction_vect = Vector2()
		world = World()
		return = ( X area index, Y area index, delta time)
		"""
		isRight, isUp, isHorizontal, isVertical = direction
		# go to next area
		area_size = 1.
		if isRight:
			shiftX = area_size
		else:
			shiftX = 0.
		if isUp:
			shiftY = area_size
		else:
			shiftY = 0.
		if isVertical:
			dtX = 9999999.
		else:
			dtX = (areas_box[isRight][X] + shiftX - corner_point.x) / direction_vect.x
		if isHorizontal:
			dtY = 9999999.
		else:
			dtY = (areas_box[isUp][Y] + shiftY - corner_point.y) / direction_vect.y
		dt = min(dtX, dtY)
		rayX = corner_point.x + dt * direction_vect.x
		rayY = corner_point.y + dt * direction_vect.y
		next_area = (int(rayX), int(rayY))
		return (int(rayX), int(rayY), dt)
		
	def update_element_position(self, moving_element, direction_vect, world):
		'''MAIN PROCEDURE : Recherche si elle existe la collision entre un élément mouvant et son environnement
		moving_element = MovingElement()
		direction_vect = Vector2()
		world = World()
		return = None
		Exit > moving_element.position is updated'''
		# initialize direction
		direction = self.define_direction( direction_vect)
		isRight, isUp, isHorizontal, isVertical = direction
		if not isHorizontal or isRight:
			x_factor = 1.
		else:
			x_factor = -1.
		if not isVertical or isUp:
			y_factor = 1.
		else:
			y_factor = -1.
		# init delta time
		dt0 = 0
		# find corner
		g_to_corner = Vector2( moving_element.position.x + moving_element.size*x_factor, \
							  moving_element.position.y + moving_element.size*y_factor)
		element_position = Point2( moving_element.position.x, moving_element.position.x)
			
		area_next_collisions_list = []
		#########################################################
		while dt0 < 1.:
			# corner point coordinate
			corner_point = element_position + g_to_corner # Point2
			# areas borders
			areas_bounds = self.define_area_box( moving_element, element_position)
			areas_to_check = self.select_areas_to_check( areas_bounds, direction)
			
			# prepare futur next area (and get max dt1)
			next_area_collision = self.calculate_next_area( areas_bounds, direction, corner_point, direction_vect, dt0, world)
			dt1 = max(next_area_collision[2], 1.)
		
			# get collision in this area group
			collisions_list = self.calculate_moving_element_collisions \
							( corner_point, direction_vect, (dt0, dt1), \
							  area_to_test_list, area_next_collisions_list)
		
			# if no collision, go to the next position
			if len(area_group_collision) == 0:
				# move_element to the next area
				dt0 = dt1
				element_position = Point2( moving_element.position.x * direction_vect.x*dt0, \
										   moving_element.position.y * direction_vect.y*dt0)
			else:
				# if collision, select the dt minus one
				collision = reduce(lambda x,y: min(a,b, lambda c: c.dt), collisions_list)
				element_position = Point2(collision.x, collision.y) - g_to_corner
				dt0=1.
		#########################################################
		# stop of the moving element
		# update element position
		moving_element.position = element_position
			
	def calculate_moving_element_collisions(self, corner_point, direction_vect, delta_time, \
											areas_to_check, temp_collisions):
		"""Calcule les collisions avec l'élément mobile dans les zones listées uniquement.
		L'ensemble des collisions détectées d'une zone est stocké dans la liste temp.
		corner_point = Point2()
		direction_vect = Vector2()
		delta_time = (t0, t1)
		areas_to_check = ( ( X area index, Y area index),...)
		temp_areas_collisions = ( temp_collision,...)
		  with temp_collisions = (element in collision, X area index, Y area index, area X, area Y, dt)
		return ( collision, ...) 
		  with collision = ( area X, area Y, dt, element in collision)
		"""
		collisions_list = []
		# for each area get collisions
		for area_index in areas_to_check:
			# init - get area
			areaX = area_index[X]
			areaY = area_index[Y]
			area = world.area( areaX, areaY)
			area_collisions_list = []
			# xxxxx
			area_tested = filter(lambda x: x.index_x==areaX and index_y==areaY, temp_collisions)
			if len(area_tested) != 0:
				area_collisions = area_tested
			else:
				# get collision in this area
				area_collisions = self.calculate_area_collisions( temp_collisions)
				# add all collision of this area
				temp_collisions += area_collisions
			collisions_list += area_collisions
		return collisions_list
		
	def calculate_area_collisions(self, area, direction, corner_point, direction_vect):
		"""Calcule les collisions dans une zone
		area = Area()
		direction = (isRight, isUp, isHorizontal, isVertical) >> def define_direction()
		corner_point = Point2()
		direction_vect = Vector2()
		"""
		area_collisions = []
		isRight, isUp, isHorizontal, isVertical = direction
		# elements in area > we list all collisions
		for element in area.linked_elements:
			dt = (element.border[not isRight][X] - corner_point.x) / direction_vect.x
			isNearX = False
			isCollisionX = False
			if dt >= 0 and dt < 1:
				isNearX = True
				rayX = element.border[not isRight][X]
				rayY = corner_point.y + dt * direction_vect.y
				if rayY >= element.border[0][Y] and \
				   rayY <= element.border[1][Y]:
						isCollisionX = True
			isNearY = False
			isCollisionY = False
			if isCollisionX == False:
				dt = (element.border[not isUp][Y] - point.y) / direction_vect.y
				# dt between 0. and 1.
				if dt >= 0 and dt < 1:
					isNearY = True
					rayX = corner_point.x + dt * direction_vect.x
					rayY = element.border[not isUp][Y]
					if rayX >= element.border[0][X] and \
					   rayX <= element.border[1][X]:
						isCollisionY = True
			if isCollisionX == True or isCollisionY == True:
				# there is collision in (rayX,rayY) point with (dt) time
				# but is it the right area ?
				collision = Collision( rayX, rayY, int(rayX), int(rayY), dt, element)
				if collision.index_x == areaX and collision.index_y == areaY:
					area_collisions.append( collision )
				## TO DO : optimisation à prévoir
				#else:
				#	# collision out of the area
				#	temp_collisions.append( collision )
			# end of for element in world.area( areaX, areaY).linked_elements:
		return area_collisions
		

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
		

	
	
	
	
	
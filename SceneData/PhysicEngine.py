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
		#self.calculate_new_position( actor, delta_time)
		# move creatures
		creatures_list = self.world.creatures_list
		for element in creatures_list:
			self.move_creature( element, delta_time)
		# event
		## TO DO - ?? which ??
		
	def move_actor(self, actor, delta_time):
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
		# remove actor from old area
		# add actor to new area
		attach_actor_in_world( self.actor, self.world)

	def move_creature(self, creature, delta_time):
		new_position = self.calculate_new_position( creature, delta_time)
		# check collision with map
		# check collision with actor
		# check collision with objects
		# check collision with creatures
		# if ok then update position
		if isCollision == False:
			creature.update_position( new_position)
		else:
			creature.keep_position()
		
	def calculate_new_position(self, element, delta_time):
		initial_position = element.position()
		# angle in radian : angle=0 => X direction . angle=pi/2 => Y direction
		angle = element.direction()
		speed = element.speed()
		new_position = element.position \
					 + Vector2( speed * delta_time, 0.).rotate( angle)
		return new_position
	
	def attach_element_in_world( actor, world):
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
				world.area(posx, posy).add_linked_element(actor)
	
	def detach_element_in_world( element, world):
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
				world.area(posx, posy).remove_linked_element(element)
	

class Raymapping:
	
	def calculate_collision( point, direction_vect, world):
		# init
		areaX = int(point.x)
		areaY = int(point.y)
		area_collisions_list = []
		area_next_collisions_list = []
		
		while len(area_collisions_list) == 0:
			# elements in area > we list all collisions
			for element in world.area( areaX, areaY).linked_elements:
				isCollision = False
				# check and find collision of this area in area_next_collisions_list
				for collision in area_next_collisions_list:
					#area_next_collisions_list.append( (element, collision_areaX, collision_areaY, rayX, rayY, dt) )
					if collision[0] == element and collision[1] == areaX and collision[2] == areaY:
						# add this collision > area_collisions_list.append( (rayX, rayY, dt) )
						area_collisions_list.append( (collision[3], collision[4], collision[5], element) )
						area_next_collisions_list.remove( collision)
						isCollision = True
						continue
				if isCollision == True:
					continue
				#element.size, element.position, element.border
				# dt between 0. and 1.
				# rayX = point.x + dt * direction_vect.x
				# rayY = point.y + dt * direction_vect.y
				#element.position.x
				# in collision rayX = element.position.x-element.size = element.border[X][0]
				# in collision rayY = element.position.y-element.size = element.border[Y][0]
				# >> dt = (element.border[X][0] - point.x) / direction_vect.x
				# >> dt = (element.border[Y][0] - point.y) / direction_vect.y
				dt = (element.border[X][0] - point.x) / direction_vect.x
				isNearX = False
				isCollisionX = False
				if dt >= 0 and dt < 1:
					isNearX = True
					rayX = element.border[X][0]
					rayY = point.y + dt * direction_vect.y
					if rayY >= element.border[Y][0] and \
					   rayY <= element.border[Y][1]:
						isCollisionX = True
				isNearY = False
				isCollisionY = False
				if isCollisionX == False:
					dt = (element.border[Y][0] - point.y) / direction_vect.y
					if dt >= 0 and dt < 1:
						isNearY = True
						rayX = point.x + dt * direction_vect.x
						rayY = element.border[Y][0]
						if rayX >= element.border[X][0] and \
						   rayX <= element.border[X][1]:
							isCollisionY = True
				if isCollisionX == True or isCollisionY == True:
					# there is collision in (rayX,rayY) point with (dt) time
					# but is it the right area ?
					collision_areaX = int(rayX)
					collision_areaY = int(rayY)
					if collision_areaX == areaX and collision_areaY == areaY:
						area_collisions_list.append( (rayX, rayY, dt, element) )
					else:
						area_next_collisions_list.append( (element, collision_areaX, collision_areaY, rayX, rayY, dt) )
			# end of for element in world.area( areaX, areaY).linked_elements:
			
			if len(area_collisions_list) == 0:
				# no collision > go to the next area
				# go to next area
				next_area = self.calculate_next_area( point, direction_vect, world)
				if dt > 0 and dt<= 1:
					#next_area = ( next_area[0], next_area[1])
					areaX = next_area[0]
					areaY = next_area[1]
				else:
					break
		# end of the while len(area_collisions_list) == 0:
		if len(area_collisions_list) != 0:
			# if there is collision, we choose the minus dt one.
			min_collision = reduce(lambda x,y: minus_list_element( 2, x, y), area_collisions_list)
		else:
			min_collision = None
		return min_collision
			
	def calculate_next_area( point, direction_vect, world):
		# go to next area
		dtX = (area.border[X][0] - point.x) / direction_vect.x
		dtY = (area.border[Y][0] - point.y) / direction_vect.y
		dt = min(dtX, dtY)
		rayX = point.x + dt * direction_vect.x
		rayY = point.y + dt * direction_vect.y
		next_area = (int(rayX), int(rayY))
		return (int(rayX), int(rayY), dt)
			
			
def minus_list_element( index, elementA, elementB):
	if elementA[index] <= elementB[index]:
		return elementA
	else:
		return elementB
	
	
class Raymapping2:
	def calculate_collision( moving_element, direction_vect, world):
		# initialize direction
		isVertical = True
		isHorizontal = True
		if direction_vect.x == 0.:
			isHorizontal = False
			x_factor = 1.
		elif direction_vect.x > 0.:
			isRight = True
			x_factor = 1.
		else:
			isLeft = True
			x_factor = -1.
		if direction_vect.y == 0.:
			isVertical = False
			y_factor = 1.
		elif direction_vect.y > 0.:
			isUp = True
			y_factor = 1.
		else:
			isDown = True
			y_factor = -1.
		# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
		g_to_point = Vector2( moving_element.position.x + moving_element.size*x_factor, \
							  moving_element.position.y + moving_element.size*y_factor)
		point = moving_element.position + g_to_point # Point2
		#
		# init
		areaX = int(point.x)
		areaY = int(point.y)
		area_collisions_list = []
		area_next_collisions_list = []
		
		while len(area_collisions_list) == 0:
			# elements in area > we list all collisions
			for element in world.area( areaX, areaY).linked_elements:
				isCollision = False
				# check and find collision of this area in area_next_collisions_list
				for collision in area_next_collisions_list:
					#area_next_collisions_list.append( (element, collision_areaX, collision_areaY, rayX, rayY, dt) )
					if collision[0] == element and collision[1] == areaX and collision[2] == areaY:
						# add this collision > area_collisions_list.append( (rayX, rayY, dt) )
						area_collisions_list.append( (collision[3], collision[4], collision[5], element) )
						area_next_collisions_list.remove( collision)
						isCollision = True
						continue
				if isCollision == True:
					continue
				#element.size, element.position, element.border
				# dt between 0. and 1.
				# rayX = point.x + dt * direction_vect.x
				# rayY = point.y + dt * direction_vect.y
				#element.position.x
				# in collision rayX = element.position.x-element.size = element.border[X][0]
				# in collision rayY = element.position.y-element.size = element.border[Y][0]
				# >> dt = (element.border[X][0] - point.x) / direction_vect.x
				# >> dt = (element.border[Y][0] - point.y) / direction_vect.y
				dt = (element.border[X][0] - point.x) / direction_vect.x
				isNearX = False
				isCollisionX = False
				if dt >= 0 and dt < 1:
					isNearX = True
					rayX = element.border[X][0]
					rayY = point.y + dt * direction_vect.y
					if rayY >= element.border[Y][0] and \
					   rayY <= element.border[Y][1]:
						isCollisionX = True
				isNearY = False
				isCollisionY = False
				if isCollisionX == False:
					dt = (element.border[Y][0] - point.y) / direction_vect.y
					if dt >= 0 and dt < 1:
						isNearY = True
						rayX = point.x + dt * direction_vect.x
						rayY = element.border[Y][0]
						if rayX >= element.border[X][0] and \
						   rayX <= element.border[X][1]:
							isCollisionY = True
				if isCollisionX == True or isCollisionY == True:
					# there is collision in (rayX,rayY) point with (dt) time
					# but is it the right area ?
					collision_areaX = int(rayX)
					collision_areaY = int(rayY)
					if collision_areaX == areaX and collision_areaY == areaY:
						area_collisions_list.append( (rayX, rayY, dt, element) )
					else:
						area_next_collisions_list.append( (element, collision_areaX, collision_areaY, rayX, rayY, dt) )
			# end of for element in world.area( areaX, areaY).linked_elements:
			
			if len(area_collisions_list) == 0:
				# no collision > go to the next area
				# go to next area
				next_area = self.calculate_next_area( point, direction_vect, world)
				if dt > 0 and dt<= 1:
					#next_area = ( next_area[0], next_area[1])
					areaX = next_area[0]
					areaY = next_area[1]
				else:
					break
		# end of the while len(area_collisions_list) == 0:
		if len(area_collisions_list) != 0:
			# if there is collision, we choose the minus dt one.
			min_collision = reduce(lambda x,y: minus_list_element( 2, x, y), area_collisions_list)
		else:
			min_collision = None
		return min_collision
			
	def calculate_next_area( point, direction_vect, world):
		# go to next area
		dtX = (area.border[X][0] - point.x) / direction_vect.x
		dtY = (area.border[Y][0] - point.y) / direction_vect.y
		dt = min(dtX, dtY)
		rayX = point.x + dt * direction_vect.x
		rayY = point.y + dt * direction_vect.y
		next_area = (int(rayX), int(rayY))
		return (int(rayX), int(rayY), dt)
	
	
	
	
	
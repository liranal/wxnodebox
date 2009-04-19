#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

from SuperElement import *

import Image


class Wall(StaticElement):
	def __init__(self, index_x, index_y):
		StaticElement.__init__(self)
		# position of the bottom left corner
		self.position = Point2( index_x, index_y)
		self.size = Point2(10,10)

class Area(Element):
	def __init__(self):
		Element.__init__(self)
		self.linked_elements = []
		
	def add_linked_element(self, element):
		self.linked_elements.append( element)

	def remove_linked_element(self, element):
		self.linked_elements.remove( element)
		
class World:
	def __init__(self):
		# une map est une matrice carrée d'entiers
		self.sizeX = 0
		self.sizeY = 0
		self.null_area = Area() # lost area
		self.area_list = []
		self.actor = None
		self.creatures_list = []
		self.area_size = 10
		
		
	def area(self, x, y):
		#assert type(x) == int
		#assert type(y) == int
		assert isinstance(x, int)
		assert isinstance(y, int)
		##assert x >= 0
		##assert y >= 0
		##assert x < self.sizeX
		##assert y < self.sizeY
		if x<0 or y<0 or x >= self.sizeX or y >= self.sizeY:
			return self.null_area
		return self.area_list[x][y]
			
	def init_area(self):
		assert self.sizeX > 0
		assert self.sizeY > 0
		self.area_list = []
		for xpos in range(self.sizeX):
			line = []
			for ypos in range(self.sizeY):
				new_area = Area()
				line.append( new_area)
			self.area_list.append( line)
		
	def load_map_from_image(self, image):
		# load black&white Image in wall map
		self.sizeX = 10
		self.sizeY = 10
		#self.init_area()
		## update each area
		#for ypos in range(self.sizeY):
			#wall = Wall()
			#self.area( 0, ypos).add_linked_element( wall)
		#xpos = self.sizeX-1
		#for ypos in range(self.sizeY):
			#wall = Wall()
			#self.area( xpos, ypos).add_linked_element( wall)
		#
		my_image = Image.open( image)
		self.sizeX = my_image.size[0]
		## WARNING : TO TEST ONLY
		self.sizeY = my_image.size[1] / 2 + 10
		self.init_area()
		# create wall and actor
		self.area_size = 10
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				r,g,b = my_image.getpixel( (x, y))
				if r==g==b and r<=60:
					# alors c est du gris
					wall = Wall( self.area_size * x, self.area_size * y)
					self.area( x, y).add_linked_element( wall)
				elif r!=0 and g==b==0:
					self.actor = Actor()
					self.actor.position = self.area_size * Point2( x, y)
		## create one creature
		creature = Creature()
		creature.position = Point2(621.00, 48.00)
		creature.speed = 2
		self.creatures_list.append( creature)
		self.add_element( creature)
		## create one creature
		creature = Creature()
		creature.position = Point2(2428.00, 28.00)
		creature.speed = 3
		self.creatures_list.append( creature)
		self.add_element( creature)
		for index in range(0,20):
			creature = Creature()
			creature.position = Point2(635.00+(index * 10), 40.00)
			creature.speed = 4
			self.creatures_list.append( creature)
			self.add_element( creature)
			

	def add_element(self, element):
		# element position and size
		bounds = element.area_bounds( self.area_size)
		rangey = range( bounds[0][1], bounds[1][1] +1)
		rangex = range( bounds[0][0], bounds[1][0] +1)
		for y in rangey:
			for x in rangex:
				self.area(x,y).add_linked_element( element)

	def remove_element(self, element):
		# element position and size
		bounds = element.area_bounds( self.area_size)
		rangey = range( bounds[0][1], bounds[1][1] +1)
		rangex = range( bounds[0][0], bounds[1][0] +1)
		for y in rangey:
			for x in rangex:
				self.area(x,y).remove_linked_element( element)
				
	def load_creatures(self):
		pass
	
	def load_static_objects(self):
		pass

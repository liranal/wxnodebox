#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

from SuperElement import *

import Image

class Wall(StaticElement):
	def __init__(self, index_x, index_y):
		StaticElement.__init__(self)
		self.position = Point2( index_x+0.5, index_y+0.5)
		self.size = 0.5

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
		self.null_area = Area()
		self.area_list = []
		self.actor = None
		self.creatures_list = ()
		
		
	def area(self, x, y):
		#assert type(x) == int
		#assert type(y) == int
		assert isinstance(x, int)
		assert isinstance(y, int)
		#assert x >= 0
		#assert y >= 0
		#assert x < self.sizeX
		#assert y < self.sizeY
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
		self.sizeX = 1
		self.sizeY = 1
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
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				r,g,b = my_image.getpixel( (x, y))
				if r==g==b and r<=60:
					# alors c est du gris
					wall = Wall( x, y)
					self.area( x, y).add_linked_element( wall)
				elif r!=0 and g==b==0:
					self.actor = Actor()
					self.actor.position = Point2( x, y)
				

	def load_creatures(self):
		pass
	
	def load_static_objects(self):
		pass

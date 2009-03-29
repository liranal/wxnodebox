#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

class Wall(Element):
	def __init__(self):
		Element.__init__(self)
		

class Area(Element):
	def __init__(self):
		Element.__init__(self)
		self.linked_elements = ()
		
	def add_linked_element( element):
		self.linked_elements.append( element)

	def remove_linked_element( element):
		self.linked_elements.remove( element)
		
class World:
	def __init__(self):
		# une map est une matrice carrée d'entiers
		self.sizeX = 0
		self.sizeY = 0
		self.area_list = ( () )
		self.creatures_list = ()
		
	def area(self, x, y):
		assert type(x) == int
		assert type(y) == int
		assert x >= 0
		assert y >= 0
		assert x < self.sizeX
		assert y < self.sizeY
		return self.area_list(x)(y)
			
	def init_area(self):
		assert self.sizeX > 0
		assert self.sizeY > 0
		self.area_list = ()
		for ypos in range(sizeY):
			line = ()
			for xpos in range(sizeX):
				new_area = Area()
				line.append( new_area)
			self.area_list.append( line)
		
	def load_map_from_image(self, image):
		# load black&white Image in wall map
		self.sizeX = 10
		self.sizeY = 10
		self.init_area()
		# update each area
		for ypos in range(self.sizeY):
			wall = Wall()
			self.area( 0, ypos).add_linked_element( wall)
		xpos = self.sizeX-1
		for ypos in range(self.sizeY):
			wall = Wall()
			self.area( xpos, ypos).add_linked_element( wall)

	def load_creatures(self):
		pass
	
	def load_static_objects(self):
		pass

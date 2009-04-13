#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

def getNewElementId( element):
	element_id = elements_manager.next_id()
	elements_manager.add_element( element)
	return element_id

class ElementsManager:
	def __init__(self):
		self.idmax = 0
		self.elements_list = []

	def next_id(self):
		self.idmax += 1
		return self.idmax
		
	def add_element(self, element):
		self.elements_list.append( element)

class Element:
	def __init__(self):
		self.id = getNewElementId(self)
		self.name="Element"+str(self.id)

	def border(self):
		return ( self.position, \
				 self.position + self.size)
	
	def area_bounds(self, area_size):
		return ( ( int(self.position.x / area_size),  \
				   int(self.position.y /area_size) ), \
				 ( int((self.position.x + self.size.x - 1) / area_size), \
				   int((self.position.y + self.size.y - 1) / area_size)) )
		
# Global Variables
elements_manager = ElementsManager()

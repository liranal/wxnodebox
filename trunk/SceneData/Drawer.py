#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 


# classic paint interface
class Drawer:
	"""Abstract drawer class
	"""
	def __init__(self, *args):
		self.init = True

	def update_init(self, *args):
		pass
		
	def color(self, red_component, green_component, blue_component):
		"""
		red_component = integer between 0 and 255
		green_component = integer between 0 and 255
		blue_component = integer between 0 and 255
		"""
		raise NotImplementedError('Can\'t instantiate class `' + \
								  self.__name__ + '\';\n' + \
								  'Abstract methods: ' + \
								  ", ".join(self.__abstractmethods__))

		
	def rectangle(self, x_position, y_position, width, heigth, is_filled):
		"""Draw a rectangle
		"""
		pass

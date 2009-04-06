#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

import wx
import cairo

#from Drawer import *

# classic paint interface
class PycairoDrawer: #(Drawer):
	def __init__(self, *args):
		#self.update_init( *args)
		self.cairoContext = None

	def update_init(self, *args):
		params = len(args)
		if params != 1:
			raise Exception("bouh")
		self.cairoContext = self.createGraphContext( args[0])
		
	def color(self, red_component, green_component, blue_component, alpha_component = 1.):
		"""
		red_component = integer between 0. and 1.
		green_component = integer between 0. and 1.
		blue_component = integer between 0. and 1.
		"""
		self.cairoContext.set_source_rgba( red_component, green_component, blue_component, alpha_component)
		
	def rectangle(self, x_position, y_position, width, height, is_filled = True):
		"""Draw a rectangle
		"""
		self.cairoContext.rectangle( x_position, y_position, width, height)
		if is_filled == True:
			self.cairoContext.fill()
		self.cairoContext.stroke()

	def sprite(self, sprite_image, x_position, y_position, width, height):
		## TODO
		pass
	
	# specific Pycairo
	def createGraphContext( self, wxPaintDCObject):
		## bad : if self.cairoContext == None:
		self.cairoContext = wx.lib.wxcairo.ContextFromDC(wxPaintDCObject)
		return self.cairoContext
	
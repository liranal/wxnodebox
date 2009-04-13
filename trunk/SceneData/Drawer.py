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

	## pour information ceci est l'Algorithme de tracé de segment de Bresenham
	## http://fr.wikipedia.org/wiki/Algorithme_de_tracé_de_segment_de_Bresenham
	def tracerSegment(self, x1, y1, x2, y2):
		assert type(x1)==int
		assert type(y1)==int
		assert type(x2)==int
		assert type(y2)==int
		
		## déclarer entier dx, dy
		dx = x2 - x1
		if dx != 0:
			if dx > 0:
				dy = y2 - y1
				if dy != 0:
					if dy > 0:
						# vecteur oblique dans le 1er quadran
					
						if dx >= dy:
							# vecteur diagonal ou oblique proche de l'horizontale, dans le 1er octant
							e = dx
							dx = e * 2
							dy = dy * 2  # e est positif
							while 1==1:	# déplacements horizontaux
								tracePixel(x1, y1)
								x1 += 1
								if x1 == x2:
									break
								e -= dy
								if e < 0:
									y1 += 1 # déplacement diagonal
									e += dx
						else:
							# vecteur oblique proche de la verticale, dans le 2nd octant
							e = dy
							dy = e * 2
							dx = dx * 2  # e est positif
							while 1==1: # déplacements verticaux
								tracePixel(x1, y1)
								y1 += 1
								if y1 == y2:
									break
								e -= dx
								if e < 0:
									x1 += 1	# déplacement diagonal
									e += dy
					else:
						# sinon dy < 0 (et dx > 0)
						# vecteur oblique dans le 4e cadran
						if dx >= -dy:
							# vecteur diagonal ou oblique proche de l'horizontale, dans le 8e octant
							e = dx
							dx = e * 2
							dy = dy * 2 # e est positif
							while 1==1:	# déplacements horizontaux
								tracePixel(x1, y1)
								x1 += 1
								if x1 == x2:
									break
								e += dy
								if e < 0:
									y1 -= 1 # déplacement diagonal
									e += dx
						else:
							# vecteur oblique proche de la verticale, dans le 7e octant
							e = dy
							dy = e * 2
							dx = dx * 2  # e est négatif
							while 1 == 1: # déplacements verticaux
								tracePixel(x1, y1)
								y1 -= 1
								if y1 == y2:
									break
								e = e + dx
								if e > 0:
									x1 += 1  # déplacement diagonal
									e += dy
				else:
					# sinon dy = 0 (et dx > 0)
					# vecteur horizontal vers la droite
					while x1 != x2:
						tracePixel( x1, y1)
						x1 += 1
			else:
				# sinon  dx < 0
				dy = y2 - y1
				if dy != 0:
					if dy > 0:
						# vecteur oblique dans le 2nd quadran
						if -dx >= dy:
							# vecteur diagonal ou oblique proche de l'horizontale, dans le 4e octant
							e = dx
							dx = e * 2
							dy = dy * 2  # e est négatif
							while 1==1:
								# déplacements horizontaux
								tracePixel(x1, y1)
								x1 -= 1
								if x1 == x2:
									break
								e += dy
								if e >= 0:
									y1 += 1 	# déplacement diagonal
									e += dx
						else:
							# vecteur oblique proche de la verticale, dans le 3e octant
							e = dy
							dy = e * 2
							dx = dx * 2  # e est positif
							while 1==1:
								# déplacements verticaux
								tracePixel(x1, y1)
								y1 += 1
								if y1 == y2:
									break
								e += dx
								if e <= 0:
									x1 -= 1
									# déplacement diagonal
									e += dy
					else:
						# sinon  // dy < 0 (et dx < 0)
						# vecteur oblique dans le 3e cadran
						if dx <= dy:
							# vecteur diagonal ou oblique proche de l'horizontale, dans le 5e octant
							e = dx
							dx = e * 2
							dy = dy * 2 # e est négatif
							while 1==1: # déplacements horizontaux
								tracePixel(x1, y1)
								x1 -= 1
								if x1 == x2:
									break
								e = e - dy
								if e >= 0:	# déplacement diagonal
									y1 -= 1
									e += dx
						else:
							# vecteur oblique proche de la verticale, dans le 6e octant
							e = dy
							dy = e * 2
							dx = dx * 2  # e est négatif
							while 1 == 1:
								# déplacements verticaux
								tracePixel(x1, y1)
								y1 -= 1
								if y1 == y2:
									break
								e = e - dx
								if e >= 0:
									# déplacement diagonal
									x1 -= 1
									e += dy
				else:
					# sinon dy = 0 (et dx < 0)
					# vecteur horizontal vers la gauche
					while x1 != x2:
						tracePixel( x1, y1)
						x1 -= 1
		else:
			# dx = 0
			dy = y2 - y1
			if dy != 0:
				if dy > 0:
					# vecteur vertical croissant
					while y1 != y2:
						tracePixel( x1, y1)
						y1 += 1
				else: # dy < 0 (et dx = 0)
					# vecteur vertical décroissant
					while y1 != y2:
						tracePixel( x1, y1)
						y1 -= 1
		# le pixel final (x2, y2) n'est pas tracé.
				
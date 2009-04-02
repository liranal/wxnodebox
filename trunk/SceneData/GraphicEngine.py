#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

from euclid import *
from Map import *

X=0
Y=1

class GraphicEngine:
    def __init__(self, world):
        assert isinstance(world, World)
        self.world = world
        self.size = (0.,0.)
        self.area_size = (10,10)

    def update_actor(self, mouse_x, mouse_y):
        move = Vector2( (mouse_x - (self.size[X]/2.)) / self.area_size[X], \
                        (mouse_y - (self.size[Y]/2.)) / self.area_size[Y])
        self.world.actor.position += move
        
    def draw(self, ctx):
        """ 
        ctx = Context()
        """
        #ctx = Context()
        self.size = ( ctx.width, ctx.height)
        actor = self.world.actor
        # coordinates of corner up/left in the world
        coord = Point2( actor.position.x+actor.size - self.size[X]/(2. * self.area_size[X]), \
                        actor.position.y+actor.size - self.size[Y]/(2. * self.area_size[Y]))
        # coord in the world
        box = ( coord, coord + Vector2( self.size[X] / float(self.area_size[X]), \
                                        self.size[Y] / float(self.area_size[Y])) )
        # coord of area
        areas_box = ( (int(box[0].x), int(box[0].y)), \
                      (int(box[1].x), int(box[1].y)) )
        #box = ( (actor.position.x * self.area_size[X] - self.size[X] / 2., actor.position.y * self.area_size[Y] - self.size[Y] / 2.), \
        #        (actor.position.x * self.area_size[X] + self.size[X] / 2., actor.position.y * self.area_size[Y] + self.size[Y] / 2.))
        # draw each area
        coord_y = int( (math.floor(coord.y) - coord.y) * self.area_size[Y] )
        for y in range( areas_box[0][Y], areas_box[1][Y]):
            # coord_x : coord on the screen
            coord_x = int( (math.floor(coord.x) - coord.x) * self.area_size[X] )
            for x in range( areas_box[0][X], areas_box[1][X]):
                area = self.world.area(x,y)
                assert isinstance( area, Area)
                if len(filter(lambda x: isinstance(x,Wall),area.linked_elements)) != 0:
                    ctx.fill(0.5,0.5,0)
                    ctx.rect( coord_x, coord_y, self.area_size[X],self.area_size[Y])
                coord_x += self.area_size[X]
            coord_y += self.area_size[Y]
        # draw actor
        ctx.fill(0.8,0.1,0.1)
        position = ( actor.position - coord ) * self.area_size[X]
        ctx.rect( int(position.x), int(position.y), self.area_size[X],self.area_size[Y])

    
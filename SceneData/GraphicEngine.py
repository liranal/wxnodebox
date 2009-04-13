#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

from euclid import *
from World import *
from EventsManager import *

from PycairoDrawer import *

X=0
Y=1

class GraphicEngine:
    def __init__(self, world, events_manager):
        assert isinstance(world, World)
        assert isinstance(events_manager, EventsManager)
        self.world = world
        self.events = events_manager
        self.size = (0.,0.)
        self.area_size = (20,20)
        self.drawer = PycairoDrawer(None)

    def update_actor(self, mouse_x, mouse_y):
        # calculate aim moving vector
        actor = self.world.actor
        move = Vector2( ((mouse_x - (self.size[X] + (actor.size.x * self.area_size[X] / self.world.area_size))/2)
                        * self.world.area_size) / self.area_size[X], \
                        ((mouse_y - (self.size[Y] + (actor.size.y * self.area_size[Y] / self.world.area_size))/2)
                        * self.world.area_size) / self.area_size[Y])
        # event
        event = self.events.create_event( "ACTOR_AIM")
        event.aim = move

    def update_actor_gunfire(self, mouse_x, mouse_y):
        # calculate aim moving vector
        actor = self.world.actor
        move = Vector2( ((mouse_x - (self.size[X] + (actor.size.x * self.area_size[X] / self.world.area_size))/2)
                        * self.world.area_size) / self.area_size[X], \
                        ((mouse_y - (self.size[Y] + (actor.size.y * self.area_size[Y] / self.world.area_size))/2)
                        * self.world.area_size) / self.area_size[Y])
        # event
        event = self.events.create_event( "ACTOR_GUNFIRE")
        event.aim = move
    
    def draw(self, *args):
        """ 
	*args >>
        dc = Context()
        """
        ##########################################
        if len(args) != 1:
            raise Exception("Params Error")
        dc = args[0]
        self.drawer.update_init( *args)
        self.size = ( dc.GetSize().x, dc.GetSize().y)
        screen_size = Vector2( self.size[0], self.size[1])
        area_screen_size = Vector2( self.area_size[X], self.area_size[Y])
        ##########################################
        actor = self.world.actor
        # coordinates of corner up/left in the world
        ##coord = actor.position - screen_size.div_factor( (2./self.world.area_size) * area_screen_size)
        coord = actor.position - self.world.area_size * screen_size.div_factor( 2. * area_screen_size)
        # coord in the world
        box = ( coord, coord + self.world.area_size * screen_size.div_factor( area_screen_size))
        # coord of area
        areas_box = ( (int(box[0].x / self.world.area_size), int(box[0].y / self.world.area_size)), \
                      (int(box[1].x / self.world.area_size), int(box[1].y / self.world.area_size)) )
        # draw each area
        coord_y = int( (areas_box[0][Y] * self.world.area_size - coord.y) * (area_screen_size.y/self.world.area_size) )
        for y in range( areas_box[0][Y], areas_box[1][Y]+1):
            # coord_x : coord on the screen
            coord_x = int( (areas_box[0][X] * self.world.area_size - coord.x) * (area_screen_size.x/self.world.area_size) )
            for x in range( areas_box[0][X], areas_box[1][X]+1):
                area = self.world.area(x,y)
                assert isinstance( area, Area)
                if len(filter(lambda x: isinstance(x,Wall),area.linked_elements)) != 0:
                    self.drawer.color( 0.5, 0.5, 0.0)
                    self.drawer.rectangle( coord_x, coord_y, area_screen_size.x, area_screen_size.y)
                coord_x += area_screen_size.x
            coord_y += area_screen_size.y
        # draw actor
        ##actor_size = Vector2(actor.size, actor.size)
        ##actor_size = actor.size
        corner_position = ( actor.position - coord) * area_screen_size.x / self.world.area_size 
        self.drawer.color( 0.8, 0.1, 0.1)
        self.drawer.rectangle( int( corner_position.x), int( corner_position.y), area_screen_size.x, area_screen_size.y)
        # draw creature
        for creature in self.world.creatures_list:
            if self.isInside(creature.position, box):
                self.drawer.color( 0, 0, 1)
                ##creature_pos =
                ##creature_size =
                corner_position = ( creature.position - coord) * area_screen_size.x / self.world.area_size 
                self.drawer.rectangle( int( corner_position.x), int( corner_position.y), area_screen_size.x, area_screen_size.y)

    def isInside(self, position, box):
        """
        position = Point2()
        box = ( Point2(), Point2())
        """
        ## en 2D on a collision si xa2>xb1 And xa1<xb2 And ya2>yb1 And ya1<yb2
        if box[0].x <= position.x <= box[1].x and box[0].y <= position.y <= box[1].y:
            return True
        return False
        
        
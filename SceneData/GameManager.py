#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

from World import *
from GraphicEngine import *
from PhysicEngine import *

from EventsManager import *

class GameManager:
    def __init__(self):
        # first elements
        self.world = World()
        self.events = EventsManager()
        # second elements
        self.graphics = GraphicEngine( self.world, self.events)
        self.physics = PhysicEngine( self.world, self.events)
        
    def initialize_world(self, world_image):
        assert isinstance(self.world, World)
        assert isinstance(world_image, str)
        self.world.load_map_from_image( world_image)
        
    def turn(self):
        self.physics.turn()
        
    def draw_scene(self, *args):
        self.graphics.draw( *args)
        
if __name__ == '__main__':
    print 'start test - GameManager'
    game = GameManager()
    game.initialize_world( "Level0.png")
    print 'end test - GameManager'

    
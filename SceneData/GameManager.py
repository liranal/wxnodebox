#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

from Map import *
from GraphicEngine import *
from PhysicEngine import *

class GameManager:
    def __init__(self):
        self.world = World()
        self.graphics = GraphicEngine( self.world)
        self.physics = PhysicEngine()
        
    def initialize_world(self, world_image):
        assert isinstance(self.world, World)
        assert isinstance(world_image, str)
        self.world.load_map_from_image( world_image)
        
if __name__ == '__main__':
    print 'start test - GameManager'
    game = GameManager()
    game.initialize_world( "Level0.png")
    print 'end test - GameManager'

    
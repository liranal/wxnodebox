#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

class Creature(DrawCreature, PhysicCreature):
    # variables
    life = 50
    level = 1
    strength = 5
    dexterity = 5
    will = 5
    status_list = { 'wait':0, 'walk':1, 'fire':2, 'hurt':3, 'dead':4 }
    sprites_list = { 0:'wait.jpg', 1:'walk.jpg', 2:'fire.jpg', 3:'dead.jpg' }
    sprites_wait = ( 'wait.jpg' )
    sprites_walk = ( 'walk1.jpg', 'walk2.jpg', 'walk3.jpg' )
    sprites_fire = ( 'fire1.jpg', 'fire2.jpg', 'fire3.jpg' )
    sprites_hurt = ( 'hurt1.jpg', 'hurt2.jpg' )
    sprites_killed = ( 'kill1.jpg', 'kill2.jpg', 'kill3.jpg' )
    sprites_dead = ( 'dead.jpg' )
    
    def __init(self):
        self.position = Point2(0,0)
        self.direction = Vector2(1,0)
        self.status = 'wait'
        self.substatus = 0

    #def __init(self, draw, physics):
    #    pass
        
class DrawCreature:
    def draw(self):
        #self.drawer.color( 0, 0, 1)
        ##creature_pos =
        ##creature_size =
        #corner_position = ( self.position - coord) * area_screen_size.x / self.world.area_size 
        #self.drawer.rectangle( int( corner_position.x), int( corner_position.y), area_screen_size.x, area_screen_size.y)
        pass
    
class PhysicCreature:
    def move(self):
        pass
    
    def act(self):
        pass
    
    
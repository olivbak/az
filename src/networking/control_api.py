import pygame
vec = pygame.math.Vector2
from ..settings.settings import *

class control_api():
    def __init__(self,mapp,players):
        self.walls = mapp.get_walls()
        self.players = players 
        self.tanks = []

    def move_tank(self,dt,tank,command):
        tanks = []
        for player in self.players:
            if tank.id != player:
                tanks.append(self.players[player]['tank']) 

        if command == "up":
            tank.move(dt,vec(TANK_SPEED,0).rotate(-tank.rotation))
            if self.collide(tank,self.walls) or self.collide(tank,tanks):
                tank.move(dt,-vec(TANK_SPEED,0).rotate(-tank.rotation))
        elif command == "down":
            tank.move(dt,vec(-TANK_SPEED/2,0).rotate(-tank.rotation))
        


    def rotate_tank(self,dt,tank,command):
        if command == "left":
            tank.rotate(dt,ROTATION_SPEED)
        elif command == "right":
            tank.rotate(dt,-ROTATION_SPEED)
    
    def collide(self,tank,sprites):
        for sprite in sprites:
            if tank.hit_rect.colliderect(sprite.hit_rect):
                return True
            
        return False

import pygame
vec = pygame.math.Vector2
from ..settings.settings import *

class control_api():
    def __init__(self,mapp,players):
        self.walls = mapp.get_walls()
        self.players = players 
        self.tanks = []

    def update_tanks(self):
        tanks = []
        for player in self.players:
            tanks.append(self.players[player]['tank']) 

        self.tanks = tanks
    
    def get_opponents(self,tank):
        opponents = []
        for player in self.players:
            if player != tank.id:
                opponents.append(self.players[player]['tank'])
        return opponents

    def move_tank(self,dt,tank,command):
        opponents = self.get_opponents(tank)
        if command == "up":
            tank.move(dt,vec(TANK_SPEED,0).rotate(-tank.rotation))
            if self.collide(tank,self.walls) or self.collide(tank,opponents):
                tank.move(dt,-vec(TANK_SPEED,0).rotate(-tank.rotation))
        elif command == "down":
            tank.move(dt,vec(-TANK_SPEED/2,0).rotate(-tank.rotation))
            if self.collide(tank,self.walls) or self.collide(tank,opponents):
                tank.move(dt,-vec(-TANK_SPEED/2,0).rotate(-tank.rotation))
    

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

    def shoot(self,tank,time):
        tank.shoot(time)
    
    def reload(self,tank):
        tank.ready_to_fire = True
    
    def update_bullets(self,dt,time):
        for tank in self.tanks:
            for key in tank.bullets.copy():
                bullet = tank.bullets[key]['bullet']
                bullet.update(dt,time,self.walls)
                self.collide_bullets(bullet,self.get_opponents(tank)) 

    def collide_bullets(self,bullet,tanks):
        for tank in tanks:
            if tank.hit_rect.colliderect(bullet.hit_rect):
                print("hit!")
                tank.alive = False
                

import pygame
from ..settings.settings import *
vec = pygame.math.Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,dir,id,spawn_time,list):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/bullet.png")
        self.rect = self.image.get_rect()
        self.pos = pos
        self.id = id
        self.vel = dir*BULLET_SPEED
        self.list = list
        self.spawn_time = spawn_time
        self.rect.center = self.pos
        self.hit_rect = self.rect

    def update(self,dt,time,walls):
        self.move_x(dt,walls)
        self.move_y(dt,walls)
        self.rect.center = self.pos
        self.hit_rect = self.rect
        self.collide_wall(walls)
        if time - self.spawn_time > BULLET_LIFETIME:
            del self.list[self.id]
            #self.kill()
    
    def collide_wall(self,walls):
        for wall in walls:
            if wall.y*TILESIZE < self.pos.y and (wall.y*TILESIZE+TILESIZE) > self.pos.y and self.pos.x > wall.x*TILESIZE and self.pos.x < (wall.x*TILESIZE+TILESIZE):
                return True
        return False

    def move_x(self,dt,walls):
        self.pos.x += self.vel.x * dt
        if self.collide_wall(walls):
            self.pos.x -= self.vel.x * dt
            self.vel.x *= (-1)

    def move_y(self,dt,walls):
        self.pos.y += self.vel.y * dt
        if self.collide_wall(walls):
            self.pos.y -=self.vel.y * dt
            self.vel.y *= (-1)

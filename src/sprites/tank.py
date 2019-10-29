import pygame
from ..settings.settings import *
from .bullet import Bullet
vec = pygame.math.Vector2
#from bullet import Bullet

class Tank(pygame.sprite.Sprite):
    def __init__(self,pos,rotation,id):
        pygame.sprite.Sprite.__init__(self)
        self.id = id

        self.vel = vec(0,0)
        self.pos = pos
        self.rotation = rotation
        self.alive = True

        self.hit_rect = pygame.Rect(0,0,TILESIZE-10,TILESIZE-10)
        self.hit_rect.center = self.pos
        
        # init bullets
        self.bullets = {}
        self.next_bullet_id = 0
        
        self.ready_to_fire = True

        self.player_img = pygame.image.load("./images/sprite.png")
        
        self.org_image = pygame.transform.rotate(self.player_img,90)
        self.image = self.org_image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
        self.image = pygame.transform.rotate(self.org_image,self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def shoot(self,time): 
        if self.ready_to_fire and len(self.bullets)<BULLET_CAP:
            dir = vec (1,0).rotate(-self.rotation)
            self.bullets[self.next_bullet_id] = {'bullet': 
                    Bullet(vec(self.pos),dir,self.next_bullet_id
                        ,time,self.bullets)}
            self.next_bullet_id += 1
            self.ready_to_fire = False
            
    def move(self,dt,dpos):
        self.pos += dpos * dt 
        self.rect.center = self.pos
        self.hit_rect.center = self.pos

    def rotate(self,dt,drot):
        self.rotation += (drot*dt) % 360
        self.image = pygame.transform.rotate(self.org_image,self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self,dt=0,opponents=[],walls=[]):
        self.move(dt)
        self.rotate(dt)
    
    def collide(self,sprites):
        for sprite in sprites:
            pass

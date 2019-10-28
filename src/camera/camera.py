import pygame
from ..settings.settings import *

class Camera:
    def __init__(self,width,height):
        self.camera = pygame.Rect(0,0,width,height)
        self.width = width
        self.height = height

    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)

    def deply(self,rect):
        return rect.move(self.camera.topleft)

    def update(self,target):
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGTH/2)

        x = min(0,x)
        y = min(0,y)
        x = max (-(self.width-WIDTH),x)
        y = max (-(self.height-HEIGTH),y)
        self.camera = pygame.Rect(x,y,self.width,self.height)

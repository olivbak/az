import pygame
from ..settings.settings import *
vec = pygame.math.Vector2

class Wall(pygame.sprite.Sprite):
    def __init__(self,group,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.groups = group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.hit_rect = self.rect



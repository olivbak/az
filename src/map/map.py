import pygame
from ..settings.settings import *
from ..sprites.wall import Wall


class Map:
    def __init__(self,filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line)
 
        self.tileheight = len(self.data)
        self.tilewidth = len(self.data[0])
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight* TILESIZE

    def get_walls(self):
        walls = pygame.sprite.Group()
        for row, tiles in enumerate(self.data):
            for col,tile in enumerate(tiles):
                if tile =='1':
                    Wall([walls],col,row)
        return walls

import pygame
from ..sprites.tank import Tank

class convert_client_data():
    def __init__(self):
        pass
    
    def get_tanks_from_server_data(self,data):
        tanks = pygame.sprite.Group()
        for dic in data:
            tanks.add(Tank (dic["pos"],dic["rotation"],dic["id"]))
        return tanks


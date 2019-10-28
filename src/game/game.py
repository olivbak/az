import pygame
from os import path
from ..settings.settings import *
from ..map.map import *
from ..networking.client import Network
from ..sprites.wall import Wall
from ..sprites.tank import Tank
from ..camera.camera import Camera
from ..data.convert_client_data import convert_client_data
#from ..sprites.bullet import Bullet

class Game():
    def __init__(self,ip):
        # SETUP pygame environment
        pygame.init()
        pygame.mixer.quit()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        self.clock = pygame.time.Clock()
        self.convert_data = convert_client_data() 
        #SETUP CONNECTION TO SERVER
        self.network = Network(ip)

        # Get initializing data from server
        self.start = self.network.getInit()
        if not self.start:
            self.quit()

        self.map = self.start["map"]
        self.playerid = self.start["id"]

        # Initialize map
        self.walls = self.map.get_walls()

        # Initialize pygame Sprites
        self.tanks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        
        # Initialize camera
        self.camera = Camera(self.map.width,self.map.height)
        #Launch the program
        self.run()
    


    def paint(self):
        self.screen.fill(BACKGROUNDCOLOR)

        for j,sprite in enumerate(self.walls):
            self.screen.blit(sprite.image,self.camera.apply(sprite))

        for sprite in self.tanks:
            self.screen.blit(sprite.image,self.camera.apply(sprite))
            #sprite.update()

        pygame.display.flip()

    def events(self):
        self.drot = 0
        self.dpos = (0,0)
        reply = ["nothing "]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            reply.append("rotate left")
        if keys[pygame.K_RIGHT]:
            reply.append("rotate right")
        if keys[pygame.K_UP]:
            reply.append("move up")
        if keys[pygame.K_DOWN]:
            reply.append("move down")
        return reply 
                    

    def update(self):
        self.walls.update() 
        command = self.events()
        self.data = self.network.send({"command":command,"dt":self.dt})
        self.tanks = self.convert_data.get_tanks_from_server_data(self.data)
        self.tank = self.get_my_tank(self.tanks)
        if not self.tank:
            self.quit()

        self.camera.update(self.tank)
        self.paint()
    
    def get_my_tank(self,tanks):
        for tank in tanks:
            if tank.id == self.playerid:
                return tank
        return None

    def quit(self):
        pygame.quit()
        exit()
    
    def run(self):
        self.run = True
        while self.run:
            self.dt = self.clock.tick(FPS) / 1000
            self.update()

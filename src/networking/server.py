import socket
from _thread import *
import sys
print(__name__)
from ..sprites.tank import Tank
import pickle
from .ip_address import Ip_address
from ..map.map import Map
from ..settings.settings import *
from ..data.server_to_client_data import server_to_client_data
from .control_api import control_api
import pygame
#from send_data import Data
vec = pygame.math.Vector2


class Server:
    def __init__(self,server,port):
        self.server = server
        self.port = port
        self.players = {}
        self.disconnected = []
        self.map = Map("./maps/map.txt") 
        self.tanks = pygame.sprite.Group() 
        self.control_api = control_api(self.map,self.players)
        self.convertdata = server_to_client_data()

    def setup(self):
        start_new_thread(self.game_loop,())
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_IP,socket.SO_REUSEADDR,1)

        try:
            self.s.bind((self.server,self.port))
        except socket.error as e:
            str(e)
        
        self.s.listen()
        print('Waiting for connection. Server started at ip:',self.server)
   
    """
    functions
    """

    def evaluate_input(self,playerid,input):
        tank = self.get_tank_from_playerid(playerid)

        for data in input["command"]:
            command  = data.split(" ") 

            if command[0] == "move":
                self.control_api.move_tank(self.dt,tank,command[1])
            elif command[0] == "rotate":
                self.control_api.rotate_tank(self.dt,tank,command[1])
            elif command[0] == "shoot":
                self.control_api.shoot(tank,self.time)
            elif command[0] == 'reload':
                self.control_api.reload(tank)

    def get_tank_from_playerid(self,playerid):
        return self.players[playerid]["tank"]

    """
    Server handling
    """
    def threaded_client(self,conn, playerid):
        print('working')
        self.players[playerid] = {"tank":Tank((300,300),0,playerid)}
        conn.send(pickle.dumps({"map":self.map,"id":playerid}))
        reply = ""
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                self.evaluate_input(playerid,data)
                if not data:
                    print("Disconnected:",conn)
                    #del self.players[playerid]
                    print("removed playa")
                    break
                else:

                    reply = {'tanks':self.convertdata.convert_tankdata_to_nonpygame_data(self.players),'bullets':self.convertdata.convert_bulletdata_to_nonpygame_data(self.players)}

                conn.sendall(pickle.dumps(reply))
                    
            except Exception as e:
                print(repr(e))
                break

        # When players disconnect

        print("Lost connection")
        try:
            del self.players[playerid]
        except Exception as e:
            pass

        conn.close()
        self.disconnected.append(playerid) 

    def server_loop(self):
        self.running = True
        ## This loop checks for new connections

        currentPlayer = 0

        while self.running:
            conn, addr = self.s.accept()
            print("Connected to", addr)
            ## If new connection - establish connection
            start_new_thread(self.threaded_client,(conn,currentPlayer))
            currentPlayer += 1
    
    def update(self):
        self.control_api.update_tanks()
        self.control_api.update_bullets(self.dt,self.time)

        #Temporary kill mechanic, that shuts down client when it dies:
        for key in self.players.copy():
            if not self.players[key]['tank'].alive:
                del self.players[key]

    def game_loop(self):
        pygame.init()
        pygame.mixer.quit()
        clock = pygame.time.Clock()

        while self.running:
            self.dt = clock.tick(FPS) / 1000
            self.time = pygame.time.get_ticks()
            self.update() 

ip = Ip_address()


server = Server(ip.get_ip(),5555)
server.setup()
server.server_loop()

server.shutdown(socket.SHUT_RDWR)
server.close()

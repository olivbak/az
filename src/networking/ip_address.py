import socket

class Ip_address:
    def __init__(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',1))
        self.local_ip = s.getsockname()[0]
    
    def get_ip(self):
        return self.local_ip



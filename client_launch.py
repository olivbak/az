import sys

from src.game.game import *
if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv)==2:
        n = Game(sys.argv[1])
    else:
        print('Invalid argv. Execute program as python3 "file" "ip"')

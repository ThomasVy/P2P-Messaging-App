# main.py file 
# CPSC 559 Project
# By Zachery Sims & Thomas Vy

from socketCommunication import SocketCommunication

def main() -> None:
    socketCommunication = SocketCommunication()
    socketCommunication.start()

if __name__ == '__main__':
    main()


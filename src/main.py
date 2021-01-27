# main.py file 
# Used to run the main application
# CPSC 559 Project
# By Zachery Sims & Thomas Vy

from socketCommunication import SocketCommunication
import asyncio

def main() -> None:
    socketCommunication = SocketCommunication()
    asyncio.run(socketCommunication.start())

if __name__ == '__main__':
    main()


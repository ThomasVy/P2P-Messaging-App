# socketCommunication.py file 
# CPSC 559 Project
# By Zachery Sims & Thomas Vy

import os
import socket
from typing import Tuple, no_type_check
from collections import namedtuple
from datetime import datetime

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 55921        # Port to listen on (non-privileged ports are > 1023)
TEAM_NAME = "Zomas"

Source = namedtuple('Source', 'address dateReceived numPeers peers')

class SocketCommunication: 
    def __init__(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sources = []

    def start(self) -> None:
        self.__sock.connect((HOST, PORT))
        while True:
            data = self.receiveRequest()
            response = self.processRequest(data)
            if not response:
                break
            self.sendResponse(response)
        self.__sock.close()

    def receiveRequest(self) -> str:
        data = self.__sock.recv(1024)
        data = data.decode('utf-8')
        print("Received", f'"{data}"')
        return data

    def sendResponse(self, response: str) -> None:
        print("Sending", f'"{response}"')
        self.__sock.sendall(str.encode(response))

    def processRequest(self, data: str) -> str:
        request = data.split('\n')
        requestType = request[0]
        response = ""
        if (requestType == "get team name"):
           response = TEAM_NAME + '\n'
        elif (requestType == "get code"):
            #TODO Thomas Add more files once first iteration is completed
            currentLocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            files = [f for f in os.listdir(currentLocation) if os.path.isfile(os.path.join(currentLocation, f))]
            response = "Python\n"
            for file in files:
                with open(os.path.join(currentLocation, file), 'r') as f:
                    response += f.read()
            response += "\n...\n"
        elif (requestType == "receive peers"):
            #TODO Zach make this less jank and maybe change the recieveRequest() method so that we arent misusing it (or write a new one?)
            peerData = self.receiveRequest().split('\n')
            address = HOST
            dateReceived = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            numPeers = peerData[0]
            peers = []
            for i in range(int(numPeers)):
                peers.append(peerData[i + 1])
            self.__sources.append(Source(address, dateReceived, numPeers, peers))
            return
        elif (requestType == "get report"):
            pass #TODO Zach
        elif (requestType == "close"):
            pass
        return response
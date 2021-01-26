# socketCommunication.py file 
# CPSC 559 Project
# By Zachery Sims & Thomas Vy

import socket
from craftResponseUtils import getCode, getReport, getTeamName, Source
from typing import Tuple, no_type_check
from datetime import datetime

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 55921        # Port to listen on

class SocketCommunication: 
    def __init__(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sources = []
        self.__socketOpen = False

    def start(self) -> None:
        self.__sock.connect((HOST, PORT))
        self.__socketOpen = True
        while self.__socketOpen:
            data = self.receiveRequest()
            response = self.processRequest(data)
            if response:
                self.sendResponse(response)

    def receiveRequest(self) -> str:
        data = self.__sock.recv(1024, socket.MSG_WAITALL)
        data = data.decode('utf-8')
        print("Received", f'"{data}"')
        return data

    def sendResponse(self, response: str) -> None:
        print("Sending", f'"{response}"')
        self.__sock.sendall(str.encode(response))

    def receivePeers(self) -> str:
        #TODO Zach make this less jank and maybe change the recieveRequest() method so that we arent misusing it (or write a new one?)
        peerData = self.receiveRequest().split('\n')
        address = str(self.__sock.getsockname()[0]) + ":" + str(self.__sock.getsockname()[1])
        dateReceived = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        numPeers = peerData[0]
        peers = []
        for i in range(int(numPeers)):
            peers.append(peerData[i + 1])
        self.__sources.append(Source(address, dateReceived, numPeers, peers))

    def processRequest(self, data: str) -> str:
        request = data.split('\n')
        requestType = request[0]
        response = ""
        if (requestType == "get team name"):
            response = getTeamName()
        elif (requestType == "get code"):
            response = getCode()
        elif (requestType == "receive peers"):
           self.receivePeers()
        elif (requestType == "get report"):
            response = getReport(self.__sources)
        elif (requestType == "close"):
            self.__sock.close()
            self.__socketOpen = False
        return response
# socketCommunication.py file 
# CPSC 559 Project
# By Zachery Sims & Thomas Vy

from craftResponseUtils import getCode, getReport, getTeamName, Source
from typing import Tuple, no_type_check
from datetime import datetime
import asyncio

HOST = "localhost"  # Standard interface address
PORT = 55921        # Port to listen on

#Socket Communication class is used to communicate with the Registry.
class SocketCommunication: 
    def __init__(self):
        self.__sources = []
        self.__socketOpen = False

    async def start(self) -> None:
        self.__reader, self.__writer = await asyncio.open_connection(HOST, PORT)
        self.__socketOpen = True
        while self.__socketOpen: #Loop until the socket is closed by the close message
            data = await self.receiveMessage()
            response = await self.processRequest(data)
            if response:
                await self.sendResponse(response)

    # Reads a line of the socket and strips off the new line
    async def receiveMessage(self) -> str:
        data = await self.__reader.readline()
        data = data.decode('utf-8').split('\n')[0]
        print("Received", f'"{data}"')
        return data

    # Writes to the socket with supplied message
    async def sendResponse(self, response: str) -> None:
        print("Sending", f'"{response}"')
        self.__writer.write(response.encode())
        await self.__writer.drain()

    #Grabs the peer list from the source and puts the list in a member variable
    async def receivePeers(self) -> str:
        address = str(HOST) + ":" + str(PORT)
        dateReceived = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        numPeers = await self.receiveMessage()
        peers = []
        for i in range(int(numPeers)):
            peer = await self.receiveMessage()
            peers.append(peer)
        self.__sources.append(Source(address, dateReceived, numPeers, peers))

    # Processes the request and reacts to the message accordingly.
    async def processRequest(self, requestType: str) -> str:
        response = ""
        if (requestType == "get team name"):
            response = getTeamName()
        elif (requestType == "get code"):
            response = getCode()
        elif (requestType == "receive peers"):
           await self.receivePeers()
        elif (requestType == "get report"):
            response = getReport(self.__sources)
        else: # (requestType == "close" or anything unexpected)
            self.__writer.close()
            await self.__writer.wait_closed()
            self.__socketOpen = False
        return response
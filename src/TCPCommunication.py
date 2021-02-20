# socketCommunication.py file 
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
import asyncio
from datetime import datetime
from address import Address
from source import Source

#TCP communication class is used to communicate with the Registry.
class TCPCommunication: 
    def __init__(self, TCPAddress: Address):
        self.__open = False
        self.__address = TCPAddress

    async def openConnection(self):
        self.__open = True
        self.__reader, self.__writer = await asyncio.open_connection(
            self.__address.ip,
            self.__address.port)

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

    #Grabs the peer list from the source
    async def receivePeers(self) -> Source:
        dateReceived = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        numPeers = await self.receiveMessage()
        peers = []
        for i in range(int(numPeers)):
            peers.append(await self.receiveMessage())
        return Source(self.__address, dateReceived, peers)

    async def closeSocket(self) -> None:
        self.__writer.close()
        self.__open = False
        
    @property
    def open(self) -> bool:
        return self.__open
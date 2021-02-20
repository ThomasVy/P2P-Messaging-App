from peerInfo import PeerInfo
from address import Address
import craftResponseUtils
from TCPCommunication import TCPCommunication
from UDPServer import UDPServer
import asyncio

class TwitterApplication:
    def __init__(self) -> None:
        self.__peerInfo = PeerInfo()
        registryIP = input("Enter Registry Address: ")
        registryPort = int(input("Enter Registry Port Address: "))
        self.__teamName = input("Enter Team Name: ")
        self.__registryAddress = Address(registryIP, registryPort)
        self.__TCPCommunication = TCPCommunication(self.__registryAddress)
        UDPServerIP = input("Enter UDP Server Address: ")
        UDPServerPort = int(input("Enter UDP Server Port Address: "))
        self.__UDPServer = UDPServer(Address(UDPServerIP, UDPServerPort))

    def start(self) -> None:
        self.__UDPServer.startServer()
        asyncio.run(self.contactRegistry())

    async def contactRegistry(self) -> None:
        await self.__TCPCommunication.openConnection()
        while self.__TCPCommunication.open: #Loop until the socket is closed by the close message
            data = await self.__TCPCommunication.receiveMessage()
            await self.processRequest(data)

    # Processes the request and reacts to the message accordingly.
    async def processRequest(self, requestType: str) -> None:
        response = ""
        if (requestType == "get team name"):
            response = craftResponseUtils.getTeamName(self.__teamName)
        elif (requestType == "get code"):
            response = craftResponseUtils.getCode()
        elif (requestType == "receive peers"):
           self.__peerInfo.addSource(await self.__TCPCommunication.receivePeers(self.__registryAddress))
        elif (requestType == "get report"):
            response = craftResponseUtils.getReport(self.__peerInfo)
        elif (requestType == "get location"):
            response = craftResponseUtils.getLocation(self.__UDPServer.address)
        else: # (requestType == "close" or anything unexpected)
            await self.__TCPCommunication.closeSocket()
        if response:
            await self.__TCPCommunication.sendResponse(response)
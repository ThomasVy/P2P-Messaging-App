# registryCommunicator.py file 
# This class will be used to communicate with registry
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
import craftResponseUtils
from address import Address
from TCPCommunication import TCPCommunication
from peerInfo import PeerInfo
from UDPServer import UDPServer

class RegistryCommunicator:
    def __init__(self, peerInfo: PeerInfo, UDPServer: UDPServer) -> None:
        self.__peerInfo = peerInfo
        self.__UDPServer = UDPServer
        self.__teamName = input("Enter Team Name: ")
        self.__registryAddress = Address(input("Enter IP and Port: "))
        self.__TCPCommunication = TCPCommunication(self.__registryAddress)

    async def start(self) -> None:
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
           self.__peerInfo.addSourceFromTCP(await self.__TCPCommunication.receivePeers())
        elif (requestType == "get report"):
            response = craftResponseUtils.getReport(self.__peerInfo)
        elif (requestType == "get location"):
            response = craftResponseUtils.getLocation(self.__UDPServer.address)
        else: # (requestType == "close" or anything unexpected)
            await self.__TCPCommunication.closeSocket()
        if response:
            await self.__TCPCommunication.sendResponse(response)

    @property
    def teamName(self) -> str:
        return self.__teamName


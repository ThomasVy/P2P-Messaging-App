import craftResponseUtils
from address import Address
from TCPCommunication import TCPCommunication
from peerInfo import PeerInfo
from snippet import Snippet

class RegistryCommunicator:
    def __init__(self, peerInfo: PeerInfo, UDPServerAddress: Address, snippetList: set([Snippet])) -> None:
        self.__peerInfo = peerInfo
        self.__snippetList = snippetList
        self.__UDPServerAddress = UDPServerAddress
        self.__teamName = input("Enter Team Name: ")
        self.__registryAddress = Address("localhost:55920")
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
            response = craftResponseUtils.getReport(self.__peerInfo, self.__snippetList)
        elif (requestType == "get location"):
            response = craftResponseUtils.getLocation(self.__UDPServerAddress)
        else: # (requestType == "close" or anything unexpected)
            await self.__TCPCommunication.closeSocket()
        if response:
            await self.__TCPCommunication.sendResponse(response)
from peerInfo import PeerInfo
from address import Address
from craftResponseUtils import getCode, getReport, getTeamName

from socketCommunication import SocketCommunication

class TwitterApplication:
    def __init__(self) -> None:
        self.__peerInfo = PeerInfo()
        self.__socket = SocketCommunication()

    async def start(self) -> None:
        ip = input("Enter Host Address: ")
        port = int(input("Enter Host Port Address: "))
        self.__teamName = input("Enter Team Name: ")
        self.__address = Address(ip, port)
        await self.__socket.openConnection(ip, port)

        while self.__socket.open: #Loop until the socket is closed by the close message
            data = await self.__socket.receiveMessage()
            await self.processRequest(data)
           
    # Processes the request and reacts to the message accordingly.
    async def processRequest(self, requestType: str) -> None:
        response = ""
        if (requestType == "get team name"):
            response = getTeamName(self.__teamName)
        elif (requestType == "get code"):
            response = getCode()
        elif (requestType == "receive peers"):
           self.__peerInfo.addSource(await self.__socket.receivePeers(self.__address))
        elif (requestType == "get report"):
            response = getReport(self.__peerInfo)
        else: # (requestType == "close" or anything unexpected)
            await self.__socket.closeSocket()
        if response:
            await self.__socket.sendResponse(response)
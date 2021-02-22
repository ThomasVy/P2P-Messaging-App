from peerInfo import PeerInfo
from address import Address
import socket
from UDPServer import UDPServer
from registryCommunicator import RegistryCommunicator
import asyncio

class GroupCommunicator:
    def __init__(self) -> None:
        self.__peerInfo = PeerInfo()
        self.__UDPServer = UDPServer(self.__peerInfo)
        self.__registryCommunicator = RegistryCommunicator(self.__peerInfo,
            self.__UDPServer.address)
                
    def bMulticast(self, message: str) -> None:
        for peer in self.__peerInfo.totalPeerList:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f"Sending {message} to {peer}")
            sock.sendto(message.encode(), (peer.ip, peer.port))

    async def start(self) -> None:
        self.__UDPServer.startServer()
        await self.__registryCommunicator.start()
        self.bMulticast("unga bunga")
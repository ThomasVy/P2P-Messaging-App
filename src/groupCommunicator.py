from peerInfo import PeerInfo
import socket
from UDPServer import UDPServer
from registryCommunicator import RegistryCommunicator
import asyncio

class GroupCommunicator:
    def __init__(self) -> None:
        self.__peerInfo = PeerInfo()
        self.__UDPServer = UDPServer()
        self.__registryCommunicator = RegistryCommunicator(self.__peerInfo,
            self.__UDPServer.address)
                
    def bMulticast(self, message: str) -> None:
        for peer in self.__peerInfo.totalPeerList:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f"Sending {message} to {peer}")
            sock.sendto(message.encode(), (peer.ip, peer.port))

    def start(self) -> None:
        self.__UDPServer.startServer()
        loop = asyncio.get_event_loop()
        loop.create_task(self.__registryCommunicator.start())
        loop.run_forever()
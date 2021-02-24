from peerInfo import PeerInfo
import socket
from UDPServer import UDPServer
from registryCommunicator import RegistryCommunicator
import threading
import time

class GroupCommunicator:
    def __init__(self) -> None:
        self.__shutdown = False
        self.__peerInfo = PeerInfo()
        self.__UDPServer = UDPServer(self.__peerInfo)
        self.__registryCommunicator = RegistryCommunicator(self.__peerInfo,
            self.__UDPServer.address)
                
    def bMulticast(self, message: str) -> None:
        for peer in self.__peerInfo.activePeerList:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f"Sending {message} to {peer}")
            sock.sendto(message.encode(), (peer.ip, peer.port))

    async def start(self) -> None:
        self.__UDPServer.startServer()
        await self.__registryCommunicator.start()
        periodicSendPeerMessageThread = threading.Thread(target=self.periodicallySendPeerMessage)
        periodicSendPeerMessageThread.daemon = True
        periodicSendPeerMessageThread.start()

    def periodicallySendPeerMessage(self) -> None:
        while not self.__shutdown:
            for peer in self.__peerInfo.activePeerList:
                peerMessage = f'peer{peer}'
                self.bMulticast(peerMessage)
                time.sleep(1)
            time.sleep(60)# sleep for 60 seconds

    @property
    def shutdown(self) -> bool:
        return self.__shutdown

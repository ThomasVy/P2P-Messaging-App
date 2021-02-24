from peerInfo import PeerInfo
import socket
from UDPServer import UDPServer
from registryCommunicator import RegistryCommunicator
import threading
import time
from source import Source
from address import Address

class GroupCommunicator:
    def __init__(self) -> None:
        self.__shutdown = False
        self.__peerInfo = PeerInfo()
        self.__UDPServer = UDPServer()
        self.__registryCommunicator = RegistryCommunicator(self.__peerInfo,
            self.__UDPServer.address)
                
    def bMulticast(self, message: str) -> None:
        for peer in self.__peerInfo.peerList:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f"Sending {message} to {peer}")
            sock.sendto(message.encode(), (peer.ip, peer.port))

    async def start(self) -> None:
        self.__UDPServer.startServer()
        await self.__registryCommunicator.start()
        periodicSendPeerMessageThread = threading.Thread(target=self.periodicallySendPeerMessage)
        periodicSendPeerMessageThread.daemon = True
        periodicSendPeerMessageThread.start()

        periodicReadMessageQueueThread = threading.Thread(target=self.processMessageQueue)
        periodicReadMessageQueueThread.daemon = True
        periodicReadMessageQueueThread.start()

    def processMessageQueue(self) -> None:
        while not self.__shutdown:
            while self.__UDPServer.messageQueue: #process all messages in the queue
                message = self.__UDPServer.messageQueue.pop()
                if message.type == "snip":
                    pass
                    #TODO: add the tweet as a snippet
                elif message.type == "peer":
                    self.__peerInfo.addSourceFromUDP(
                        Source(message.source, message.timestamp, set([Address(message.body)])))
                    #TODO: add the new peers and the source
                elif message.type == "stop":
                    self.__shutdown = True
            time.sleep(5)

    def periodicallySendPeerMessage(self) -> None:
        while not self.__shutdown:
            for peer in self.__peerInfo.peerList.copy():
                peerMessage = f'peer{peer}'
                self.bMulticast(peerMessage)
                time.sleep(1)
            time.sleep(60)# sleep for 60 seconds

    @property
    def shutdown(self) -> bool:
        return self.__shutdown

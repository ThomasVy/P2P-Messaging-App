from address import Address
from peer import Peer
import threading
from datetime import datetime
from message import Message
import socket
from peerInfo import PeerInfo
from source import Source

class UDPServer:
    def __init__(self, peerInfo: PeerInfo) -> None:
        self.__address = Address("localhost:"+input("Enter UDP Server Port Address: "))
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((self.__address.ip, self.__address.port))
        self.__serverThread = threading.Thread(target=self.serve)
        self.__socketClosed = False
        self.__messageQueue = []

    def startServer(self) -> None:
        self.__serverThread.start()
        print("Starting UDP server in thread:", self.__serverThread.name)

    def shutdownServer(self) -> None:
        self.__socket.close()
        self.__socketClosed = True

    def serve(self) -> None:
        while not self.__socketClosed:
            data, addr = self.__socket.recvfrom(1024) # buffer size is 1024 bytes
            message = data.decode('utf-8').split('\n')[0]
            sourceAddress = Address(f'{addr[0]}:{addr[1]}')
            dateReceived = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.__messageQueue.append(Message(message, sourceAddress, dateReceived))

    def bMulticast(self, messageText: str, peerInfo: PeerInfo) -> None:
        for peer in peerInfo.peerList.copy():
            dateSent = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            message = Message(messageText, peer, dateSent)
            self.logMessageSent(message, peerInfo)
            self.__socket.sendto(messageText.encode(), (peer.ip, peer.port))

    def logMessageSent(self, message: Message, peerInfo: PeerInfo) -> None:
        if message.type == "peer":
            peerInfo.logPeerMessage(Source(message.source, message.timestamp, set([Peer(Address(message.body))])))
        
    @property
    def address(self) -> Address:
        return self.__address
    
    @property
    def messageQueue(self) -> list([Message]):
        return self.__messageQueue
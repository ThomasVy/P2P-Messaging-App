from address import Address
from peer import Peer
import threading
from datetime import datetime
from message import Message
import socket
from peerInfo import PeerInfo
from source import Source
from requests import get

class UDPServer:
    def __init__(self, peerInfo: PeerInfo) -> None:
        ip = socket.gethostbyname(socket.gethostname())
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((ip, 0)) #bind to any available port
        self.__address = Address(f"{ip}:{self.__socket.getsockname()[1]}")
        print("UDP Server is at " + str(self.__address))

        self.__serverThread = threading.Thread(target=self.serve)
        self.__socketClosed = False
        self.__socketLock = threading.Lock()
        self.__messageQueue = []

    def startServer(self) -> None:
        self.__serverThread.start()
        print("Starting UDP server in thread:", self.__serverThread.name)

    def shutdownServer(self) -> None:
        self.__socketLock.acquire()
        self.__socketClosed = True
        self.__socket.close()
        self.__socketLock.release()

    def serve(self) -> None:
        while not self.__socketClosed:
            # will unblock from recvfrom when socket is closed
            data, addr = self.__socket.recvfrom(1024) # buffer size is 1024 bytes
            data = data.decode('utf-8').split('\n')[0]
            sourceAddress = Address(f'{addr[0]}:{addr[1]}')
            dateReceived = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            message = Message(data, sourceAddress, dateReceived)
            self.__messageQueue.append(message)
            if (message.type == "stop"):
                self.shutdownServer()
        print("UDP server Thread exiting")

    def bMulticast(self, messageText: str, peerInfo: PeerInfo) -> None:
        for peer in peerInfo.peerList.copy():
            dateSent = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            message = Message(messageText, peer, dateSent)
            self.__socketLock.acquire()
            if not self.__socketClosed: # don't use the socket if it is closed.
                self.logMessageSent(message, peerInfo)
                self.__socket.sendto(messageText.encode(), (socket.gethostbyname(peer.ip), peer.port))
            self.__socketLock.release()

    def logMessageSent(self, message: Message, peerInfo: PeerInfo) -> None:
        if message.type == "peer":
            peerInfo.logPeerMessage(Source(message.source, message.timestamp, set([Peer(Address(message.body))])))
        
    @property
    def address(self) -> Address:
        return self.__address
    
    @property
    def messageQueue(self) -> list([Message]):
        return self.__messageQueue
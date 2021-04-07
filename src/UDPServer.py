# UDPServer.py file 
# UDP Server for communicating therough UDP sockets
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
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
        self.__peerInfo = peerInfo
        ip = socket.gethostbyname(socket.gethostname()) #Grab the external IP address
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Use UDP
        self.__socket.bind((ip, 0)) #use the external IP address and bind to any available port
        self.__address = Address(f"{self.__socket.getsockname()[0]}:{self.__socket.getsockname()[1]}")
        print("UDP Server is at " + str(self.__address))
        self.__serverThread = threading.Thread(target=self.serve)  #thread for receiving peer messages
        self.__socketClosed = False #signal that the socket is closed
        self.__socketLock = threading.Lock()
        self.__messageQueue = [] #UDP message queue

    #starts the UDP server
    def startServer(self) -> None:
        self.__serverThread.start()

    #shutdown the UDP server/socket
    def shutdownServer(self) -> None:
        with self.__socketLock:
            self.__socketClosed = True
            self.__socket.sendto("shutdown".encode(),
                (socket.gethostbyname(self.__address.ip), self.__address.port))
            self.__socket.close()

    def serve(self) -> None:
        while not self.__socketClosed:
            # will unblock from recvfrom when socket is closed
            data, addr = self.__socket.recvfrom(1024) # buffer size is 1024 bytes
            data = data.decode('utf-8').split('\n')[0]
            sourceAddress = Address(f'{addr[0]}:{addr[1]}')
            dateReceived = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            message = Message(data, sourceAddress, dateReceived)
            self.__messageQueue.append(message)
        print("server thread ending")

    def sendMessage(self, message: Message) -> None:
        with self.__socketLock:
            if not self.__socketClosed: # don't use the socket if it is closed.
                self.__socket.sendto(str(message).encode(),
                (socket.gethostbyname(message.source.ip), message.source.port))
                self.logMessageSent(message) #log the message that was sent

    #Send the message supplied to all active peers 
    def bMulticast(self, messageText: str) -> None:
        for peer in self.__peerInfo.activePeerList:
            dateSent = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            message = Message(messageText, peer, dateSent)
            self.sendMessage(message)

    #log messages that were sent
    def logMessageSent(self, message: Message) -> None:
        if message.type == "peer": #currently only log the peer messages
            self.__peerInfo.logPeerMessage(Source(message.source, message.timestamp,
             set([Peer(Address(message.body))])))
        
    @property
    def address(self) -> Address:
        return self.__address
    
    @property
    def messageQueue(self) -> list([Message]):
        return self.__messageQueue


from address import Address
import threading
import socketserver
from datetime import datetime
from message import Message

class UDPRequestHandler(socketserver.DatagramRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        message = data.decode('utf-8').split('\n')[0]
        sourceAddress = Address(f'{self.client_address[0]}:{self.client_address[1]}')
        dateReceived = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.server.messageQueue.append(Message(message, sourceAddress, dateReceived))

class ThreadedUDPServer(socketserver.ThreadingUDPServer):
    def __init__(self, address: tuple, requestHandler: socketserver.BaseRequestHandler) -> None:
        super().__init__(address, requestHandler)
        self.messageQueue = []

class UDPServer:
    def __init__(self) -> None:
        self.__address = Address("localhost:"+input("Enter UDP Server Port Address: "))
        self.__server = ThreadedUDPServer((self.__address.ip, self.__address.port), UDPRequestHandler)
        self.__serverThread = threading.Thread(target=self.__server.serve_forever)
        # Exit the server thread when the main thread terminates
        self.__serverThread.daemon = True

    def startServer(self) -> None:
        self.__serverThread.start()
        print("Starting UDP server in thread:", self.__serverThread.name)

    def shutdownServer(self) -> None:
        self.__server.shutdown()
        #may have to kill the thread.. 

    @property
    def address(self) -> Address:
        return self.__address
    
    @property
    def messageQueue(self) -> list([Message]):
        return self.__server.messageQueue
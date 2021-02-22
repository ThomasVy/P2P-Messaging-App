from address import Address
from peerInfo import PeerInfo
import threading
import socketserver
from datetime import datetime

class UDPRequestHandler(socketserver.DatagramRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def handle(self):
        print("handling a message")
        #TODO: send this message to be sent to the executor
        dateReceived = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = self.request[0].strip()
        socket = self.request[1]
        print(f'{self.client_address[0]} wrote: {data}')
        #this is where we should process what type of request: peer, snip, or stop message
        #socket.sendto(data.upper(), self.client_address)

    def executeMessageRead(self, messageType: str, messageBody: str):
        if messageType == "snip":
            pass
            #TODO: add the tweet as a snippet
        elif messageType == "peer":
            pass
            #TODO: add the new peers and the source
        elif messageType == "stop":
            pass
            #TODO: close the connection with this peer

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

class UDPServer:
    def __init__(self, peerInfo: PeerInfo) -> None:
        self.__peerInfo = peerInfo
        self.__address = Address("localhost", 
            int(input("Enter UDP Server Port Address: ")))

    def startServer(self) -> None:
        server = socketserver.ThreadingUDPServer((self.__address.ip, self.__address.port), UDPRequestHandler)
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Starting UDP server in thread:", server_thread.name)

    @property
    def address(self) -> Address:
        return self.__address
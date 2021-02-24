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
        data = self.request[0].strip()
        socket = self.request[1]
        message = data.decode('utf-8').split('\n')[0]
        print(f'{self.client_address[0]} wrote: ' + message)
        messagetype = message[:4]
        message = message[4:]
        sourceAddress = Address(self.client_address[0], self.client_address[1])
        self.executeMessageRead(messagetype, message, sourceAddress)
        #this is where we should process what type of request: peer, snip, or stop message
        #socket.sendto(data.upper(), self.client_address)

    def getPeerInfo(self, peerInfo: PeerInfo) -> None:
        self.__peerInfo = peerInfo
        return

    def executeMessageRead(self, messageType: str, messageBody: str, sourceAddress: Address):
        dateReceived = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if messageType == "snip":
            pass
            #TODO: add the tweet as a snippet
        elif messageType == "peer":
            # Making sure that we arent adding the same peer or source twice
            sourceInList = False
            peerAddressInfo = messageBody.split(":")
            peerAddress = Address(peerAddressInfo[0], peerAddressInfo[1])
            if(peerAddress not in self.__peerInfo.totalPeerList()):
                for source in self.__peerInfo.sourceList():
                    if source.address() == sourceAddress:
                        sourceInList = True
                        break
            self.__peerInfo.addSource(Source(sourceAddress, dateReceived, set([peerAddress])))
            #TODO: add the new peers and the source
        elif messageType == "stop":
            pass
            #TODO: close the connection with this peer

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

class UDPServer:
    def __init__(self, peerInfo: PeerInfo) -> None:
        self.__peerInfo = peerInfo
        self.__timestamp = 0
        self.__address = Address("localhost", 
            int(input("Enter UDP Server Port Address: ")))
        self.__requestHandler = UDPRequestHandler()

    def startServer(self) -> None:
        server = socketserver.ThreadingUDPServer((self.__address.ip, self.__address.port), UDPReqeustHandler)
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
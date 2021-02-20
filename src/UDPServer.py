from address import Address
import socket
import threading
import socketserver

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print(f'{self.client_address[0]} wrote: {data}')
        #this is where we should process what type of request: peer, snip, or stop message
        #socket.sendto(data.upper(), self.client_address)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

class UDPServer:
    def __init__(self, UDPAddress: Address) -> None:
        self.__address = UDPAddress

    def startServer(self) -> None:
        server = ThreadedUDPServer((self.__address.ip, self.__address.port), ThreadedUDPRequestHandler)
        with server:
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

if __name__ == '__main__':
    udpServer = UDPServer(Address("localhost", 0))
    udpServer.startServer()


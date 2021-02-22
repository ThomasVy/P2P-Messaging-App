from address import Address
import threading
import socketserver

class UDPRequestHandler(socketserver.DatagramRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def handle(self):
        # data = self.request[0].strip()
        data = datagram = self.rfile.readline().strip()
        print(f'{self.client_address} wrote: {data}')
        #this is where we should process what type of request: peer, snip, or stop message

class UDPServer:
    def __init__(self) -> None:
        self.__address = Address(input("Enter UDP Server Address: "), 
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
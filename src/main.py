import socket
from typing import no_type_check
HOST = '192.168.56.1'  # Standard loopback interface address (localhost)
PORT = 55921        # Port to listen on (non-privileged ports are > 1023)

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        keepListening = True
        while keepListening:
            data = s.recv(1024)
            data = data.decode('utf-8')
            keepListening = processRequest(data)
        


def processRequest(data: str) -> bool:
    print("Received", data)
    request = data.split('\n')
    requestType = request[0]
    if (requestType == "get team name"):
        pass #TODO
    elif (requestType == "get code"):
        pass #TODO
    elif (requestType == "receive peers"):
        pass #TODO
    elif (requestType == "get report"):
        pass #TODO
    elif (requestType == "close"):
        return False
    return True



if __name__ == '__main__':
    main()
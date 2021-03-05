# peer.py file 
# Class for a single peer
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from address import Address
from datetime import datetime
class Peer:
    def __init__(self, address: Address) -> None:
        self.__address = address #address of the peer
        #last time we heard from this peer.
        self.__timestamp = datetime.now().timestamp()

    def __hash__(self) -> int:
        return hash((self.__address))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Peer):
            return ((self.__address == other.__address))
        else:
            return False
    
    @property
    def address(self) -> Address:
        return self.__address
    
    @property
    def timestamp(self) -> int:
        return self.__timestamp
    
    @property
    def ip(self) -> str:
        return self.__address.ip

    @property
    def port(self) -> int:
        return self.__address.port
    
    def updateTimestamp(self) -> None:
        self.__timestamp = datetime.now().timestamp()

    def __str__(self) -> str:
        return str(self.__address)


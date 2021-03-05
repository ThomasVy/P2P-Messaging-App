# address.py file 
# Address class for holding the ip address and the port number
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
class Address:
    def __init__(self, address: str) -> None:
        splitAddress = address.split(":")
        self.__ip = splitAddress[0]
        self.__port = int(splitAddress[1])

    def __hash__(self) -> int:
        return hash((self.ip, self.port))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Address):
            return ((self.__ip == other.__ip) and (self.__port == other.__port))
        else:
            return False

    @property
    def ip(self) -> str:
        return self.__ip
    
    @property
    def port(self) -> int:
        return self.__port

    def __str__(self) -> str:
        return f'{self.__ip}:{self.__port}'


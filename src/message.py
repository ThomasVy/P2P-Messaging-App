# message.py file 
# this class will hold the information that is used in UDP Server
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from address import Address

class Message:
    def __init__(self, message: str, source: Address, timestamp: str) -> None:
        self.__type = message[:4] #type of message
        self.__body = message[4:] #main body of the message
        self.__source = source #Address sender/receiver 
        self.__timestamp = timestamp #When the message is sent/received

    @property
    def type(self) -> str:
        return self.__type
    
    @property 
    def source(self) -> Address:
        return self.__source
    
    @property
    def timestamp(self) -> str:
        return self.__timestamp

    @property
    def body(self) -> str:
        return self.__body

    def __str__(self) -> str:
        return f'{self.type}{self.body}'


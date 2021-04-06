# ackReceived.py file 
# This is a value type that represents our incoming acks so that we can keep track of them
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from address import Address
class AckReceived:
    def __init__(self, lamportTimestamp: int, source: Address):
        self.__lamportTimestamp = lamportTimestamp #lamport time stamp of the incoming ack
        self.__source = source #source peer

    def __hash__(self) -> int:
        return hash((self.__lamportTimestamp, self.__source))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, AckReceived):
            return ((self.__lamportTimestamp == other.__lamportTimestamp) and (self.__source == other.__source))
        else:
            return False
    @property
    def lamportTimestamp(self) -> int:
        return self.__lamportTimestamp
    
    @property
    def source(self) -> str:
        return self.__source
    
    def __str__(self) -> str:
        return f'{self.__lamportTimestamp} {self.__source}'


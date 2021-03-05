# snippet.py file 
# The snippet messages received from peers to display to the user
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from address import Address
class Snippet:
    def __init__(self, lamportTimestamp: int, messageBody: str, senderAddress: Address):
        self.__lamportTimestamp = lamportTimestamp #lamport time stamp of the snippet
        self.__messageBody = messageBody #actual text of the snippet
        self.__senderAddress = senderAddress #the sender who sent the snippet

    @property
    def lamportTimestamp(self) -> int:
        return self.__lamportTimestamp
    
    @property
    def messageBody(self) -> str:
        return self.__messageBody
    
    @property
    def senderAddress(self) -> Address:
        return self.__senderAddress
    
    def __str__(self) -> str:
        return f'{self.__lamportTimestamp} {self.__messageBody} {self.__senderAddress}'


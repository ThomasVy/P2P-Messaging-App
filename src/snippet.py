# snippet.py file 
# The snippet messages received from peers to display to the user
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from address import Address
class Snippet:
    def __init__(self, lamportTimestamp: int, originalLamportTimestamp: int,
     messageBody: str, senderAddress: Address):
        #The timestamp that sender originally had for this snippet.
        self.__originalLamportTimestamp = originalLamportTimestamp  
        self.__lamportTimestamp = lamportTimestamp #lamport time stamp of the snippet
        self.__messageBody = messageBody #actual text of the snippet
        self.__senderAddress = senderAddress #the sender who sent the snippet

    def __eq__(self, other: object):
        return self.__originalLamportTimestamp == other.__originalLamportTimestamp and \
            self.__senderAddress == other.__senderAddress and \
            self.__messageBody == other.__messageBody

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


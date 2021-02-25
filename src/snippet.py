from address import Address
class Snippet:
    def __init__(self, lamportTimestamp: int, messageBody: str, senderAddress: Address):
        self.__lamportTimestamp = lamportTimestamp
        self.__messageBody = messageBody
        self.__senderAddress = senderAddress

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
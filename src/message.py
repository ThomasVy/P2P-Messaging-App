from address import Address

class Message:
    def __init__(self, message: str, source: Address, timestamp: str) -> None:
        self.__type = message[:4]
        self.__body = message[4:]
        self.__source = source
        self.__timestamp = timestamp

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
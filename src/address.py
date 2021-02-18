class Address:
    def __init__(self, ip: str, port: int) -> None:
        self.__ip = ip
        self.__port = port

    @property
    def ip(self) -> str:
        return self.__ip
    
    @property
    def port(self) -> int:
        return self.__port

    def __str__(self) -> str:
        return f'{self.__ip}:{self.__port}'

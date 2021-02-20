from address import Address

class Source:
    def __init__(self, address: Address, date: str, peerList: set([Address])) -> None:
        self.__address = address
        self.__date = date
        self.__peerList = peerList

    @property
    def address(self) -> Address:
        return self.__address

    @property
    def date(self) -> str:
        return self.__date

    @property
    def peerList(self) -> set([Address]):
        return self.__peerList
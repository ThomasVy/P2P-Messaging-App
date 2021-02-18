from address import Address

class Source:
    def __init__(self, address: Address, date: str, peerList: set[str]) -> None:
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
    def peerList(self) -> set[str]:
        return self.__peerList
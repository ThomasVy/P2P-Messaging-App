from address import Address
from source import Source

class PeerInfo:
    def __init__(self) -> None:
        self.__sourceList = {}
        self.__totalPeerList= set([])

    def addSource(self, address: Address, date: str, peerList: list[str]) -> None:
        self.__sourceList[str(address)] = Source(address, date, peerList)
        self.__totalPeerList.update(peerList)

    @property
    def totalPeerList(self) -> set[str]:
        return self.__totalPeerList

    @property
    def sourceList(self) -> list[Source]:
        return self.__sourceList.values()
from address import Address
from source import Source
from address import Address

class PeerInfo:
    def __init__(self) -> None:
        self.__sourceList = {}
        self.__totalPeerList= set([])

    def addSource(self, source: Source) -> None:
        self.__sourceList[str(source.address)] = source
        self.__totalPeerList.update(source.peerList)

    @property
    def totalPeerList(self) -> set([Address]):
        return self.__totalPeerList

    @property
    def sourceList(self) -> list([Source]):
        return self.__sourceList.values()
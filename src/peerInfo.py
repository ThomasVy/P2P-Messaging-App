from address import Address
from source import Source

class PeerInfo:
    def __init__(self) -> None:
        self.__sourceList = {}
        self.__activePeerList= set([])

    def addSource(self, source: Source) -> None:
        self.__sourceList[str(source.address)] = source
        self.__activePeerList.update(source.peerList)

    @property
    def activePeerList(self) -> set([Address]):
        return self.__activePeerList

    @property
    def sourceList(self) -> list([Source]):
        return self.__sourceList.values()

    #returns list of all peers that were in the system, even peers that are inactive.
    @property
    def totalPeerList(self) -> set([Address]):
        list = set([])
        for source in self.__sourceList.values():
            list.update(source.peerList)
        return list
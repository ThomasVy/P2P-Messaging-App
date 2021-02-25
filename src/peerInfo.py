from address import Address
from source import Source
from snippet import Snippet

class PeerInfo:
    def __init__(self) -> None:
        self.__tcpSourceList = []
        self.__udpSourceList = []
        self.__udpSentPeerLog = []
        self.__snippets = []
        self.__peerList = set([])

    def addSourceFromUDP(self, source: Source) -> None:
        self.__udpSourceList.append(source)
        self.__peerList.update(source.peerList )

    def addSourceFromTCP(self, source: Source) -> None:
        self.__tcpSourceList.append(source)
        self.__peerList.update(source.peerList)

    def logPeerMessage(self, peerMessage: Source) -> None:
        self.__udpSentPeerLog.append(peerMessage)

    def addSnippet(self, snippet: Snippet) -> None:
        self.__snippets.append(snippet)

    @property
    def snippets(self) -> list([Snippet]):
        return self.__snippets

    @property
    def udpSentPeerList(self) -> list([Source]):
        return self.__udpSentPeerLog

    @property
    def tcpSourceList(self) -> list([Source]):
        return self.__tcpSourceList
    
    @property
    def udpSourceList(self) -> list([Source]):
        return self.__udpSourceList

    @property
    def peerList(self) -> set([Address]):
        return self.__peerList
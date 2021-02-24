from address import Address
from source import Source
from enum import Enum

class PeerInfo:
    def __init__(self) -> None:
        self.__tcpSourceList = []
        self.__udpSourceList = []
        self.__udpSentPeerLog = []
        self.__udpSentMessageLog = []
        self.__peerList = set([])

    def addSourceFromUDP(self, source: Source) -> None:
        self.__udpSourceList.append(source)
        self.__peerList.update(source.peerList )

    def addSourceFromTCP(self, source: Source) -> None:
        self.__tcpSourceList.append(source)
        self.__peerList.update(source.peerList)

    def logPeerSentUDP(self, peerSent: Source) -> None:
        self.__udpSentPeerLog.append(peerSent)

    # def logMessageSentUDP(self, messageSent: Message) -> None:
    #     self.__udpSentMessageLog.append(messageSent)

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
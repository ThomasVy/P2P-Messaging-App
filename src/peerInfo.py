# peerInfo.py file 
# Holds all the information from peers. Eg. Snippets, 
# peer messages sent, peer messages received
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from source import Source
from snippet import Snippet
from peer import Peer
from ackReceived import AckReceived

class PeerInfo:
    def __init__(self) -> None:
        self.__tcpSourceList = [] #List of TCP sources 
        self.__udpSourceList = [] #List of UDP sources 
        self.__udpSentPeerLog = [] #List of UDP peer messages sent
        self.__snippets = [] #snippets received
        self.__peerList = set([]) #active peer lists
        self.__totalPeerList = set([]) #all the known peers since the beginning
        self.__acksReceived = set([])
        self.__ackCount = 0

    def addSourceFromUDP(self, source: Source) -> None:
        self.__udpSourceList.append(source)
        self.__peerList.update(source.peerList)
        self.__totalPeerList.update(source.peerList)

        ## also update the timestamp of the source since we have now heard from it
        for sourcePeer in self.__peerList:
            if sourcePeer.address == source.address:
                sourcePeer.updateTimestamp()

    def addSourceFromTCP(self, source: Source) -> None:
        self.__tcpSourceList.append(source)
        self.__peerList.update(source.peerList)
        self.__totalPeerList.update(source.peerList)

    def logPeerMessage(self, peerMessage: Source) -> None:
        self.__udpSentPeerLog.append(peerMessage)

    def addSnippet(self, snippet: Snippet) -> None:
        self.__snippets.append(snippet)
    
    def addAck(self, ackReceived: AckReceived) -> None:
        self.__acksReceived.update(ackReceived)
        self.__ackCount += 1

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
    def peerList(self) -> set([Peer]):
        return self.__peerList

    @property
    def totalPeerList(self) -> set([Peer]):
        return self.__totalPeerList

    @property
    def acksReceived(self) -> set([AckReceived]):
        return self.__acksReceived

    @property
    def ackCount(self) -> int:
        return self.__ackCount

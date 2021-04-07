# peerInfo.py file 
# Holds all the information from peers. Eg. Snippets, 
# peer messages sent, peer messages received
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from source import Source
from snippet import Snippet
from peer import Peer
from ackReceived import AckReceived
from datetime import datetime
import threading

class PeerInfo:
    def __init__(self) -> None:
        self.__tcpSourceList = [] #List of TCP sources 
        self.__udpSourceList = [] #List of UDP sources 
        self.__udpSentPeerLog = [] #List of UDP peer messages sent
        self.__snippets = [] #snippets received
        self.__peerList = set([])  #all the known peers since the beginning
        self.__acksReceived = set([])
        #Prevents the peerlist from expanding while iterating over it
        self.__peerListLock = threading.Lock()

    def addSourceFromUDP(self, source: Source) -> set([Peer]):
        with self.__peerListLock:
            catchUpList = {peer for peer in source.peerList if peer not in self.__peerList}
            ## also update the timestamp of the source since we have now heard from it
            for sourcePeer in self.__peerList:
                if sourcePeer.address == source.address:
                    sourcePeer.updateTimestamp()
                    if(sourcePeer.status != "alive"):
                        sourcePeer.status = "alive"
                        #reactivated peer so we need to send catch up messages
                        catchUpList.add(sourcePeer)
                    break
            self.__udpSourceList.append(source)
            self.__peerList.update(source.peerList)
        return catchUpList

    def addSourceFromTCP(self, source: Source) -> None:
        with self.__peerListLock:
            self.__tcpSourceList.append(source)
            self.__peerList.update(source.peerList)

    def logPeerMessage(self, peerMessage: Source) -> None:
        self.__udpSentPeerLog.append(peerMessage)

    def addSnippet(self, snippet: Snippet) -> None:
        self.__snippets.append(snippet)
    
    def addAck(self, ackReceived: AckReceived) -> None:
        self.__acksReceived.add(ackReceived)

    def checkForInactivePeers(self) -> None:
        with self.__peerListLock:
            currentTime = datetime.now().timestamp()
            for peer in self.__peerList:
                if(peer.status != "silent"):
                    #If the peer hasn't sent a peer message within 3 minutes, remove them
                    if (peer.timestamp + 60) < currentTime:
                        print(f'Have not heard from {peer} in a while, setting them silent...')
                        peer.status = "silent"
                
    @property
    def snippets(self) -> list([Snippet]):
        return self.__snippets.copy()

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
    def activePeerList(self) -> set([Peer]):
        activePeers = {peer for peer in self.__peerList if peer.status == "alive"}
        return activePeers

    @property
    def totalPeerList(self) -> set([Peer]):
        return self.__peerList

    @property
    def acksReceived(self) -> set([AckReceived]):
        return self.__acksReceived

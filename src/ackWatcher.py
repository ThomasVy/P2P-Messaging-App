# ackWatcher.py file 
# this class is responsible for monitoring acks for a specific message and for purging peers who have not acked
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from address import Address
import time
from ackReceived import AckReceived
from snippet import Snippet
from message import Message
from UDPServer import UDPServer
from datetime import datetime
from peerInfo import PeerInfo
from peer import Peer
class AckWatcher:
    def __init__(self, snippet: Snippet, peerInfo: PeerInfo, UDPServer: UDPServer) -> None:
        self.__peerInfo = peerInfo
        self.__udpServer = UDPServer
        self.__sentList = peerInfo.activePeerList.copy()
        self.__tempSentList = set([Peer])
        self.__snippetTimestamp = snippet.lamportTimestamp
        self.__snippet = snippet
    
    def start(self) -> None:
        for i in range(3):
            time.sleep(10)
            for ack in self.__peerInfo.acksReceived:
                if ack.lamportTimestamp == self.__snippetTimestamp:
                    self.__tempSentList = [peer for peer in self.__sentList if str(ack.source) != str(peer.address)]
                    self.__sentList = self.__tempSentList
            for peer in self.__sentList:
                print("Re-Sending snippet message to " + str(peer.address))
                date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                messagetext = f'snip{self.__snippetTimestamp} {self.__snippet.messageBody}'
                self.__udpServer.sendMessage(Message(message=messagetext,
                                                     source=peer.address,
                                                     timestamp=date))

        newInactiveList = [peer for peer in self.__peerInfo.activePeerList if peer in self.__sentList]
        for peer in newInactiveList:
            print("looks like " + str(peer.address) + " didnt wanna ack our snip. They are now banned from my minecraft server")
            peer.status = "missing_ack"
    ## self destruct or something
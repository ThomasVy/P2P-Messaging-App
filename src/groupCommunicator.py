from peerInfo import PeerInfo
from UDPServer import UDPServer
from registryCommunicator import RegistryCommunicator
import threading
import time
from source import Source
from address import Address
from peer import Peer
from snippet import Snippet
import asyncio
from datetime import datetime

class GroupCommunicator:
    def __init__(self) -> None:
        self.__shutdown = False
        self.__peerInfo = PeerInfo()
        self.__UDPServer = UDPServer(self.__peerInfo)
        self.__lamportMutex = threading.Lock()
        self.__lamportTimestamp = 0
        self.__registryCommunicator = RegistryCommunicator(self.__peerInfo,
            self.__UDPServer)
                
    async def start(self) -> None:
        self.__UDPServer.startServer()
        await self.__registryCommunicator.start()
        periodicSendPeerMessageThread = threading.Thread(target=self.periodicallySendPeerMessage)
        periodicSendPeerMessageThread.start()

        periodicReadMessageQueueThread = threading.Thread(target=self.processMessageQueue)
        periodicReadMessageQueueThread.start()

        periodicallyPurgeInactivePeersThread = threading.Thread(target=self.periodicallyPurgeInactivePeers)
        periodicallyPurgeInactivePeersThread.start()

    def processMessageQueue(self) -> None:
        while not self.__shutdown:
            while len(self.__UDPServer.messageQueue): #process all messages in the queue
                message = self.__UDPServer.messageQueue.pop()
                if message.type == "snip":
                    #splitting out the lamport timestamp from the rest of the snippet
                    lamportTimestamp = int(message.body.split(" ")[0])
                    body = message.body[message.body.index(" "):]
                    #update our own lamport timestamp so that we are in step with everyone else
                    self.__lamportMutex.acquire()
                    self.__lamportTimestamp = max(lamportTimestamp + 1, self.__lamportTimestamp)
                    snippet = Snippet(self.__lamportTimestamp, body, message.source)
                    self.__lamportTimestamp += 1
                    self.__lamportMutex.release()
                    self.__peerInfo.addSnippet(snippet)
                
                elif message.type == "peer":
                    self.__peerInfo.addSourceFromUDP(
                        Source(message.source, message.timestamp, set([Peer(Address(message.body))])))
                    #TODO: add the new peers and the source
                elif message.type == "stop":
                    print("Shutting Down...")
                    self.__shutdown = True
                    self.__UDPServer.shutdownServer()
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.__registryCommunicator.start()) #do the final registry communication
                    
            time.sleep(1)

    def sendSnippet(self, tweet) -> None:
        self.__lamportMutex.acquire()
        message = f'snip{self.__lamportTimestamp} {tweet}'
        self.__lamportTimestamp += 1
        self.__lamportMutex.release()
        self.__UDPServer.bMulticast(message, self.__peerInfo)

    def periodicallySendPeerMessage(self) -> None:
        while not self.__shutdown:
            peerList = self.__peerInfo.peerList.copy()
            for peer in peerList:
                peerMessage = f'peer{peer}'
                self.__UDPServer.bMulticast(peerMessage, self.__peerInfo)
                time.sleep(1)
            time.sleep(30)# sleep for 60 seconds
    
    def periodicallyPurgeInactivePeers(self) -> None:
        while not self.__shutdown:
            peers = self.__peerInfo.peerList
            currentTime = datetime.now().timestamp()
            for peer in peers:
                if (peer.timestamp + 180) < currentTime:
                    print("Have not heard from " + str(peer) + " in a while, disconnecting from them...")
                    self.__peerInfo.peerList.remove(peer)
                time.sleep(1)
            time.sleep(180)


    @property
    def shutdown(self) -> bool:
        return self.__shutdown

    @property
    def snippets(self) -> list([Snippet]):
        return self.__peerInfo.snippets
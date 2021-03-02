from peerInfo import PeerInfo
from UDPServer import UDPServer
from registryCommunicator import RegistryCommunicator
import threading
from source import Source
from address import Address
from peer import Peer
from snippet import Snippet
import asyncio
from datetime import datetime

class GroupCommunicator:
    def __init__(self, conditional: threading.Condition) -> None:
        self.__shutdown = False
        self.__peerInfo = PeerInfo()
        self.__UDPServer = UDPServer(self.__peerInfo)
        self.__lamportMutex = threading.Lock()
        self.__lamportTimestamp = 0
        self.__registryCommunicator = RegistryCommunicator(self.__peerInfo,
            self.__UDPServer)
        self.__periodicSendPeerMessageThread = threading.Thread(target=self.periodicallySendPeerMessage, args=(conditional,))
        self.__periodicReadMessageQueueThread = threading.Thread(target=self.processMessageQueue, args=(conditional,))
        self.__periodicallyPurgeInactivePeersThread = threading.Thread(target=self.periodicallyPurgeInactivePeers, args=(conditional,))
                
    async def start(self) -> None:
        self.__UDPServer.startServer()
        await self.__registryCommunicator.start()
        self.__periodicSendPeerMessageThread.start()
        self.__periodicReadMessageQueueThread.start()
        self.__periodicallyPurgeInactivePeersThread.start()

    def processMessageQueue(self, conditional: threading.Condition) -> None:
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

                elif message.type == "stop":
                    self.__shutdown = True
                    conditional.acquire()
                    conditional.notifyAll()
                    conditional.release()
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.__registryCommunicator.start()) #do the final registry communication
            conditional.acquire()
            conditional.wait(timeout=1.0)
            conditional.release()
        print("processMessageQueue Thread Ending")

    def sendSnippet(self, tweet) -> None:
        self.__lamportMutex.acquire()
        message = f'snip{self.__lamportTimestamp} {tweet}'
        self.__lamportTimestamp += 1
        self.__lamportMutex.release()
        self.__UDPServer.bMulticast(message, self.__peerInfo)

    def periodicallySendPeerMessage(self, conditional: threading.Condition) -> None:
        while not self.__shutdown:
            peerList = self.__peerInfo.peerList.copy()
            for peer in peerList:
                peerMessage = f'peer{peer}'
                self.__UDPServer.bMulticast(peerMessage, self.__peerInfo)
            conditional.acquire()
            conditional.wait(timeout=30.0)
            conditional.release()
        print("Sending Peer Message Thread Ending")
    
    def periodicallyPurgeInactivePeers(self, conditional: threading.Condition) -> None:
        while not self.__shutdown:
            peers = self.__peerInfo.peerList.copy()
            currentTime = datetime.now().timestamp()
            for peer in peers:
                if (peer.timestamp + 180) < currentTime:
                    print("Have not heard from " + str(peer) + " in a while, disconnecting from them...")
                    self.__peerInfo.peerList.remove(peer)
            conditional.acquire()
            conditional.wait(timeout=180.0)
            conditional.release()
        print("Purge Thread Ending")

    @property
    def shutdown(self) -> bool:
        return self.__shutdown

    @property
    def snippets(self) -> list([Snippet]):
        return self.__peerInfo.snippets
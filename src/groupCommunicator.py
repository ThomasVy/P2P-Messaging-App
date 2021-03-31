# groupCommunicator.py file 
# this class will handle most of the communication behind the scenes to
# send snippets to peers, peer messages, filtering messages, etc. 
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
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
from message import Message

class GroupCommunicator:
    def __init__(self, timerLock: threading.Condition) -> None:
        self.__shutdown = False #This will be the variable that signals the system to shutdown
        self.__peerInfo = PeerInfo() #this will hold all the peer list, peer snippets, and peer messages
        self.__UDPServer = UDPServer(self.__peerInfo) #The UDP server for UDP communication
        self.__lamportMutex = threading.Lock()
        self.__lamportTimestamp = 0 #For keeping lamport timestep in check
        self.__registryCommunicator = RegistryCommunicator(self.__peerInfo,
            self.__UDPServer) #for communicating between the registry
        #prepping the threads that are needed for communication
        self.__periodicSendPeerMessageThread = threading.Thread(
            target=self.periodicallySendPeerMessage)
        self.__periodicReadMessageQueueThread = threading.Thread(
            target=self.processMessageQueue)
        self.__periodicallyPurgeInactivePeersThread = threading.Thread(
            target=self.periodicallyPurgeInactivePeers)
        self.__timerLock = timerLock
        
                
    async def start(self) -> None:
        self.__UDPServer.startServer()
        await self.__registryCommunicator.start()
        self.__periodicSendPeerMessageThread.start()
        self.__periodicReadMessageQueueThread.start()
        self.__periodicallyPurgeInactivePeersThread.start()

    #starts the process for shutting down the application (threads and server)
    def __initiateShutdownSequence(self, stopSenderAddress: Address) -> None:
        self.__shutdown = True #signal to stop looping all threads
        timeNow = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ackMessage = Message(message=f'ack{self.__registryCommunicator.teamName}', 
                     source=stopSenderAddress,
                     timestamp=timeNow)
        self.__UDPServer.shutdownServer()
        self.__UDPServer.sendMessage(ackMessage) #Send the ack shutdown message
        shutdownMessage = Message(message="shutdown",
                            source=self.__UDPServer.address,
                            timestamp=timeNow) #some random message to unblock our udp server
        self.__UDPServer.sendMessage(shutdownMessage)#Send UDPMessage to our server to unblock and shutdown
        self.__timerLock.acquire()
        self.__timerLock.notifyAll() #wake up all sleeping threads so they can shutdown
        self.__timerLock.release()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__registryCommunicator.start()) #do the final registry communication

    #processes a snippet from the message queue
    def __processSnippet(self, message: Message) -> None:
        #splitting out the lamport timestamp from the rest of the snippet
        lamportTimestamp = int(message.body.split(" ")[0])
        body = message.body[message.body.index(" "):]
        #update our own lamport timestamp so that we are in step with everyone else
        self.__lamportMutex.acquire()
        self.__lamportTimestamp = max(lamportTimestamp + 1, self.__lamportTimestamp)
        snippet = Snippet(self.__lamportTimestamp, body, message.source)
        self.__lamportTimestamp += 1
        self.__lamportMutex.release()
        self.__peerInfo.addSnippet(snippet) #add the snippet to the list of snippets

    #Process all the UDP messages received in the UDPServer message queue
    def processMessageQueue(self) -> None:
        while not self.__shutdown:
            while len(self.__UDPServer.messageQueue): #process all messages in the queue if there is any
                message = self.__UDPServer.messageQueue.pop() #remove the first message in the queue
                if message.type == "snip":
                   self.__processSnippet(message)
                elif message.type == "peer":
                    self.__peerInfo.addSourceFromUDP(
                        Source(message.source, message.timestamp, set([Peer(Address(message.body))])))
                elif message.type == "stop":
                    self.__initiateShutdownSequence(message.source)
                    break # Do not process any more messages once the shutdown sequence is initiated.
            self.__timerLock.acquire()
            self.__timerLock.wait(timeout=1.0) #check the message queue every 1 second
            self.__timerLock.release()
        print("processMessageQueue Thread Ending")

     #Sends snippet messages to all known peers in an interval
    def sendSnippet(self, tweet) -> None:
        self.__lamportMutex.acquire()
        message = f'snip{self.__lamportTimestamp} {tweet}'
        self.__lamportTimestamp += 1
        self.__lamportMutex.release()
        self.__UDPServer.bMulticast(message)

    #Sends peer messages to all known peers in an interval
    def periodicallySendPeerMessage(self) -> None:
        while not self.__shutdown:
            peerList = self.__peerInfo.peerList.copy()
            for peer in peerList:
                peerMessage = f'peer{peer}'
                self.__UDPServer.bMulticast(peerMessage)
            self.__timerLock.acquire()
            self.__timerLock.wait(timeout=30.0) #send peer messages every 30 seconds
            self.__timerLock.release()
        print("Sending Peer Message Thread Ending")
    
    #delete peers if they haven't sent a peer message in a while (3 minutes)
    def periodicallyPurgeInactivePeers(self) -> None:
        while not self.__shutdown:
            peers = self.__peerInfo.peerList.copy() #make a copy of the list because it might change
            currentTime = datetime.now().timestamp()
            for peer in peers:
                #If the peer hasn't sent a peer message within 3 minutes, remove them
                if (peer.timestamp + 180) < currentTime:
                    print("Have not heard from " + str(peer) + " in a while, disconnecting from them...")
                    self.__peerInfo.peerList.remove(peer)
            self.__timerLock.acquire()
            self.__timerLock.wait(timeout=180.0) #check again in 3 minutes
            self.__timerLock.release()
        print("Purge Thread Ending")

    @property
    def shutdown(self) -> bool:
        return self.__shutdown

    @property
    def snippets(self) -> list([Snippet]):
        return self.__peerInfo.snippets


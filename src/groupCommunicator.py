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
from ackReceived import AckReceived

class GroupCommunicator:
    def __init__(self, timerCondition: threading.Condition) -> None:
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
        self.__timerCondition = timerCondition
                
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
        self.__UDPServer.sendMessage(ackMessage) #Send the ack shutdown message
        self.__UDPServer.shutdownServer()
        with self.__timerCondition:
            self.__timerCondition.notifyAll() #wake up all sleeping threads so they can shutdown
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__registryCommunicator.start()) #do the final registry communication

    #processes a snippet from the message queue
    def __processSnippet(self, message: Message) -> None:
        #splitting out the lamport timestamp from the rest of the snippet
        messageBodyList = message.body.split(" ")
        messageLamportTimestamp = int(messageBodyList[0])
        body = ' '.join(messageBodyList[1:])
        with self.__lamportMutex:
            correctedTimestamp = max(messageLamportTimestamp + 1, self.__lamportTimestamp)
            snippet = Snippet(correctedTimestamp, messageLamportTimestamp, body, message.source)
            if(snippet not in self.__peerInfo.snippets): #only add the snippet if it hasn't been added before.
                #update our own lamport timestamp so that we are in step with everyone else
                self.__lamportTimestamp = correctedTimestamp + 1
                self.__peerInfo.addSnippet(snippet) #add the snippet to the list of snippets
        # Craft and send ack message for snippet
        ackMessage = Message(message=f'ack {messageLamportTimestamp}',
                     source=message.source,
                     timestamp=message.timestamp)
        self.__UDPServer.sendMessage(ackMessage)
    
    def __processCatchUpSnip(self, messageBody: str) -> None:
        messageBodyList = messageBody.split(" ")
        originalSender = Address(messageBodyList[0])
        messageLamportTimestamp = int(messageBodyList[1])
        content = ' '.join(messageBodyList[2:])
        with self.__lamportMutex:
            correctedTimestamp = max(messageLamportTimestamp + 1, self.__lamportTimestamp)
            snippet = Snippet(correctedTimestamp, messageLamportTimestamp, content, originalSender)
            if(snippet not in self.__peerInfo.snippets): #only add the snippet if it hasn't been added before.
                #update our own lamport timestamp so that we are in step with everyone else
                self.__lamportTimestamp = correctedTimestamp + 1
                self.__peerInfo.addSnippet(snippet) #add the snippet to the list of snippets

    #Process all the UDP messages received in the UDPServer message queue
    def processMessageQueue(self) -> None:
        while not self.__shutdown:
            while len(self.__UDPServer.messageQueue): #process all messages in the queue if there is any
                message = self.__UDPServer.messageQueue.pop() #remove the first message in the queue
                if message.type == "snip":
                   self.__processSnippet(message)
                elif message.type == "peer":
                    self.__processPeer(message)
                elif message.type == "ack ":
                    self.__processAck(message)
                elif message.type == "ctch":
                    self.__processCatchUpSnip(message.body)
                elif message.type == "stop":
                    self.__initiateShutdownSequence(message.source)
                    break # Do not process any more messages once the shutdown sequence is initiated.
            with self.__timerCondition:
                self.__timerCondition.wait(timeout=1.0) #check the message queue every 1 second
        print("processMessageQueue Thread Ending")
    
    def __processPeer(self, message: Message) -> None:
        source = Source(message.source, message.timestamp, set([Peer(Address(message.body))]))
        catchUpList = self.__peerInfo.addSourceFromUDP(source)
        for catchUpPeer in catchUpList:
            for snippet in self.__peerInfo.snippets:
                catchUpTxt = f'ctch{snippet.senderAddress} {snippet.originalLamportTimestamp} {snippet.messageBody}'
                catchUpMsg = Message(message=catchUpTxt,
                                     source=catchUpPeer.address,
                                     timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                self.__UDPServer.sendMessage(catchUpMsg)
                with self.__timerCondition:
                    self.__timerCondition.wait(timeout=1.0) #wait a little bit or else the messages could be out of order

    #Craft the ack object and add it to our internal list of received acks
    def __processAck(self, message: Message) -> None:
        lamportTimestamp = int(message.body)
        ack = AckReceived(lamportTimestamp, message.source)
        self.__peerInfo.addAck(ack)

     #Sends snippet messages to all known peers in an interval
    def sendSnippet(self, tweet) -> None:
        with self.__lamportMutex:
            message = f'snip{self.__lamportTimestamp} {tweet}'
            self.__lamportTimestamp += 1
        self.__UDPServer.bMulticast(message)

    #Sends peer messages to all known peers in an interval
    def periodicallySendPeerMessage(self) -> None:
        while not self.__shutdown:
            for peer in self.__peerInfo.activePeerList:
                peerMessage = f'peer{peer}'
                self.__UDPServer.bMulticast(peerMessage)
            with self.__timerCondition:
                self.__timerCondition.wait(timeout=30.0) #send peer messages every 30 seconds
        print("Sending Peer Message Thread Ending")
    
    #delete peers if they haven't sent a peer message in a while (3 minutes)
    def periodicallyPurgeInactivePeers(self) -> None:
        while not self.__shutdown:
            self.__peerInfo.checkForInactivePeers()
            with self.__timerCondition:
                self.__timerCondition.wait(timeout=60.0) #check again in 3 minutes
        print("Purge Thread Ending")

    @property
    def shutdown(self) -> bool:
        return self.__shutdown

    @property
    def snippets(self) -> list([Snippet]):
        return self.__peerInfo.snippets


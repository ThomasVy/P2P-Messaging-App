# craftResponseUtils.py file 
# Formats response strings to send to through the socket
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from collections import namedtuple
from peerInfo import PeerInfo
from address import Address
from snippet import Snippet
import os

Source = namedtuple('Source', 'address dateReceived numPeers peers')

# goes through all files in src folder and crafts response string with all the code
def getCode() -> str:
    currentLocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    files = [f for f in os.listdir(currentLocation) if os.path.isfile(os.path.join(currentLocation, f))]
    response = "Python\n"
    for file in files:
        with open(os.path.join(currentLocation, file), 'r') as f:
            response += f.read()
    response += "\n...\n"
    return response

# crafts response string with team name
def getTeamName(teamName: str) -> str:
    response = f'{teamName}\n'
    return response

# crafts response string with appropriate report information
def getReport(peerInfo: PeerInfo, snippetList: set([Snippet])) -> str:
    response = ''
    totalPeerList = peerInfo.peerList
    udpSourceList = peerInfo.udpSourceList
    tcpSourceList = peerInfo.tcpSourceList
    udpSentPeerList = peerInfo.udpSentPeerList

    response += f'{len(totalPeerList)}\n'
    for peer in totalPeerList:
        response += f'{peer}\n'
    response += f'{len(tcpSourceList)}\n'

    #tcp source list
    for source in tcpSourceList:
        response += f'{source.address}\n'
        response += f'{source.date}\n'
        response += f'{len(source.peerList)}\n'
        for peer in source.peerList:
            response += f'{peer}\n'

    #udp source list (peers received via udp)
    response += f'{len(udpSourceList)}\n'
    for source in udpSourceList:
        response += f'{source.address} {source.peerList[0]} {source.date}\n'

    #udp sent list
    response += f'{len(udpSentPeerList)}\n'
    for source in udpSentPeerList:
        response += f'{source.address} {source.peerList[0]} {source.date}\n'

    for snippet in snippetList:
        response += snippet

    return response

def getLocation(serverAddress: Address) -> str:
    response = f'{serverAddress}\n'
    return response

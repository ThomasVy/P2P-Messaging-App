# craftResponseUtils.py file 
# Formats response strings to send to through the socket
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from collections import namedtuple
from peerInfo import PeerInfo
from address import Address
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
def getReport(peerInfo: PeerInfo) -> str:
    response = ''
    totalPeerList = peerInfo.activePeerList
    sourceList = peerInfo.sourceList

    response += f'{len(totalPeerList)}\n'
    for peer in totalPeerList:
        response += f'{peer}\n'
    response += f'{len(sourceList)}\n'

    # Iterate a second time to list the sources
    for source in sourceList:
        response += f'{source.address}\n'
        response += f'{source.date}\n'
        response += f'{len(source.peerList)}\n'
        for peer in source.peerList:
            response += f'{peer}\n'
    return response

def getLocation(serverAddress: Address) -> str:
    response = f'{serverAddress}\n'
    return response

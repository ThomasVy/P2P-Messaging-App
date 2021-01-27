# craftResponseUtils.py file 
# Formats response strings to send to through the socket
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from collections import namedtuple
import os

TEAM_NAME = "Zhomas"
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
def getTeamName() -> str:
    response = TEAM_NAME + '\n'
    return response

# crafts response string with appropriate report information
def getReport(sources: list[Source]) -> str:
    totalPeers = 0
    peerlist = []
    response = ''
    totalSources = len(sources)

    # Iterate once so that we get the total number of peers and sources
    for source in sources:
        totalPeers += int(source.numPeers)
        for peer in source.peers:
            peerlist.append(peer)

    response += (str(totalPeers) + "\n")
    for peer in peerlist:
        response += (str(peer) + "\n")
    response += (str(totalSources) + "\n")

    # Iterate a second time to list the sources
    for source in sources:
        response += (source.address + "\n")
        response += (source.dateReceived + "\n")
        response += (source.numPeers + "\n")
        for peer in source.peers:
            response += (peer + "\n")
    return response


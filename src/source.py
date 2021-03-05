# source.py file 
# This class holds the information for which peer sent which peer 
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from address import Address
from peer import Peer

class Source:
    def __init__(self, address: Address, date: str, peerList: set([Peer])) -> None:
        self.__address = address #the ip address which the peer list came from
        self.__date = date #the date when the peer message list was sent
        self.__peerList = peerList #the list of peer that the peer sent over

    @property
    def address(self) -> Address:
        return self.__address

    @property
    def date(self) -> str:
        return self.__date

    @property
    def peerList(self) -> set([Peer]):
        return self.__peerList


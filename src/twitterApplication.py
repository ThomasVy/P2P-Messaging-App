from groupCommunicator import GroupCommunicator

class TwitterApplication:
    def __init__(self) -> None:
        self.__groupCommunicator = GroupCommunicator()
       
    def start(self) -> None: 
        self.__groupCommunicator.start()
    
    def grabUserTweet()-> None:
        pass #TODO
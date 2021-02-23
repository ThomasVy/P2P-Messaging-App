from groupCommunicator import GroupCommunicator

class TwitterApplication:
    def __init__(self) -> None:
        self.__groupCommunicator = GroupCommunicator()
       
    async def start(self) -> None: 
        await self.__groupCommunicator.start()
        while not self.__groupCommunicator.__shutdown:
            self.grabUserTweet()
    
    def grabUserTweet(self)-> None:
        tweet = input()
        self.__groupCommunicator.bMulticast(message=tweet)

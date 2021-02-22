from groupCommunicator import GroupCommunicator

class TwitterApplication:
    def __init__(self) -> None:
        self.__groupCommunicator = GroupCommunicator()
       
    async def start(self) -> None: 
        await self.__groupCommunicator.start()
    
    def grabUserTweet()-> None:
        pass #TODO
from groupCommunicator import GroupCommunicator
import threading
import time

class TwitterApplication:
    def __init__(self) -> None:
        self.__groupCommunicator = GroupCommunicator()
        self.__MAX_SNIP_LENGTH = 1000
       
    async def start(self) -> None: 
        await self.__groupCommunicator.start()
        displayTweetsThread = threading.Thread(target=self.displayTweets)
        displayTweetsThread.daemon = True
        displayTweetsThread.start()
        self.grabUserTweet()
    
    def displayTweets(self) -> None:
        oldSnippetLen = -1
        while not self.__groupCommunicator.shutdown:
            if (len(self.__groupCommunicator.snippets) > oldSnippetLen): #display only when there are new messages
                oldSnippetLen = len(self.__groupCommunicator.snippets)
                print("\n\n\n--------------------Tweets Begin--------------------")
                for snippet in self.__groupCommunicator.snippets.copy(): #display all the tweets ever since the beginning
                    print(snippet)
                print("---------------------Tweets End---------------------")
            time.sleep(2)

    def grabUserTweet(self)-> None:
        while not self.__groupCommunicator.shutdown:
            tweet = input()
            tweet = tweet[:self.__MAX_SNIP_LENGTH]
            #truncate message when it is too long.
            self.__groupCommunicator.sendSnippet(tweet)

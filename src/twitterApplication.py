from groupCommunicator import GroupCommunicator
import threading

class TwitterApplication:
    def __init__(self) -> None:
        self.__conditional = threading.Condition()
        self.__groupCommunicator = GroupCommunicator(self.__conditional)
        self.__MAX_SNIP_LENGTH = 1000
        self.__displayTweetsThread = threading.Thread(target=self.displayTweets, args=(self.__conditional,))

    async def start(self) -> None:
        await self.__groupCommunicator.start()
        self.__displayTweetsThread.start()
        self.grabUserTweet()
    
    def displayTweets(self, conditional:threading.Condition) -> None:
        oldSnippetLen = -1
        while not self.__groupCommunicator.shutdown:
            if (len(self.__groupCommunicator.snippets) > oldSnippetLen): #display only when there are new messages
                oldSnippetLen = len(self.__groupCommunicator.snippets)
                print("\n\n\n--------------------Tweets Begin--------------------")
                for snippet in self.__groupCommunicator.snippets.copy(): #display all the tweets ever since the beginning
                    print(snippet)
                print("---------------------Tweets End---------------------")
            conditional.acquire()
            conditional.wait(timeout=2.0)
            conditional.release()
        print("Displaying Tweets Thread exiting")
        print("System is shutting down. Press Enter to close the program...")

    def grabUserTweet(self)-> None:
        try:
            while not self.__groupCommunicator.shutdown:
                tweet = input()
                if self.__groupCommunicator.shutdown:
                    break
                #truncate message when it is too long.
                tweet = tweet[:self.__MAX_SNIP_LENGTH]
                self.__groupCommunicator.sendSnippet(tweet)
        finally:
            print("Grab User Tweet Thread exiting")

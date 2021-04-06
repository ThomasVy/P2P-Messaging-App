# twitterApplication.py file 
# this class is essentially the main application and the UI of the system
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from groupCommunicator import GroupCommunicator
import threading

class TwitterApplication:
    def __init__(self) -> None:
        #used to sleep threads and notify threads to wake up
        self.__conditional = threading.Condition() 
        self.__groupCommunicator = GroupCommunicator(self.__conditional)
        self.__MAX_SNIP_LENGTH = 1000 #max snippet length that can be sent
        self.__displayTweetsThread = threading.Thread(
            target=self.displayTweets, args=(self.__conditional,))

    #start the main application
    async def start(self) -> None:
        await self.__groupCommunicator.start()
        self.__displayTweetsThread.start()
        self.grabUserTweet() #The main thread will grab the user input
    
    #Displays snippets periodic if there are new snippets. 
    def displayTweets(self, conditional:threading.Condition) -> None:
        oldSnippetLen = -1 #this variable is used to check if there are new snippets
        while not self.__groupCommunicator.shutdown:
            if (len(self.__groupCommunicator.snippets) > oldSnippetLen): #display only when there are new snippets
                oldSnippetLen = len(self.__groupCommunicator.snippets)
                print("\n\n\n--------------------Tweets Begin--------------------")
                for snippet in self.__groupCommunicator.snippets.copy(): #display all the tweets ever since the beginning
                    print(snippet)
                print("---------------------Tweets End---------------------")
            with conditional:
                conditional.wait(timeout=2.0) #display snippets every 2 seconds if there are new snippets
        print("Displaying Tweets Thread exiting")
        print("System is shutting down. Press Enter to close the program...")

    #grabs user tweets that are typed
    def grabUserTweet(self)-> None:
        try:
            while not self.__groupCommunicator.shutdown:
                tweet = input()
                if self.__groupCommunicator.shutdown: #quit the thread if it's system is shutting down
                    break
                #truncate message when it is too long.
                tweet = tweet[:self.__MAX_SNIP_LENGTH]
                self.__groupCommunicator.sendSnippet(tweet)
        finally:
            print("Grab User Tweet Thread exiting")

            

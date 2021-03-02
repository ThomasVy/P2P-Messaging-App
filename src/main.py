# main.py file 
# Used to run the main application
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from twitterApplication import TwitterApplication
import asyncio

def main() -> None:
    twitterApp = TwitterApplication()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(twitterApp.start())

if __name__ == '__main__':
    main()


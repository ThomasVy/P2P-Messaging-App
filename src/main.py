# main.py file 
# Used to run the main application
# CPSC 559 Project
# By Zachery Sims & Thomas Vy

from twitterApplication import TwitterApplication
import asyncio

def main() -> None:
    twitterApp = TwitterApplication()
    asyncio.run(twitterApp.start())

if __name__ == '__main__':
    main()


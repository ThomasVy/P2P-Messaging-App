# main.py file 
# Used to run the main application
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from twitterApplication import TwitterApplication
import asyncio

def main() -> None:
    twitterApp = TwitterApplication()
    loop = asyncio.get_event_loop()
    loop.create_task(twitterApp.start())
    loop.run_forever()

if __name__ == '__main__':
    main()


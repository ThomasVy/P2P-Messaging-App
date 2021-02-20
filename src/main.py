# main.py file 
# Used to run the main application
# CPSC 559 Project
# By Zachery Sims & Thomas Vy
from twitterApplication import TwitterApplication

def main() -> None:
    twitterApp = TwitterApplication()
    twitterApp.start()

if __name__ == '__main__':
    main()


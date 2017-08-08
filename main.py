''' iRNBA's entry point '''

from pync import Notifier
from reddit import Reddit

import time

FIVE_MINUTES = 60 * 60 * 5
def main():
    ''' Instantiates reddit and notification notifier '''
    reddit = Reddit()
    while True:
        reddit.fetch_latest_posts()


        time.sleep(FIVE_MINUTES)
    Notifier.notify('You have {0} new posts!'.format(len(reddit.posts)), title='iRNBA')

main()
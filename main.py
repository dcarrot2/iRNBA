''' iRNBA's entry point '''

from pync import Notifier
from reddit import Reddit

import time

FIVE_MINUTES = 60 * 5
def main():
    ''' Instantiates reddit and notification notifier '''
    reddit = Reddit()
    while True:
        reddit.fetch_latest_posts()
        for notification in reddit.notifications:
            if notification:
                Notifier.notify(
                    '{0}'.format(
                        notification['title']
                    ),
                    open=notification['link'],
                    title='iRNBA'
                )
                time.sleep(5)
        time.sleep(FIVE_MINUTES)

main()
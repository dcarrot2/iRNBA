''' iRNBA's entry point '''
from notifier import Notifier
from reddit import Reddit

import time

FIVE_MINUTES = 60 * 5
def main():
    ''' Instantiates reddit and notification notifier '''
    reddit = Reddit()
    notifier = Notifier()
    while True:
        reddit.fetch_latest_posts()
        for notification in reddit.notifications:
            if notification:
                notifier.send_notification(
                    message=notification.get('title', ''),
                    link=notification.get('link', ''),
                    title='iRNBA'
                )
                time.sleep(5)
        time.sleep(FIVE_MINUTES)

main()
''' iRNBA's entry point '''

from reddit import Reddit

def main():
    ''' Instantiates reddit and notification notifier '''

    reddit = Reddit()
    reddit.fetch_latest_posts()
    print reddit.posts

main()
''' This module fetches latest posts periodically and tells us whether a post is getting popular '''
from logger import Logger
import requests

URL = 'https://reddit.com/r/nba.json'

class Reddit(object):
    ''' Class to define reddit instance '''
    def __init__(self):
        self.posts = []
        self.logger = Logger()

    def fetch_latest_posts(self):
        ''' Fetch /r/nba front page '''
        nba_front_page = requests.get(URL, headers = {'User-agent' : 'irnba 0.0.1'})
        posts = []
        self.logger.log.info('Loading into mem')
        try:
            posts = nba_front_page.json()['data']['children']
        except KeyError as exception:
            self.logger.log.error('Key error on {0}'.format(exception.message))
        except Exception as general_exception:
            self.logger.log.error('Exception on {0}'.format(general_exception.message))
        
        self.logger.log.info('massaging')
        self.logger.log.info(len(posts))
        for p in posts:
            self.logger.log.info('Posting')
            post = p.get('data', {})
            self.posts.append({ 'title': post.get('title', ''), 'id': post.get('id', ''), 'num_comments': post.get('num_comments', 0), 'up_votes': post.get('ups', 0)})
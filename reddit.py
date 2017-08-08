''' This module fetches latest posts periodically and tells us whether a post is getting popular '''
from logger import Logger
from ttldict import TTLOrderedDict
import json
import requests

BASE_URL = 'https://reddit.com/r/nba'
URL = BASE_URL + '.json'
UPVOTE_THRESHOLD = 1500
TTL = 60 * 60 * 24 * 3

class Reddit(object):
    ''' Class to define reddit instance '''
    def __init__(self):
        self.posts = TTLOrderedDict(default_ttl=TTL)
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
        
        for p in posts:
            post = p.get('data', {})
            id = post.get('id', None)
            if not id:
                self.logger.log.info('Post with no id found: {0}'.format(json.dumps(post)))
                continue
            self.posts[id] = {
                'title': post.get('title', ''),
                'id': post.get('id', ''),
                'num_comments': post.get('num_comments', 0),
                'up_votes': post.get('ups', 0),
                'link': post.get('permalink', '')
            }

    def flush_posts(self):
        ''' Flush posts '''
        self.posts = {}

    @staticmethod
    def is_post_getting_hot(post):
        ''' Given an old post and a new post, determine if the post is getting popular in rNBA '''
        upvotes = post.get('ups', 0)
        if upvotes > UPVOTE_THRESHOLD:
            title = post.get('title', '')
            link = post.get('link', '')
            votes = post.get('upvotes')
            return {}
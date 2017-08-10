''' This module fetches latest posts periodically and tells us whether a post is getting popular '''
from logger import Logger
from ttldict import TTLOrderedDict
import json
import requests

BASE_URL = 'https://reddit.com'
URL = BASE_URL + '/r/nba.json'
UPVOTE_THRESHOLD = 1500
TTL = 60 * 60 * 24 * 3

class Reddit(object):
    ''' Class to define reddit instance '''
    def __init__(self):
        self.posts = TTLOrderedDict(default_ttl=TTL)
        self.notifications = []
        self.logger = Logger()

    def fetch_latest_posts(self):
        ''' Fetch /r/nba front page '''
        self.notifications = []
        self.logger.log.info('Fetching nba front page')
        nba_front_page = requests.get(URL, headers = {'User-agent' : 'irnba 0.0.1'})
        posts = []
        keys = ['title', 'id', 'ups', 'permalink']
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
            if not id in self.posts:  # Create new post
                self.posts[id] = {key: post.get(key, '') for key in keys}
            self.notifications.append(
                self.is_post_getting_hot(self.posts[id], id)
            )

    def is_post_getting_hot(self, post, id):
        ''' Given an old post and a new post, determine if the post is getting popular in rNBA '''
        upvotes = post.get('ups', 0)
        if upvotes > UPVOTE_THRESHOLD and not self.posts[id].get('marked', False):
            title = post.get('title', '')
            link = post.get('permalink', '')
            self.posts[id]['marked'] = True
            return {'title': title, 'link': BASE_URL + link}
        return None
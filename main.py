import datetime
import json
import webbrowser
import requests
import pprint

REDDIT_URL = 'http://reddit.com/r/%(subreddit)s/%(ordering)s.json'

def log(message, verbosity=1):
    print message

class Story(object):
    def __init__(self, title, link, message, comments_link=None,
        num_comments=None, source=None):

        self.title = title.encode('utf-8')
        self.link = link.encode('utf-8')
        self.message = message.encode('utf-8')
        self.comments_link = comments_link.encode('utf-8')
        self.num_comments = num_comments
        self.found_time = datetime.datetime.now()
        self.source = source.encode('utf-8')

    def show_all(self):
        pprint.pprint(self.__dict__)

    def __unicode__(self):
        return '[%(source)s] %(title)s (%(found_time)s' % {
            'source': self.source, 'title': self.title, 'found_time': self.found_time}

    __repr__ = __unicode__

    def __hash__(self):
        return hash(self.source + self.title)


def get_reddit_stories(subreddit='all', ordering='hot', limit=5):
    stories = []
    params = {
        'limit': limit
    }
    headers = {
        'User-agent': 'Mozilla/5.0'
    }

    url = REDDIT_URL % {'subreddit': subreddit, 'ordering': ordering}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        msg = '[Error] Problem with %(url)s - %(reason)s' % {'url': url, 'reason': reason}
        log(msg)
        return

    else:
        data = response.json()['data']
        if not data.has_key('children'):
            msg = '[Warn] `%(subreddit)s` subreddit has no `%(ordering)s` stories' % {
                'subreddit': subreddit, 'ordering': ordering
            }
            log(msg)
            return

    for story in data['children']:
        story_data = story['data']

        story_kwargs = {
            'title': story_data.get('title', 'No Title'),
            'link': story_data.get('url', 'No Url'),
            'message': story_data.get('description', 'No Description'),
            'comments_link': story_data.get('permalink', 'No Comments Link'),
            'num_comments': story_data.get('num_comments', 'No Comments'),
            'source': 'reddit'
        }

        s = Story(**story_kwargs)
        stories.append(s)

    return stories


if __name__ == '__main__':
    stories = get_reddit_stories('python')
    for story in stories:
        story.show_all()

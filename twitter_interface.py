''' Class to handle of all of the twitter and twitter cache interfacing '''

from collections import defaultdict
import json
import os
import tweepy as tw
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

class TwitterWrapper():
    '''This is the class where all of the wrapping happens'''

    def __init__(self, name):
        self.name = name
        self.tweets = {}

    def get_cache(self):
        '''Get the list of tweets for the user that is cached in the local filesystem'''

        file_name = self.name + '.json'

        if(os.path.isfile(file_name)):
            with open(file_name, 'r') as infile:
                self.tweets = json.loads(infile.read())
        return self.tweets

    def get_current_tweets(self, since_id=1, count=100):
        ''' Download the current list of tweets from twitter'''

        auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tw.API(auth, wait_on_rate_limit=True)

        self.tweets = api.user_timeline(screen_name=self.name, count=count, since_id=since_id)

#        with open(file_name, 'w') as outfile:
            # Iterate and print tweets
#            for tweet in t:
#                print(tweet.text)
#                l2.append(tweet._json)
#            l = l2 + l
#            json.dump(l, outfile)

        return self.tweets

    def get_recent_tweet_id(self, tweets):
        ''' Given a list of tweets, return the id of the most recent tweet'''

        since_id = 1
        if(tweets is not None):
            for tweet in tweets:
                if(tweet['id'] > since_id):
                    since_id = tweet['id']
        return since_id
#        max(tweets.iteritems(), key=operator.itemgetter(1))[0]

    def join_tweets(self, tweets1, tweets2):
        ''' Given two lists of tweets, join them and make them unique'''

        ids = defaultdict(lambda: 0)
        out_tweets = {}

        if(tweets1 is not None):
            for tweet in tweets1:
                ids[tweet["id"]] += 1
            out_tweets = tweets1

        if(tweets2 is not None):
            for tweet in tweets2:
                if(tweet["id"] not in ids):
                    ids[tweet["id"]] += 1
                    out_tweets += tweet

        return out_tweets

''' Class to handle of all of the twitter and twitter cache interfacing '''

from collections import defaultdict
import json
import tweepy as tw
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

class TwitterWrapper():
    '''This is the class where all of the wrapping happens'''

    def __init__(self, name):
        self.name = name
        self.file_name = "data/" + self.name + '.json'
        self.tweets = []

    def load_tweets(self, cache_only=True):
        ''' Single funciton to be used by callers to get data '''

        old_tweets = self.load_tweets_from_file()
        if(cache_only is False):
            since = self.get_recent_tweet_id(old_tweets)
            new_tweets = self.get_current_tweets(since, 100)
            self.tweets = self.join_tweets(old_tweets, new_tweets)
            self.save_tweets(self.tweets)
        return self.tweets

    def load_tweets_from_file(self):
        '''Get the list of tweets for the user that is cached in the local filesystem'''

        self.tweets = []

        try:
            with open(self.file_name, 'r') as infile:
                self.tweets = json.loads(infile.read())
        except:
            self.tweets = []

        return self.tweets

    def get_current_tweets(self, since_id=1, count=100):
        ''' Download the current list of tweets from twitter'''

        auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tw.API(auth, wait_on_rate_limit=True)

        self.tweets = []

        # Convert the tweets to json immediatly
        for tweet in api.user_timeline(user_id=self.name, count=count, since_id=since_id):
            self.tweets.append(tweet._json)

        return self.tweets

    def get_recent_tweet_id(self, tweets):
        ''' Given a list of tweets, return the id of the most recent tweet'''

        since_id = 1
        if(tweets is not None):
            for tweet in tweets:
                if(tweet['id'] > since_id):
                    since_id = tweet['id']
        return since_id

    def join_tweets(self, tweets1, tweets2):
        ''' Given two lists of tweets, join them and make them unique'''

        ids = defaultdict(lambda: 0)
        out_tweets = []

        if(tweets1 is not None):
            for tweet in tweets1:
                ids[tweet["id"]] += 1
            out_tweets = tweets1

        if(tweets2 is not None):
            for tweet in tweets2:
                if(tweet["id"] not in ids):
                    ids[tweet["id"]] += 1
                    out_tweets.append(tweet)
        return out_tweets

    def sort_tweets(self, tweets):
        ''' Sort list of tweets by the id field, putting them in
        chronological order '''

        return sorted(tweets, key=lambda x: x["id"], reverse=True)

    def save_tweets(self, tweets):
        ''' Write all tweets to person's file '''

        with open(self.file_name, 'w') as outfile:
            json.dump(tweets, outfile)

''' Class to handle of all of the twitter and twitter cache interfacing '''

from collections import defaultdict
import json
import time
import pandas as pd
import tweepy as tw
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

class TwitterWrapper():
    '''This is the class where all of the wrapping happens'''

#In [46]: user = api.get_user(screen_name = 'saimadhup')
#In [47]: user.id
#Out[47]: 1088398616

    def __init__(self, name):
#        self.name = name
#        self.file_name = "data/" + self.name + '.json'
        self.tweets = []

    def set_user_id(self, user_id):
        self.name = ""

    def set_screen_name(self, input_screen_name):
        auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tw.API(auth, wait_on_rate_limit=True)

        user = api.get_user(screen_name = input_screen_name)
        self.name = user.id
        self.file_name = "data/" + str(input_screen_name) + '.json'
        self.tweets = []

    def load_tweets(self, cache_only=True):
        ''' Single funciton to be used by callers to get data '''

        old_tweets = self.load_tweets_from_file()

        if(cache_only is False):
            since = self.get_recent_tweet_id(old_tweets)
            new_tweets = self.load_timeline_tweets(since)
            self.tweets = self.join_tweets(old_tweets, new_tweets)
            self.save_tweets(self.tweets)
        return self.tweets

    def sanatize(self, tweets):

        ret_value = []
        for t in tweets:
            ret_value.append(t._json)
        return ret_value

    def load_timeline_tweets(self, since):
        ''' load max timeline tweets. Capped by twitter at 3200 '''
        auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tw.API(auth, wait_on_rate_limit=True)        
        alltweets = []	
        
        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(user_id=self.name,count=200)
        
        sanitized_tweets = self.sanatize(new_tweets)

        #save most recent tweets
        alltweets.extend(sanitized_tweets)
        
        #save the id of the oldest tweet less one
        oldest = alltweets[-1]["id"] - 1
        
        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print( "getting tweets before %s" % (oldest))
            
#            time.sleep(2)
            #all subsiquent requests use the max_id param to prevent duplicates
#            oldest = 1194414093781917695
            new_tweets = api.user_timeline(user_id=self.name,count=200,max_id=oldest,min_id=since)
            
            #save most recent tweets
            alltweets.extend(self.sanatize(new_tweets))
            
            #update the id of the oldest tweet less one
            oldest = alltweets[-1]["id"] - 1
            
            print( "...%s tweets downloaded so far" % (len(alltweets)))

        self.tweets = alltweets
        self.save_tweets(self.tweets)
        return self.tweets

    def get_tweet_text(self, cache_only=True):
        ''' Single funciton to be used by callers to get data '''

        self.load_tweets(cache_only)
        df = pd.read_json(self.file_name, orient='records')
        return df['text']

    def get_tweet_id_text(self, cache_only=True):
        ''' Single funciton to be used by callers to get data '''

        tweets = self.load_tweets(cache_only)
        df = pd.read_json(self.file_name, orient='records')
        return df[['id', 'text']]

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
                if(int(tweet['id_str']) > since_id):
                    since_id = int(tweet['id_str'])
        return since_id

    def join_tweets(self, tweets1, tweets2):
        ''' Given two lists of tweets, join them and make them unique'''

        ids = defaultdict(lambda: 0)
        out_tweets = []

        if(tweets1 is not None):
            for tweet in tweets1:
                ids[int(tweet["id_str"])] += 1
            out_tweets = tweets1

        if(tweets2 is not None):
            for tweet in tweets2:
                if(tweet["id"] not in ids):
                    ids[int(tweet["id_str"])] += 1
                    out_tweets.append(tweet)
        return out_tweets

    def sort_tweets(self, tweets):
        ''' Sort list of tweets by the id field, putting them in
        chronological order '''

        return sorted(tweets, key=lambda x: int(x["id_str"]), reverse=True)

    def save_tweets(self, tweets):
        ''' Write all tweets to person's file '''

        with open(self.file_name, 'w') as outfile:
            json.dump(tweets, outfile)

    def more_timeline(self):
        # OAuth process, using the keys and tokens
        auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # Creation of the actual interface, using authentication
        api = tw.API(auth)

        i = 0
        for status in tw.Cursor(api.user_timeline, screen_name=self.name, tweet_mode="extended").items():
            print("{} {}".format(i, status.full_text))
            i += 1
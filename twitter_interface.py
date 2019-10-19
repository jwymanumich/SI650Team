from datetime import datetime
import json
import os
import tweepy as tw
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

def GetTweets(name, cache_only, count=100):

    file_name = name + '.json'
    l = list()
    since_id = 1

    if(os.path.isfile(file_name)):
        with open(file_name, 'r') as infile:
            l = json.loads(infile.read())

#            created_at = d[0]["created_at"]
            #Wed Nov 28 19:33:04 +0000 2018
#            datetime_object = datetime.strptime(created_at, '%a %b %d %X %z %Y')
#            date_since = datetime_object.strftime("%Y-%m-%d")#"2018-11-16"
            since_id = l[0]["id"]
#            since_id = 1044949188788682756


    if(cache_only == False):
        auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tw.API(auth, wait_on_rate_limit=True)

        t = api.user_timeline(screen_name=name, count=count, since_id=since_id)

        l2 = list()

        with open(file_name, 'w') as outfile:
            # Iterate and print tweets
            for tweet in t:
                print(tweet.text)
                l2.append(tweet._json)
            l = l2 + l
            json.dump(l, outfile)
            
    return l[0:count]
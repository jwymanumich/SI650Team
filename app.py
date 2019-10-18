import json
import mytwitter
import os
import pandas as pd
import tweepy as tw

mytwitter.AFunction()

with open('config.json') as json_file:
    data = json.load(json_file)
    consumer_key = 'yourkeyhere'
    consumer_secret = 'yourkeyhere'
    access_token = 'yourkeyhere'
    access_token_secret = 'yourkeyhere'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = "#wildfires"
date_since = "2018-11-16"

tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(5)

# Iterate and print tweets
for tweet in tweets:
    print(tweet.text)

print("test checkin2s2")
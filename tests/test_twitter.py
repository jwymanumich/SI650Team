''' Module for running all unit tests in this space '''

import json
import unittest

from twitter_interface import TwitterWrapper

DATA_EMPTYLIST = json.loads("[]")

DATA_ONE_ITEM = json.loads("[{\
        \"created_at\": \"Wed Nov 28 19:33:04 +0000 2018\",\
        \"id\": 1067863966829801500}]")

DATA_TWO_ITEMS = json.loads("[{\
        \"created_at\": \"Wed Nov 28 19:33:04 +0000 2018\",\
        \"id\": 1067863966829801500},\
        {\
        \"created_at\": \"Wed Nov 28 19:33:04 +0000 2018\",\
        \"id\": 1067863966829801400}]")

class TestTwitterMostRecent(unittest.TestCase):
    ''' Testset for working with twitter interface'''

    def setUp(self):
        self.mytwitterwrapper = TwitterWrapper("Matt_LeBlanc")

    def test_since_one_value(self):
        ''' Confirm that since works with one item '''
        since = self.mytwitterwrapper.get_recent_tweet_id(DATA_ONE_ITEM)
        self.assertEqual(1067863966829801500, since)

    def test_since_zero_values(self):
        ''' Confirm that an empty json list returns 1'''
        self.assertEqual(1, self.mytwitterwrapper.get_recent_tweet_id(DATA_EMPTYLIST))

    def test_since_null_values(self):
        ''' Confirm that an empty json list returns 1'''

        self.assertEqual(1, self.mytwitterwrapper.get_recent_tweet_id(None))

    def test_since_two_values_first(self):
        '''Confirm that the max value is found in a list if it is the first value'''
        since = self.mytwitterwrapper.get_recent_tweet_id(DATA_TWO_ITEMS)
        self.assertEqual(1067863966829801500, since)

    def test_since_two_values_second(self):
        '''Confirm that max value is found if it isn't the first value'''

        since = self.mytwitterwrapper.get_recent_tweet_id(DATA_TWO_ITEMS)
        self.assertEqual(1067863966829801500, since)

class TestTwitterJoin(unittest.TestCase):
    ''' Testset for working with twitter interface'''

    def setUp(self):
        self.mytwitterwrapper = TwitterWrapper("Matt_LeBlanc")

    def test_jointweets_two_duplicate(self):
        '''Confirm joining two dupes makes the correct list of two items'''
        tweets_out = self.mytwitterwrapper.join_tweets(DATA_TWO_ITEMS, DATA_TWO_ITEMS)
        self.assertEqual(len(tweets_out), 2)

    def test_jointweets_two_null_values(self):
        '''Confirm that max value is found if it isn't the first value'''

        tweets_out = self.mytwitterwrapper.join_tweets(None, None)
        self.assertEqual(len(tweets_out), 0)

if __name__ == '__main__':
    unittest.main()

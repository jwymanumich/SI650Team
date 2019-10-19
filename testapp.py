''' Module for running all unit tests in this space '''

import json
import unittest
from twitter_interface import TwitterWrapper

class TestTwitterInterface(unittest.TestCase):
    ''' Testset for working with twitter interface'''

    def setUp(self):
        self.mytwitterwrapper = TwitterWrapper("Matt_LeBlanc")

        self.data_emptylist = json.loads("[]")

        self.data_one_item = json.loads("[{\
                \"created_at\": \"Wed Nov 28 19:33:04 +0000 2018\",\
                \"id\": 1067863966829801500}]")

        string_data = "[{\
                \"created_at\": \"Wed Nov 28 19:33:04 +0000 2018\",\
                \"id\": 1067863966829801500},\
                {\
                \"created_at\": \"Wed Nov 28 19:33:04 +0000 2018\",\
                \"id\": 1067863966829801400}]"
        self.data_two_items = json.loads(string_data)

    def since_one_value(self):
        ''' Confirm that since works with one item '''
        since = self.mytwitterwrapper.get_recent_tweet_id(self.data_one_item)
        self.assertEqual(1067863966829801500, since)

    def since_zero_values(self):
        ''' Confirm that an empty json list returns 1'''
        self.assertEqual(1, self.mytwitterwrapper.get_recent_tweet_id(self.data_emptylist))

    def since_null_values(self):
        ''' Confirm that an empty json list returns 1'''

        self.assertEqual(1, self.mytwitterwrapper.get_recent_tweet_id(None))

    def since_two_values_first_value(self):
        '''Confirm that the max value is found in a list if it is the first value'''
        since = self.mytwitterwrapper.get_recent_tweet_id(self.data_two_items)
        self.assertEqual(1067863966829801500, since)

    def since_two_values_second_value(self):
        '''Confirm that max value is found if it isn't the first value'''

        since = self.mytwitterwrapper.get_recent_tweet_id(self.data_two_items)
        self.assertEqual(1067863966829801500, since)

    def jointweets_two_duplicate_values(self):
        '''Confirm joining two dupes makes the correct list of two items'''
        tweets_out = self.mytwitterwrapper.join_tweets(self.data_two_items, self.data_two_items)
        self.assertEqual(len(tweets_out), 2)

    def jointweets_two_null_values(self):
        '''Confirm that max value is found if it isn't the first value'''

        tweets_out = self.mytwitterwrapper.join_tweets(None, None)
        self.assertEqual(len(tweets_out), 0)


if __name__ == '__main__':
    unittest.main()

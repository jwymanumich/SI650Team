''' Basic app where all of the processing happens '''

from ir_work import load_data
from twitter_interface import TwitterWrapper


def do_main():
    ''' A place to do all of the main work for now '''
    tw_handle = TwitterWrapper("Matt_LeBlanc")

    inverted_index, my_collection = load_data(tw_handle.load_tweets(cache_only=True), [])

    print("do_main complete")

do_main()

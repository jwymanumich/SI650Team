''' Basic app where all of the processing happens '''

import sys
import json

from ir_work import load_data
from twitter_interface import TwitterWrapper
from topic_modeling_draft_si_650 import get_topic_models

from flask import Flask
from flask import request

app = Flask(__name__)

INVERTED_INDEX = None
MY_COLLECTION = None

I = 111

@app.route("/twitterid/<twitter_id>/topics/<topic_count>")
def twitter_id_topics(twitter_id, topic_count):
    global I
    I *= 2
    tw_handle = TwitterWrapper(twitter_id)

    cache_only = True
    if(request.args.get('force_call') is not None):
        cache_only = False

    df = tw_handle.get_tweet_text(cache_only=cache_only)
    return get_topic_models(df, n_top_words = int(topic_count))

@app.route("/twittername/<twitter_name>/topics/<topic_count>")
def twitter_name_topics(twitter_name, topic_count):
    global I
    I *= 2
    tw_handle = TwitterWrapper("")
    tw_handle.set_screen_name(twitter_name)

    cache_only = True
    if(request.args.get('force_call') is not None):
        cache_only = False

    df = tw_handle.get_tweet_text(cache_only=cache_only)
    return get_topic_models(df, n_top_words = int(topic_count))


@app.route("/inverted_index")
def inverted_index():
    global INVERTED_INDEX, MY_COLLECTION
    word = request.args.get('word')
    return "{}".format(INVERTED_INDEX.word_count(word))

@app.route("/<name>/random_tweet")
def random_tweet(name):
    global INVERTED_INDEX, MY_COLLECTION
    tw_handle = TwitterWrapper(name)

    INVERTED_INDEX, MY_COLLECTION = load_data(tw_handle.load_tweets(cache_only=True), [])

    document = MY_COLLECTION.get_document(1)

    return_value = {'id': document.document_id}
    return json.dumps(return_value)

@app.route("/words/")
def do_main():
    ''' A place to do all of the main work for now '''
    tw_handle = TwitterWrapper("4348237453")

    global INVERTED_INDEX, MY_COLLECTION

    word = request.args.get('user')
#    eprint(word)
    INVERTED_INDEX, MY_COLLECTION = load_data(tw_handle.load_tweets(cache_only=True), [])
#    return(load_data(tw_handle.load_tweets(cache_only=True), []))
    return "{}".format(INVERTED_INDEX.word_count(word))
#    print("do_main complete")
#do_main()

#def eprint(*args, **kwargs):
#    print(*args, file=sys.stderr, **kwargs)


''' Basic app where all of the processing happens '''

import sys
import json

from ir_work import load_data
from twitter_interface import TwitterWrapper
from flask import Flask
from flask import request

app = Flask(__name__)

INVERTED_INDEX = None
MY_COLLECTION = None

I = 111
@app.route("/anotherpath")
def home():
    global I
    I *= 2
    return "Hello, Flask!"

@app.route("/yomama")
def home2():
    global I
    return ("zzzHeffllo, Flask {} {}!".format("asdf", I))

@app.route("/inverted_index")
def inverted_index():
    global INVERTED_INDEX, MY_COLLECTION
    word = request.args.get('word')
    return "{}".format(INVERTED_INDEX.word_count(word))

@app.route("/random_tweet")
def random_tweet():
    global INVERTED_INDEX, MY_COLLECTION
    tw_handle = TwitterWrapper("4348237453")

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

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


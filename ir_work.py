''' file that handles code for parsing tweet text and doing TFIDF type things '''

import math

from document import Document
from invertedindex import InvertedIndex

class Collection():
    ''' Just a bunch of documents '''
    def __init__(self):
        self._documents = []
        self.num_docs = 0
        self.avg_dl = None

    def add_document(self, cur_document):
        ''' Add a document to this collection '''
        self._documents.append(cur_document)
        self.num_docs = len(self._documents)
        self.avg_dl = None

    def get_document(self, index):
        ''' Access a document in this collection '''
        return self._documents[index]

    def get_documents(self):
        ''' Access a document in this collection '''
        return self._documents

    def get_avg_dl(self):
        ''' get length of average document as a decimal '''

        if(self.avg_dl is None):
            total_size = sum([len(item._words) for item in self._documents])
            self.avg_dl = total_size / self.num_docs
        return self.avg_dl

    def get_doc_count(self):
        ''' get the total number of documents in the collection '''
        return self.num_docs

"""
sd.num_docs: total number of documents in the index
sd.avg_dl: average document length of the collection
sd.total_terms: total number of terms in the index
sd.corpus_term_count: number of times a term t_id appears in the collection

sd.doc_count: number of documents that a term t_id appears in
sd.doc_term_count: number of times the term appears in the current document
sd.doc_size: total number of terms in the current document
sd.doc_unique_terms: number of unique terms in the current document

sd.query_length: the total length of the current query (sum of all term weights)
sd.query_term_weight: query term count (or weight in case of feedback)
"""

def score_one_bm25(word, document, inverted_index, collection, k1, b, k3):

    num_docs = collection.get_doc_count()
    doc_count = len(inverted_index.get_word_info(word)['doc_ids'])
#    doc_term_count = inverted_index.get_word_info(word)['document_frequency']
    doc_term_count = document.term_count(word)
    avg_dl = collection.get_avg_dl()
    doc_unique_terms = document.total_term_count()

    idf_value = float(num_docs - doc_count + 0.5) / float(doc_count + 0.5)
    numerator = (float(k1 + 1) * doc_term_count)
    denominator = (k1 * (1 - b + b * (float(doc_unique_terms)/avg_dl)) + doc_term_count)
    r = math.log(idf_value) * (numerator / denominator) 
#        * (((k3 + 1) * sd.query_term_weight) / (k3 + sd.query_term_weight))
    return r

def score_tf_idf(word, document, inverted_index, collection, k1, b, k3):

    doc_term_count = document.term_count(word)
    doc_count = collection.get_doc_count()
    term_document_count = inverted_index.get_term_document_count(word)

    type_freq = float(doc_term_count)/document.total_term_count()
    idf = doc_count/ term_document_count
    return type_freq * math.log(idf)

def load_data2(tweets, stop_words):
    return "A String"

def load_data(tweets, stop_words):
    ''' Load words from file, skipping items matching values
    in the provided set of stop_words'''

    my_inv_index = InvertedIndex()
    my_collection = Collection()

    friends = []
    for tweet in tweets:
        cur_document = Document(tweet['id'], tweet['text'], stop_words)

        for mention in tweet["entities"]["user_mentions"]:
#            print(mention["id"])
            friends.append(mention["id_str"])
        my_inv_index.add_document(cur_document)
        my_collection.add_document(cur_document)
#    for friend in set(friends):
#        tw_handle = TwitterWrapper(friend)
#        for tweet2 in tw_handle.load_tweets(cache_only=True):
#            print(tweet2["text"])
    i = 0
    max_value = 0
    d2 = None
    query = my_collection.get_documents()[0]
#    return "ASDFfffFF"

#    for document in my_collection.get_documents()[1:]:
#        value = 1
#        for word in query.get_words():
#            value *= score_tf_idf(word, document, my_inv_index, my_collection, k1 = 1.2, b = 0.75, k3 = 500)
#            value *= score_one_bm25(word, document, my_inv_index, my_collection, k1 = 1.2, b = 0.75, k3 = 500)

#        if(value > max_value):
#            max_value = value
#            d2 = document
    return my_inv_index, my_collection

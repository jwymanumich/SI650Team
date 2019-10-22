''' file that handles code for parsing tweet text and doing TFIDF type things '''

from document import Document
from invertedindex import InvertedIndex

"""
sd.num_docs: total number of documents in the index
sd.avg_dl: average document length of the collection
sd.total_terms: total number of terms in the index
sd.doc_count: number of documents that a term t_id appears in
sd.corpus_term_count: number of times a term t_id appears in the collection

sd.doc_term_count: number of times the term appears in the current document
sd.doc_size: total number of terms in the current document
sd.doc_unique_terms: number of unique terms in the current document

sd.query_length: the total length of the current query (sum of all term weights)
sd.query_term_weight: query term count (or weight in case of feedback)
"""

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

    def get_avg_dl(self):
        ''' get length of average document as a decimal '''

        if(self.avg_dl is None):
            total_size = sum([len(item._words) for item in self._documents])
            self.avg_dl = total_size / self.num_docs
        return self.avg_dl

    def get_doc_count(self):
        ''' get the total number of documents in the collection '''
        return self.num_docs


def load_data(tweets, stop_words):
    ''' Load words from file, skipping items matching values
    in the provided set of stop_words'''

    my_inv_index = InvertedIndex()
    my_collection = Collection()

    for tweet in tweets:
        cur_document = Document(tweet['text'], stop_words)
        my_inv_index.add_document(cur_document)
        my_collection.add_document(Document)

    return my_inv_index, my_collection

''' file that handles code for parsing tweet text and doing TFIDF type things '''

from collections import defaultdict
import re
import nltk
from nltk.stem import PorterStemmer

class collection():
    ''' Just a bunch of documents '''
    def __init__(self):
        self.documents = []

    def add_document(self, cur_document):
        self.documents.append(cur_document)

    def get_document(self, index):
        return self.documents[index]

class document():
    ''' Represnet documents for inverted_index and collection
    processing '''

    def __init__(self, line, stop_words):
        self.line = line
        self.words = []
        self.pos = []
        self.stop_word = []

        stemmer = PorterStemmer()

        line_tok = nltk.word_tokenize(self.line)
        
        for word_pos in nltk.pos_tag(line_tok):
            cur_word = word_pos[0].lower()
            stemmed_word = stemmer.stem(cur_word)

            if(re.search("[a-zA-Z]", stemmed_word) is not None):
                self.words.append(cur_word)
                self.pos.append(word_pos[1])
                self.stop_word.append(cur_word in stop_words)

class inverted_index():
    ''' To be used for all inverted_index needs '''

    def __init__(self):
        print("New II")
        self.words = {}
        self.cur_record = 0

    def add_document(self, cur_document):
        for item, word in enumerate(cur_document.words):
            
            if(word not in self.words):
                self.words[word] = {}
                self.words[word]['total_frequency'] = 0
                self.words[word]['doc_ids'] = []
                self.words[word]['document_frequency'] = []

            inverted_index_item = self.words[word]
            inverted_index_item['total_frequency'] += 1
            inverted_index_item['POS'] = cur_document.pos[item]

            if(self.cur_record not in inverted_index_item['doc_ids']):
                inverted_index_item['doc_ids'].append(self.cur_record)
                inverted_index_item['document_frequency'].append(1)
            else:
                index = inverted_index_item['doc_ids'].index(self.cur_record)
                inverted_index_item['document_frequency'][index] += 1

        self.cur_record += 1

def load_data(tweets, stop_words):
    ''' Load words from file, skipping items matching values
    in the provided set of stop_words'''

    my_inv_index = inverted_index()
    my_collection = collection()

    for tweet in tweets:
        cur_document = document(tweet['text'], stop_words)
        my_inv_index.add_document(cur_document)
        my_collection.add_document(document)

    return my_inv_index, my_collection

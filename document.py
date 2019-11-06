''' Everything having to do with the parsing of a document for evaluation '''

import re

import nltk
from nltk.stem import PorterStemmer

class Document():
    ''' Represnet documents for inverted_index and collection
    processing '''

    def __init__(self, document_id, line, stop_words):
        self.line = line
        self.document_id = document_id

        self._words = []
        self._pos = []
        self._stop_word = []
        stemmer = PorterStemmer()

        line_tok = nltk.word_tokenize(self.line)

        for word_pos in nltk.pos_tag(line_tok):
            cur_word = word_pos[0].lower()
            stemmed_word = stemmer.stem(cur_word)

            if(re.search("[a-zA-Z]", stemmed_word) is not None):
                self._words.append(cur_word)
                self._pos.append(word_pos[1])
                self._stop_word.append(cur_word in stop_words)

        self._total_words = len(self._words)

        self._term_frequency = {}
        self._word_counts = {}
        for word in self._words:
            if word not in self._word_counts:
                self._word_counts[word] = 0
            self._word_counts[word] += 1
            self._term_frequency[word] = float(self._word_counts[word]) / len(self._words)

    def get_words(self):
        ''' Get the words '''
        return self._words

    def term_count(self, term):
        ''' count occurrences of term in document '''

        count = 0
        if(term in self._words):
            count = self._word_counts[term]
        return count

    def total_term_count(self):
        ''' Total number of terms in this document '''
        return self._total_words

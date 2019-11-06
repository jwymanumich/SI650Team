''' File to house the implementation of the inverted index
'''

class InvertedIndex():
    ''' To be used for all inverted_index needs '''

    def __init__(self):
        ''' make index, default ctor '''
        self._words = {}
        self._cur_record = 0

    def add_document(self, cur_document):
        ''' Add a document of data to the inverted index '''

        for word in cur_document.get_words():

            if(word not in self._words):
                self._words[word] = {}
                self._words[word]['total_frequency'] = 0
                self._words[word]['doc_ids'] = []
                self._words[word]['document_frequency'] = []

            inverted_index_item = self._words[word]
            inverted_index_item['total_frequency'] += 1
            inverted_index_item['POS'] = cur_document.get_pos(word)

            if(self._cur_record not in inverted_index_item['doc_ids']):
                inverted_index_item['doc_ids'].append(self._cur_record)
                inverted_index_item['document_frequency'].append(1)
            else:
                index = inverted_index_item['doc_ids'].index(self._cur_record)
                inverted_index_item['document_frequency'][index] += 1

        self._cur_record += 1

    def total_terms(self):
        ''' get the total number of unique terms in the collection '''
        return len(self._words)

    def word_count(self, word):
        ''' Get the total number of occurrences of a term '''
        count = 0
        if(word in self._words):
            count = self._words[word]["total_frequency"]
        return count

    def get_word_info(self, word):
        ''' return information for the word provided'''
        return self._words[word]

    def get_term_document_count(self, word):
        ''' get the number of documents that this word appeared in '''
        return len(self._words[word]['doc_ids'])

''' Module for running all unit tests of inverted index '''

import unittest

from invertedindex import InvertedIndex
from ir_work import Document

class TestInvertedIndex(unittest.TestCase):
    ''' Testset for working with inverted index data '''


    def setUp(self):
        ''' setup for tests '''
        document1 = Document(1, "this is a document", [])
        document2 = Document(2, "this is not a document", [])

        self.inverted_index = InvertedIndex()
        self.inverted_index.add_document(document1)
        self.inverted_index.add_document(document2)

    def test_invertedindex_word_count(self):
        ''' Test the the count of term is correct '''
        self.assertEqual(self.inverted_index.word_count("a"), 2)

    def test_invertedindex_zero_count(self):
        ''' Test the the count of term is correct '''
        self.assertEqual(self.inverted_index.word_count("aaa"), 0)


if __name__ == '__main__':
    unittest.main()

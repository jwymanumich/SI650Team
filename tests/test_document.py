''' Module for running all unit tests in this space '''

import json
import unittest

from ir_work import document

class TestDocumentLoad(unittest.TestCase):
    ''' Testset for working with document data '''

    def setUp(self):
        print("Setup Document Test")

    def test_document_basicwordcount(self):
        my_doc = document("a man a plan a canal pamama", [])
        self.assertEqual(len(my_doc.words), 7)

    def test_document_partofspeech(self):
        my_doc = document("a man a plan a canal pamama", [])
        self.assertEqual(my_doc.pos[6], "NN")

    def test_skip_only_numbers(self):
        my_doc = document("999", [])
        self.assertEqual(len(my_doc.words), 0)

    def test_skip_only_chars(self):
        my_doc = document("@#$", [])
        self.assertEqual(len(my_doc.words), 0)


if __name__ == '__main__':
    unittest.main()

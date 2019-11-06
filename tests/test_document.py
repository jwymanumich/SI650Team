''' Module for running all unit tests in this space '''

import unittest

from ir_work import Document

class TestDocumentLoad(unittest.TestCase):
    ''' Testset for working with document data '''

    def setUp(self):
        ''' setup for tests '''

        self.basic_document = Document(111, "a man a plan a canal panama", [])
        print("Setup Document Test")

    def test_document_basicwordcount(self):
        ''' test that the right number of words are found '''

        my_doc = self.basic_document
        self.assertEqual(len(my_doc.get_words()), 7)

    def test_skip_only_numbers(self):
        ''' test that we are not picking up numbers '''

        my_doc = Document(111, "999", [])
        self.assertEqual(len(my_doc.get_words()), 0)

    def test_skip_only_chars(self):
        ''' test that we are not picking up only special characters '''

        my_doc = Document(111, "@#$", [])
        self.assertEqual(len(my_doc.get_words()), 0)

    def test_confirm_term_count(self):
        ''' confirm that term count is set correctly '''

        my_doc = self.basic_document
        self.assertEqual(my_doc.term_count('a'), 3)
        self.assertEqual(my_doc.term_count('plan'), 1)

    def test_type_frequency(self):
        ''' confirm that term frequency is being set correctly '''

        my_doc = self.basic_document
        self.assertEqual(my_doc._term_frequency['a'], float(3)/7)
        self.assertEqual(my_doc._term_frequency['plan'], float(1)/7)

    def test_total_words(self):
        ''' confirm that the number of words are counted correctly '''

        my_doc = self.basic_document
        self.assertEqual(my_doc.total_term_count(), 7)

    def test_total_words_0(self):
        ''' confirm that the number of words are counted correctly '''

        my_doc = self.basic_document
        self.assertEqual(my_doc.term_count("asdfasdf"), 0)

    def test_document_id(self):
        ''' confirm that the document id is processed and returned correctly '''

        my_doc = self.basic_document
        self.assertEqual(my_doc.document_id, 111)


if __name__ == '__main__':
    unittest.main()

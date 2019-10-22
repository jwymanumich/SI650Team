''' Module for running all unit tests in this space '''

import unittest

from ir_work import Collection, Document

class TestCollection(unittest.TestCase):
    ''' Testset for working with document data '''

    def setUp(self):
        ''' setup for tests '''
        print("Setup Document Test")

    def test_collection_avg_dl(self):
        ''' test average document length as decimal '''

        collection = Collection()
        collection.add_document(Document("this is a document", []))
        collection.add_document(Document("this is not a document", []))

        self.assertEqual(collection.get_avg_dl(), float(4.5))


if __name__ == '__main__':
    unittest.main()

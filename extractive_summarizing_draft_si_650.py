from rouge_score import rouge_scorer
import nltk
import numpy
import numpy
import datetime
import random
import pandas as pd
from nltk.probability import FreqDist
from math import sqrt
from twitter_interface import TwitterWrapper
from mongoengine import Document, StringField, DateTimeField, IntField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, ListField


class TestDocument(object):
    def __init__(self, id, author_screen_name, author_name, date, content, url, retweet_count):
        self.id = id
        self.author_screen_name = author_screen_name
        self.author_name = author_name
        self.date = date
        self.content = content
        self.url = url
        self.retweet_count = retweet_count


class WordFrequencyTuple(EmbeddedDocument):
    word = StringField(required=True, default="Unknown")
    count = IntField(required=True, default=0)


class Content(EmbeddedDocument):
    raw = StringField(required=True, default="Unknown")
    tokens = ListField(StringField(), required=True, default=list)
    word_frequencies = ListField(EmbeddedDocumentField(
        WordFrequencyTuple), required=True, default=list)
    date = DateTimeField(required=True, default=datetime.datetime.utcnow)

    def construct_word_freq_list(self, items):
        for item in items:
            t = WordFrequencyTuple()
            t.word = item[0]
            t.count = item[1]
            self.word_frequencies.append(t)


class AbstractSummarizer(object):
    def __init__(self, documents):
        '''
        It initialises the centroid summarizer structure.
        It receives a dict of documents.
        '''
        self.documents = documents

    def summarize(self):
        raise NotImplementedError(
            "summarize() was not implemented by child class")

    def _attach_feature_vectors(self):
        '''
        Iterates over the summarizer documents and calculates a tf-idf
        weighted feature vector for each document. The feature vectors is
        attached to the document.
        '''
        corpus = nltk.TextCollection(
            [document.tokens for document in self.documents.values()])
        terms = list(set(corpus))

        for id, document in self.documents.items():
            text = nltk.Text(document.tokens)
            fv = numpy.zeros([len(set(corpus))])
            for item in document.word_frequencies:
                fv[terms.index(item.word)] = corpus.tf_idf(item.word, text)
            self.documents[id].fv = fv


class BaseSummarizer(AbstractSummarizer):
    '''
    This class implements the base algorithm for automatic text summarization,
    where the summarizer selects random "sentences" for a summary.
    Please note that a single tweet is considered as a "sentence" of the LexRank algorithm.
    '''

    def summarize(self):
        doc_list = [document for document in self.documents.values()]
        random.shuffle(doc_list)
        return doc_list


class LexRankSummarizer(AbstractSummarizer):
    '''
    This class implements the LexRank algorithm for automatic text summarization.
    The implementation is based on this paper: http://tangra.si.umich.edu/~radev/lexrank/lexrank.pdf
    Please note that a single tweet is considered as a "sentence" of the LexRank algorithm.
    '''

    def summarize(self, threshold=0.1, tolerance=0.00001):

        self._attach_feature_vectors()
        doc_list = [document for document in self.documents.values()]
        ranked_doc_list = self._rank_documents(doc_list, threshold, tolerance)

        # the bigger the distance the better
        sorted_documents = sorted(
            ranked_doc_list, key=lambda document: -document.dist)
        return sorted_documents

    def _rank_documents(self, doc_list, threshold, tolerance):
        n = len(doc_list)
        # Initialises the adjacency matrix
        adjacency_matrix = numpy.zeros([n, n])

        degree = numpy.zeros([n])
        scores = numpy.zeros([n])

        for i, documenti in enumerate(doc_list):
            for j, documentj in enumerate(doc_list):
                adjacency_matrix[i][j] = cosine(
                    documenti.fv, documentj.fv, distance=False)

                if adjacency_matrix[i][j] > threshold:
                    adjacency_matrix[i][j] = 1.0
                    degree[i] += 1
                else:
                    adjacency_matrix[i][j] = 0

        for i in range(n):
            for j in range(n):
                if degree[i] == 0:
                    degree[i] = 1.0  # at least similat to itself
                adjacency_matrix[i][j] = adjacency_matrix[i][j] / degree[i]

        scores = self.power_method(adjacency_matrix, tolerance)

        for i in range(0, n):
            doc_list[i].dist = scores[i]
        return doc_list

    def power_method(self, m, epsilon):
        n = len(m)
        p = [1.0 / n] * n
        while True:
            new_p = [0] * n
            for i in range(n):
                for j in range(n):
                    new_p[i] += m[j][i] * p[j]
            total = 0
            for x in range(n):
                total += (new_p[i] - p[i]) ** 2
            p = new_p
            if total < epsilon:
                break
        return p


def cosine(v1, v2, distance=True):
    '''
    Calculates the cosine similarity between two vectors. If distance == True we
    return the similarity multiplied by -1 in order to indicate that lower
    distances are closer similarities. The cosine sim of two close vectors
    should be almost 1 but in our clustering algorithm we take distances so
    1 must become -1 to indicate a closer distance. 
    '''
    dist = numpy.dot(v1, v2) / (sqrt(numpy.dot(v1, v1) * numpy.dot(v2, v2)))

    return dist


def get_test_data():
    content0 = Content()
    content0.raw = 'This is a document related to sports : Football, basketball, tennis, golf etc.'
    content0.tokens = ['document', 'relat', 'sport',
                       'footbal', 'basketbal', 'tenni', 'golf', 'etc']
    content0.construct_word_freq_list([('basketbal', 1), ('document', 1), ('etc', 1), (
        'footbal', 1), ('golf', 1), ('relat', 1), ('sport', 1), ('tenni', 1)])
    content0.date = datetime.datetime.utcnow

    content1 = Content()
    content1.raw = 'In this document we will be talking about basketball, football, tennis, golf and sports in general.'
    content1.tokens = ['document', 'talk', 'basketbal',
                       'footbal', 'tenni', 'golf', 'sport', 'gener']
    content1.construct_word_freq_list([('basketbal', 1), ('document', 1), (
        'footbal', 1), ('gener', 1), ('golf', 1), ('sport', 1), ('talk', 1), ('tenni', 1)])
    content1.date = datetime.datetime.utcnow

    doc0 = TestDocument(0, "test_name", "test_name",
                        datetime.datetime.utcnow, content0, "no_url", 0)
    doc1 = TestDocument(1, "test_name", "test_name",
                        datetime.datetime.utcnow, content1, "no_url", 0)

    return [doc0, doc1]


def convert_real_data(df):
    docs = []
    for index, row in df.iterrows():
        uid = row['id']
        text = row['text']

        content = Content()
        content.raw = text
        content.tokens = nltk.word_tokenize(text)
        content.date = datetime.datetime.utcnow

        fdist = FreqDist(content.tokens)
        freq_list = []
        for k in fdist.keys():
            freq_list.append((k, fdist[k]))
        content.construct_word_freq_list(freq_list)

        # content.construct_word_freq_list([('basketbal', 1), ('document', 1), (
        # 'footbal', 1), ('gener', 1), ('golf', 1), ('sport', 1), ('talk', 1), ('tenni', 1)])

        doc = TestDocument(uid, "test_name", "test_name",
                           datetime.datetime.utcnow, content, "no_url", 0)
        docs.append(doc)

    return docs


def evaluate(base=False):
    # testing done here
    handles_to_evaluate = ['elonmusk', 'barackobama', 'realdonaldtrump', 'justinbieber', 'neiltyson', 'wendys',
                           'gordonramsay', 'katyperry']

    for handle in handles_to_evaluate:
        # print handle name
        print(handle)

        # get data
        tw_handle = TwitterWrapper("")
        tw_handle.set_test_name(handle)
        df = tw_handle.get_tweet_id_text(cache_only=True)
        test_documents = convert_real_data(df)

        # run algorithm
        doc_dict = {}
        id = 0
        for doc in test_documents:
            doc_dict[id] = doc.content
            id += 1

        lrs = LexRankSummarizer(doc_dict)
        res = lrs.summarize(threshold=0.1, tolerance=0.0001)

        if base is True:
            lrs = BaseSummarizer(doc_dict)
            res = lrs.summarize()

        # test result rouge1, rouge2
        with open(f'./data/{handle}_gold.txt') as f:
            content = f.readlines()

        scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2'], use_stemmer=True)

        prediction = [doc.raw.strip() for doc in res[:50]]
        prediction = ' '.join(prediction)

        target = [x.strip() for x in content]
        target = ' '.join(target)

        scores = scorer.score(target, prediction)

        # print scores and newline
        print(scores)
        print()

    # finish confirmation
    print('done!')


def get_topic_models_graph(df, n_top_words):
    test_documents = convert_real_data(df)

    # test_documents = get_test_data()
    doc_dict = {}
    id = 0
    for doc in test_documents:
        doc_dict[id] = doc.content
        id += 1

    lrs = LexRankSummarizer(doc_dict)

    return_value = {"values": []}
    res = lrs.summarize(threshold=0.1, tolerance=0.0001)
    for doc in res[:n_top_words]:
        print(doc.dist, doc.raw)
        item = df[df['text'] == doc.raw]

        for (columnName, columnData) in item.iteritems():
            if(columnName == 'id'):
                return_value['values'].append(
                    {'id': str(columnData.values[0]), 'text': doc.raw})
    return return_value


if __name__ == '__main__':
    evaluate()
    # evaluate(base=True)

    # tw_handle = TwitterWrapper("")
    # tw_handle.set_screen_name("BarackObama")
    # df = tw_handle.get_tweet_id_text(cache_only=True)
    # get_topic_models_graph(df.head(50), 10)

# return_value = {"values": []}
    # res = lrs.summarize(threshold=0.1, tolerance=0.0001)
    # for doc in res[:n_top_words]:
    #     print(doc.dist, doc.raw)
    #     item = df[df['text'] == doc.raw]

    #     for (columnName, columnData) in item.iteritems():
    #         if(columnName == 'id'):
    #             return_value['values'].append({'id': str(columnData.values[0]), 'text':doc.raw})
    # return return_value

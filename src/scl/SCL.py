import csv
import sys
from gensim import corpora, models, similarities
import gensim
from gensim import corpora
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from collections import Counter
from nltk.corpus import stopwords
import pandas as pd

topic2FileNames = {'biology': 'biology_processed', 'cooking': 'cooking_processed', 'crypto': 'crypto_processed', 'diy': 'diy_processed', 'robotics': 'robotics_processed', 'travel': 'travel_processed'}
ROOT_DIR = '../../SmallData/'

tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')

def read_pivot_features(fileName):
    pass

def read_CSV_file(fileName):
    rawData = pd.read_csv(fileName)
    return rawData

def read_pivot_file(fileName):
    pivot_words = set()
    with open(fileName, 'r') as fh:
        for line in fh:
            pivot_words.add(line.strip())

    return pivot_words

def get_domain_specific_words(document_set, num_topics, ndomainwords, pivot_words):
    texts = []
    for document in document_set:
        raw = document.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [word for word in tokens if not word in en_stop]

        stopped_tokens = [word for word in stopped_tokens if word not in stopwords.words('english')]

        # add tokens to list
        texts.append(stopped_tokens)

    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]

    tfidf = models.TfidfModel(corpus)

    corpus_tfidf = tfidf[corpus]

    domain_words = set()

    ldamodel = gensim.models.ldamodel.LdaModel(corpus_tfidf, num_topics = num_topics, id2word = dictionary, passes = 20)

    words_per_topic = 2 * (ndomainwords // num_topics)

    for topic in range(num_topics):
        words = ldamodel.show_topic(topic, words_per_topic)
        for word, _ in words:
            if word in pivot_words:
                continue
            domain_words.add(word)

    return domain_words

if __name__ == '__main__':
    for topic, fn in topic2FileNames.iteritems():
        rawData = read_CSV_file(ROOT_DIR + fn + '.csv')
        pivot_words = read_pivot_file(ROOT_DIR + fn + '.pivots')
        print len(pivot_words)
        domain_words = get_domain_specific_words(rawData.title, 5, 100, pivot_words)
        print len(domain_words)

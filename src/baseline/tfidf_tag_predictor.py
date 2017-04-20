#!/usr/bin/python
# encoding=utf8

import csv
import nltk
from HTMLParser import HTMLParser
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
import operator
import numpy as np
import string
import sys
import re
import os

# Change the default encoding
reload(sys)
sys.setdefaultencoding('utf8')

wordCount = defaultdict(int)

swords = stopwords.words('english')

punctuations = string.punctuation

def data_clean(data):
    print('Cleaning data')
    data = data.apply(lambda x: x.lower())
    # data = data.apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())
    data = data.apply(lambda x: re.sub(r'^\W+|\W+$', ' ', x))
    data = data.apply(lambda i: ''.join(i.strip(punctuations)))
    # print('tokenize')
    data = data.apply(lambda x: word_tokenize(x))

    # Select only the nouns
    is_noun = lambda pos: pos[:2] == 'NN'
    for i in range(len(data)):
        data[i] = [word for (word, pos) in nltk.pos_tag(data[i]) if is_noun(pos)]

    # print('Remove stopwords')
    data = data.apply(lambda x: [i for i in x if i not in swords if len(i) > 2])
    # print('minor clean some wors')
    data = data.apply(lambda x: [i.split('/') for i in x])
    data = data.apply(lambda x: [i for y in x for i in y])
    # print('Lemmatizing')
    wordnet_lemmatizer = WordNetLemmatizer()
    data = data.apply(lambda x: [wordnet_lemmatizer.lemmatize(i) for i in x])
    data = data.apply(lambda x: [i for i in x if len(i) > 2])
    return data

def parseFile(fileName):
    rawData = pd.read_csv(fileName)
#     titles = data_clean(rawData.title)
#     contents = data_clean(rawData.content)
#     tags = rawData.tags
#     return (titles, contents, tags)
    return rawData


def get_frequency(documents):
    frequency = []
    frequency_sizes = []
    inverse_frequency = {}
    for i in range(len(documents)):
        title, content = documents[i]
        word_ratio = len(content) / (len(title) + 1e-3)
        if word_ratio == 0:
            word_ratio = 1
        word_count = {}

        for word in title:
            if word in word_count:
                word_count[word] = word_count[word] + word_ratio
            else:
                word_count[word] = word_ratio

        for word in content:
            if word in word_count:
                word_count[word] = word_count[word] + 1
            else:
                word_count[word] = 1

        for word in word_count:
            if word in inverse_frequency:
                inverse_frequency[word] = inverse_frequency[word] + 1
            else:
                inverse_frequency[word] = 1

        frequency_sizes.append(len(content) + 20 * len(title))
        frequency.append(word_count)

    return (frequency, frequency_sizes, inverse_frequency)

def get_vocabulary(documents):
    vocabulary = {}
    for document in documents:
        for word in document:
            if word in vocabulary:
                vocabulary[word] = vocabulary[word] + document[word]
            else:
                vocabulary[word] = document[word]
    vocabulary = sorted(vocabulary.values())

    return vocabulary

def compute_tfidf_baseline(rawData, topic):
    titles = data_clean(rawData.title)
    contents = data_clean(rawData.content)
    assert len(titles) == len(contents), 'length mismatch!'
    title_contents = zip(titles, contents)
    frequency, _, inverse_frequency = get_frequency(title_contents)
    tfidf_distribution = []
    ii = 0
    for document in frequency:
        if document == {}:
            continue
        max_frequency = sorted(document.items(), key = operator.itemgetter(1), reverse = True)[0][1]
        for word in document:
            document[word] = document[word] / (max_frequency + 1e-3) * np.log(len(frequency) / (inverse_frequency[word] + 1e-3))
            tfidf_distribution.append(document[word])
        ii += 1

    index = 1
    sorted(frequency[index].items(), key = operator.itemgetter(1), reverse = True)

    top = 3
    output = []
    for i in range(0, len(rawData)):
        prediction = sorted(frequency[i], key = frequency[i].get, reverse = True)[0:top]
        output.append([rawData.id[i], ' '.join(prediction)])

    pd.DataFrame(data = output, columns = ['id', 'tags']).to_csv(topic + '_submission.csv', index = False)


# inputFileName = ['biology_processed.csv', 'cooking_processed.csv', 'crypto_processed.csv', 'diy_processed.csv', 'robotics_processed.csv', 'travel_processed.csv']
# topic2FileNames = {'biology': 'biology_processed.csv', 'cooking': 'cooking_processed.csv', 'crypto': 'crypto_processed.csv', 'diy': 'diy_processed.csv', 'robotics': 'robotics_processed.csv', 'travel': 'travel_processed.csv', 'physics': 'test_processed.csv'}
topic2FileNames = {'physics': 'test_processed.csv'}

for topic, fn in topic2FileNames.iteritems():
    print 'Processing topic: ', topic
    rawData = parseFile('../../ProcessedData/' + fn)
    compute_tfidf_baseline(rawData, topic)

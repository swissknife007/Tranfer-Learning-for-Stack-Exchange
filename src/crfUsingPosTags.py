#!/usr/bin/python
# encoding=utf8 

import csv
from HTMLParser import HTMLParser
from collections import defaultdict
import sys  
import re
import os
import nltk

import sklearn
#import scipy.stats
#from sklearn.metrics import make_scorer
#from sklearn.cross_validation import cross_val_score
#from sklearn.grid_search import RandomizedSearchCV

import sklearn_crfsuite
#from sklearn_crfsuite import scorers
#from sklearn_crfsuite import metrics

# Change the default encoding
reload(sys)  
sys.setdefaultencoding('utf8')

def getCountOfWordInSentence(sWord, sentence):
    count = 0
    sentence = sentence.split()
    for word in sentence:
        if sWord == word:
            count = count + 1
    return count

def cleanSentence(sentence):
    sentence = re.sub('[^A-Za-z0-9]+', ' ', sentence).lower()
    sentence = re.sub(' +', ' ', sentence)
    sentence = sentence.strip()
    return sentence
    
def word2Feature(taggedOutput, i, length):
    word = taggedOutput[i]
    wordFeature = dict()

    wordFeature['prevPrevPrev'] = 'ZZZ'
    wordFeature['prevPrev'] = 'ZZZ'
    wordFeature['prev'] = 'ZZZ'
    wordFeature['current'] = word[1]
    wordFeature['next'] = 'ZZZ'
    wordFeature['nextNext'] = 'ZZZ'
    wordFeature['nextNextNext'] = 'ZZZ'

    if i - 1 >= 0:
        wordFeature['prev'] = taggedOutput[i - 1][1]
        if i - 2 >= 0:
           wordFeature['prevPrev'] = taggedOutput[i - 2][1]
           if i - 3 >= 0:
               wordFeature['prevPrevPrev'] = taggedOutput[i - 3][1]
    if i + 1 < length:
        wordFeature['next'] = taggedOutput[i + 1][1]
        if i + 2 < length:
            wordFeature['nextNext'] = taggedOutput[i + 2][1]
            if i + 3 < length:
                wordFeature['nextNextNext'] = taggedOutput[i + 3][1]

    wordFeature['prevCurrNext'] = wordFeature['prev'] + "," + wordFeature['current'] + "," + wordFeature['next']
    wordFeature['prevPrevPrevCurr'] = wordFeature['prevPrev'] + "," + wordFeature['prev'] + "," + wordFeature['current']
    wordFeature['currNextNextNext'] = wordFeature['current'] + "," + wordFeature['next'] + "," + wordFeature['nextNext']
    wordFeature['bigram1'] = wordFeature['current'] + "," + wordFeature['next']
    wordFeature['bigram2'] = wordFeature['prev'] + "," + wordFeature['current']
    wordFeature['bigram3'] = wordFeature['prevPrev'] + "," + wordFeature['prev']
    wordFeature['bigram4'] = wordFeature['next'] + "," + wordFeature['nextNext']
    wordFeature['4-gram1'] = wordFeature['prevPrev'] + "," + wordFeature['prev'] + "," + wordFeature['current'] + "," + wordFeature ['next']
    wordFeature['4-gram2'] = wordFeature['prev'] + "," + wordFeature['current'] + "," + wordFeature ['next'] + "," + wordFeature['nextNext']

    #Features for prev 3 and next 3 pos tags have been included

    return wordFeature


def parseFile(fileName):
    countTagsDictionary = dict()
    with open(fileName) as f:
        reader = csv.reader(f)
        for row in reader:
            taggedOutput = nltk.pos_tag(nltk.word_tokenize(cleanSentence(row[1])))
            rowIds.append(row[0])

            length = len(taggedOutput)
            featureVectorForWordsInSentence = [ word2Feature(taggedOutput, i, length) for i in range(length) ]
            dataX.append(featureVectorForWordsInSentence)
            outputVectorForWordsInSentence = []

            sentenceVector = []

            for word in taggedOutput:
                sentenceVector.append(word)
                val = 0
                for tag in row[3].split():
                    if word[0] == tag:
                        val = 1
                outputVectorForWordsInSentence.append(str(val))

            dataY.append(outputVectorForWordsInSentence)

            sentenceData.append(sentenceVector)



def parseFileTest(fileName):
    countTagsDictionary = dict()
    with open(fileName) as f:
        reader = csv.reader(f)
        for row in reader:
            taggedOutput = nltk.pos_tag(nltk.word_tokenize(cleanSentence(row[1])))
            rowIds.append(row[0])

            length = len(taggedOutput)
            featureVectorForWordsInSentence = [ word2Feature(taggedOutput, i, length) for i in range(length) ]
            dataXTest.append(featureVectorForWordsInSentence)

            sentenceVector = []

            for word in taggedOutput:
                sentenceVector.append(word)

            sentenceDataTest.append(sentenceVector)

#inputFileName = ['biology_processed.csv', 'cooking_processed.csv', 'crypto_processed.csv', 'diy_processed.csv', 'robotics_processed.csv']#, 'travel_processed.csv']
inputFileName = ['cooking_processed.csv']

dataX = []
dataY = []
sentenceData = []
rowIds = []

for i in range(len(inputFileName)):
   parseFile('../ProcessedData/' + inputFileName[i])

crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    #c1=0.034184189382167676,
    #c2=0.016117073705935864,
    max_iterations=100,
    all_possible_transitions=True
)

crf.fit(dataX, dataY)
#predY = crf.predict(dataX)

#i = -1
#for tags in predY:
#    i = i + 1
#    j = -1
#    rowVec = []
#    for tag in tags:
#        j = j + 1
#
#        if tag == '1':
#            rowVec.append(sentenceData[i][j][0])
#
#    print rowIds[i] + "," + ",".join(rowVec)

testFileName = ['test_processed.csv']


dataXTest = []
sentenceDataTest = []
rowIds = []

for i in range(len(testFileName)):
   parseFileTest('../ProcessedData/' + testFileName[i])

predY = crf.predict(dataXTest)

i = -1
for tags in predY:
    i = i + 1
    j = -1
    rowVec = []
    for tag in tags:
        j = j + 1

        if tag == '1':
            rowVec.append(sentenceDataTest[i][j][0])

    print rowIds[i] + "," + " ".join(rowVec)

#crf = sklearn_crfsuite.CRF(
#    algorithm='lbfgs',
#    max_iterations=100,
#    all_possible_transitions=True
#)
#params_space = {
#    'c1': scipy.stats.expon(scale=0.5),
#    'c2': scipy.stats.expon(scale=0.05),
#}
#
#labels = ['0', '1']
## use the same metric for evaluation
#f1_scorer = make_scorer(metrics.flat_f1_score,
#                        average='weighted', labels=labels)
#
## search
#rs = RandomizedSearchCV(crf, params_space,
#                        cv=3,
#                        verbose=1,
#                        n_jobs=-1,
#                        n_iter=50,
#                        scoring=f1_scorer)
#rs.fit(dataX, dataY)
#
#print('best params:', rs.best_params_)
#print('best CV score:', rs.best_score_)

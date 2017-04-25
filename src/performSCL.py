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
import numpy as np
from sparsesvd import sparsesvd
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import RidgeCV
from calculateDomainWords import get_domain_words_union_tags 
from calculatePivotWords import getPivotWords
from split_domain_data import parseFileSplitData

reload(sys)  
sys.setdefaultencoding('utf8')







#inputFileNameToDomainName = {'biology_processed.csv':'biology' , 'cooking_processed.csv':'cooking', 'crypto_processed.csv':'crypto', 'diy_processed.csv':'diy', 'robotics_processed.csv':'robotics', 'travel_processed.csv':'travel', 'test_processed.csv':'physics'}
inputFileNameToDomainName = {'robotics_processed.csv':'robotics'}




numDomainWords = 10
numPivotWords = 10
trainingPerc = 0.5

def createVocabulary(pivotWords, sourceDomainWords, targetDomainWords):
    vocabulary = dict()
    index = 1

    wordLists = [pivotWords, sourceDomainWords, targetDomainWords]

    for wordList in wordLists:
        for word in wordList:
            if word not in vocabulary:
                vocabulary[word] = index
                index + 1

    return vocabulary


def initialize():
    targetDomainName = 'physics'
    targetDomainWords = get_domain_words_union_tags(targetDomainName, numDomainWords)
    pivotWords = getPivotWords(numPivotWords)

    for fileName in inputFileNameToDomainName:
        domainName = inputFileNameToDomainName[fileName]
        if domainName == targetDomainName:
            continue

        sourceDomainWords = get_domain_words_union_tags(domainName, numDomainWords)
        vocabulary = createVocabulary(pivotWords, sourceDomainWords, targetDomainWords)
        (XLabeled, XUnlabeled) = parseFileSplitData(fileName, trainingPerc)
        labeledSourceTitleList, labeledSourceContentList, labeledSourceTags = XLabeled
        unlabeledSourceTitleList, unlabeledSourceContentList = XUnlabeled




initialize()

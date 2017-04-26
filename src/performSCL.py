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
from sklearn.linear_model import RidgeCV, LogisticRegression
from calculateDomainWords import get_domain_words_union_tags 
from calculatePivotWords import getPivotWords
from split_domain_data import parseFileSplitData
from split_domain_data import parseTestFile
import scipy


reload(sys)  
sys.setdefaultencoding('utf8')

useContent = True


def checkIfStringIsNum(string):
    ret = True

    try:
        val = float(string)
    except ValueError:
        ret = False

    return ret




#inputFileNameToDomainName = {'biology_processed.csv':'biology' , 'cooking_processed.csv':'cooking', 'crypto_processed.csv':'crypto', 'diy_processed.csv':'diy', 'robotics_processed.csv':'robotics', 'travel_processed.csv':'travel', 'test_processed.csv':'physics'}
inputFileNameToDomainName = {'robotics_processed.csv':'robotics'}




numDomainWords = 1000
numPivotWords = 1000
trainingPerc = 0.5

def getWordIndex(word, vocabularyMap):
    if word in vocabularyMap:
        return vocabularyMap[word]
    return 0

def createVocabulary(pivotWords, sourceDomainWords, targetDomainWords):
    vocabulary = dict()
    index = 1

    wordLists = [pivotWords, sourceDomainWords, targetDomainWords]

    for wordList in wordLists:
        for word in wordList:
            if word not in vocabulary:
                vocabulary[word] = index
                index = index + 1

    return vocabulary


def tokenize(sentence):
    return sentence.split(' ')


def getXForTrainingPivotClassifiers(titleList, contentList, vocabularyMap):
    vocabLength = len(vocabularyMap)

    X = np.zeros((len(titleList), vocabLength)) 

    for i, questionTitle in enumerate(titleList):
        for word in questionTitle:
            wordIndex = getWordIndex(word, vocabularyMap)
            if wordIndex == 0:
                continue

            X[i, wordIndex - 1] += 1


    if useContent:
        for i, questionContent in enumerate(contentList):
            for word in questionContent:
                wordIndex = getWordIndex(word, vocabularyMap)
                if wordIndex == 0:
                    continue

                X[i, wordIndex - 1] += 1

    #print("sum", np.sum(X))
    return X


def getYFeaturePivotPresent(pivotWord, titleList, contentList):
    Y = np.zeros((len(titleList), 1))

    for i in xrange(0, len(titleList)):
        present = 0
        if pivotWord in titleList[i]:
            present = 1
        if useContent:
            if pivotWord in contentList[i]:
                present = 1

        Y[i, 0] = present

    return Y


def getWeightVector(X, Y):
    ridgeCVFeaturePivotPresent = RidgeCV()
    #print X.shape
    #print Y.shape
    #print("Y sum", np.sum(Y))
    ridgeCVFeaturePivotPresent.fit(X, Y)

    return ridgeCVFeaturePivotPresent.coef_


def getTheta(pivotWords, titleList, contentList, vocabularyMap, h):
    WList = []

    X = getXForTrainingPivotClassifiers(titleList, contentList, vocabularyMap)

    for pivotWord in pivotWords:
        #print 'Training for pivot word '+pivotWord
        XCopy = X.copy()
        pivotIndex = getWordIndex(pivotWord, vocabularyMap)
        XCopy[:, pivotIndex - 1] = 0
        #print XCopy.shape

        YFeaturePivotPresent = getYFeaturePivotPresent(pivotWord, titleList, contentList)

        #print("Yfeature pivot shape", YFeaturePivotPresent.shape)
        Wpivot = getWeightVector(XCopy, YFeaturePivotPresent.ravel())
        #print Wpivot
        #if(np.sum(Wpivot)):
        #    print("w pivot", np.sum(Wpivot))

        WList.append(Wpivot)

    W = np.vstack(WList)
    U, _, _ = scipy.sparse.linalg.svds(W, h)
    theta = U.T

    return theta




def initialize():
    targetDomainName = 'physics'
    targetDomainWords = get_domain_words_union_tags(targetDomainName, numDomainWords)
    unlabeledTargetTitleList, unlabeledTargetContentList = parseTestFile('test_processed.csv')

    for i in range(0, len(unlabeledTargetTitleList)):
        unlabeledTargetTitleList[i] = tokenize(unlabeledTargetTitleList[i])
        unlabeledTargetContentList[i] = tokenize(unlabeledTargetContentList[i])

    pivotWords = getPivotWords(numPivotWords)

    for fileName in inputFileNameToDomainName:
        domainName = inputFileNameToDomainName[fileName]
        if domainName == targetDomainName:
            continue

        sourceDomainWords = get_domain_words_union_tags(domainName, numDomainWords)
        vocabulary = createVocabulary(pivotWords, sourceDomainWords, targetDomainWords)
        (XLabeled, XUnlabeled) = parseFileSplitData(fileName, trainingPerc)
        labeledSourceTitleList, labeledSourceContentList, labeledSourceTagList = XLabeled
        unlabeledSourceTitleList, unlabeledSourceContentList = XUnlabeled

        for i in range(0, len(labeledSourceTitleList)):
            labeledSourceTitleList[i] = tokenize(labeledSourceTitleList[i])
            labeledSourceContentList[i] = tokenize(labeledSourceContentList[i])

        for i in range(0, len(unlabeledSourceTitleList)):
            unlabeledSourceTitleList[i] = tokenize(unlabeledSourceTitleList[i])
            unlabeledSourceContentList[i] = tokenize(unlabeledSourceContentList[i])


        titleList = unlabeledTargetTitleList

        titleList.extend(unlabeledSourceTitleList)

        size1 = len(unlabeledSourceContentList)
        size2 = len(unlabeledTargetContentList)

        contentList = unlabeledTargetContentList
        contentList.extend(unlabeledSourceContentList)

        assert(len(contentList) == size1 + size2)
        
        h = 5
        getTheta(pivotWords, titleList, contentList, vocabulary, h)




initialize()

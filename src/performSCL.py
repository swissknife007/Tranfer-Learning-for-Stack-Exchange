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

reload(sys)  
sys.setdefaultencoding('utf8')

#Algorithm:
#1) Choose m pivot features
#2) Create m binary prediction problems... b_1, b_2, b_3...
#3) for k = 1 to m; find wl such that wl * x = b_k
#4) Create W = [w1|w2|w3|...]
#5) U D V = svd(W) - Done
#6) theta = U^T  (top h) - Done
#7) Train predictor on  [X; theta * X], Y - Done





def selectPivotFeatures():
    pivotFeatures = []
    return pivotFeatures;





def getWordIndex(word, vocabularyMap):
    return vocabularyMap.get(word, 0)




def getXForPivotWordForTrainingBinaryClassifier(pivotWord, tokenizedQuestionList, vocabularyMap):
    vocabLength = len(vocabularyMap)

    X = np.zeros((len(tokenizedQuestionList), vocabLength)) 
    pivotIndex = getWordIndex(pivotWord)

    for i, tokenizedQuestion in enumerate(tokenizedQuestionList):
        for word in tokenizedQuestion:
            wordIndex = getWordIndex(word, vocabularyMap)
            if wordIndex == 0:
                continue
            if pivotIndex == wordIndex:
                X[i, pivotIndex] = 0

            X[i, wordIndex] = 1

    return X


def getYFeaturePivotPresent(pivotWord, tokenizedQuestionList):
    present = 0
    for word in tokenizedQuestionList:
        if pivot == word:
            present = 1

    return present


def getWeightVectorFeaturePivotPresent(X, pivotWord, tokenizedQuestionList):
    YFeaturePivotPresent = getYFeaturePivotPresent(pivotWord, tokenizedQuestionList)
    ridgeCVFeaturePivotPresent = RidgeCV()
    ridgeCVFeaturePivotPresent.fit(X, YFeaturePivotPresent)

    return ridgeCVFeaturePivotPresent.coef_


def createPredictionProblems(pivotWord, tokenizedQuestionList, tags, vocabularyMap):
    Wpivot = []
    #remove pivot features from question matrix
    X = getXForPivotWordForTrainingBinaryClassifier(pivotWord, tokenizedQuestionList, vocabularyMap)

    WfeaturePivotPresent = getWeightVectorFeaturePivotPresent(X, pivotWord, tokenizedQuestionList)
    print WfeaturePivotPresent.shape

    Wpivot.append(WfeaturePivotPresent)

    return np.vstack(Wpivot)






def getTheta(pivotWords, tokenizedQuestionList, tags, h):
    WList = []

    for i in xrange(1, len(pivotWords)):
        Wpivot = createPredictionProblems(pivot, tokenizedQuestionList, tags)
        WList.append(Wpivot)

    W = np.vstack(WList)
    U, _, _ = sparsesvd(W.tocsc(), h)
    theta = U.T

    return theta







def createTagMap(tags):
    tagMap = dict()
    for tag in tags:
        if tag not in tagMap:
            tagMap[tag] = 1













def addPadding(inputList, padLength):
    while padLength > 0:
        inputList.append(0)
        padLength = padLength - 1

    return inputList







def getXY(tokenizedQuestionList, vocabularyMap, tagMap):
    maxLength = -1
    X = []
    Y = []

    for i in xrange(0, len(tokenizedQuestionList)):
        lenQuestion = len(tokenizedQuestionList[i])
        if lenQuestion > maxLength:
            maxLength = lenQuestion

    for i in xrange(0, len(tokenizedQuestionList)):
        tokenizedQuestion = tokenizedQuestionList[i]
        lenQuestion = len(tokenizedQuestion)
        padLength = maxLength - lenQuestion
        x = []
        y = []

        for word in tokenizedQuestion:
            x.append(getWordIndex(word))
            if word in tagMap:
                y.append(1)
            else:
                y.append(0)

        x = addPadding(x, padLength)
        y = addPadding(y, padLength)

        X.append(x)
        Y.append(y)

    return np.array(X), np.array(Y)







def createVocabularyMap(DSWords, pivotWords):
    vocabularyMap = dict()
    index = 1

    for word in DSWords:
        if word not in vocabularyMap:
            vocabularyMap[word] = index
            index = index + 1

    for word in pivotWords:
        if word not in vocabularyMap:
            vocabularyMap[word] = index
            index = index + 1


    return vocabularyMap





def trainPredictor(DSWords, pivotWords, tokenizedQuestionList, tags, h):
    theta = getTheta(pivotWords, tokenizedQuestionList, tags, h)
    tagMap = createTagMap(tags)
    vocabularyMap = createVocabularyMap(DSWords, pivotWords)
    X, Y = getXY(tokenizedQuestionList, vocabularyMap, tagMap)
    forest = RandomForestClassifier(n_estimators=100, random_state=1)
    multiOutputClassifier = MultiOutputClassifier(forest, n_jobs=-1)
    thetaX = theta * X
    XAugmented = np.concatenate(X, thetaX, axis = 0)
    multiOutputClassifier.fit(XAugmented, Y).predict(XAugmented)



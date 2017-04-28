#!/usr/bin/python
# encoding=utf8 

import operator
import sys
import numpy as np
import csv
from HTMLParser import HTMLParser
from collections import defaultdict
import sys  
import re
import os
import nltk
from calculatePMI import calculatePMIForAllDomains

reload(sys)  
sys.setdefaultencoding('utf8')


varianceThreshold = 0.5
meanThreshold = 2.5

def checkIfStringIsNum(string):
    ret = True

    try:
        val = float(string)
    except ValueError:
        ret = False

    return ret



def getGlobalVocabulary(PMIForDomainName):
    globalVocabDict = dict()
    index = 0

    for domainName in PMIForDomainName:
        PMIDomain = PMIForDomainName[domainName]
        for word in PMIDomain:
            if word not in globalVocabDict:
                globalVocabDict[word] = index
                index = index + 1

    return globalVocabDict

def getPivotCandidates(PMIForDomainName, globalVocab):
    nDomains = len(PMIForDomainName)
    pivotCandidateDict = dict()

    for word in globalVocab:
        if checkIfStringIsNum(word):
            continue

        PMIwordArray = np.zeros((nDomains, 1))
        i = 0

        for domainName in PMIForDomainName:
            PMIDomain = PMIForDomainName[domainName]
            if word in PMIDomain:
                PMIwordArray[i, 0] = PMIDomain[word]
            i = i + 1

        variance = np.var(PMIwordArray)
        mean = np.mean(PMIwordArray, axis = 0)

        if variance < varianceThreshold and mean < meanThreshold:
            pivotCandidateDict[word] = variance

    return pivotCandidateDict
        

def createVocabularyForDomainList(domainList, PMIForDomainName):
    commonVocab = defaultdict(int)
    for domainName in domainList:
        PMI = PMIForDomainName[domainName]
        for word in PMI:
            if word not in commonVocab:
                commonVocab[word] = 1

    return commonVocab


def getPivotWords(domainList, nWords):
    PMIForDomainName, globalWordCount, globalTotalWordCount, wordCountInDomainName, wordCountInDomainName, totalWordsInDomainName = calculatePMIForAllDomains()
    globalVocab = getGlobalVocabulary(PMIForDomainName)
    pivotCandidates = getPivotCandidates(PMIForDomainName, globalVocab)
    pivotCandidatesSorted = sorted(pivotCandidates.items(), key=operator.itemgetter(1), reverse=False)
    pivotList = []
    commonVocab = createVocabularyForDomainList(domainList, PMIForDomainName)

    for word, variance in pivotCandidatesSorted:
        if nWords <= 0:
            break

        if word not in commonVocab:
            continue

        #print word
        #print variance
        pivotList.append(word)
        nWords -= 1

    #for word in pivotList:
    #    print word

    return pivotList

    #TODO: return top nWords


#getPivotWords(100)

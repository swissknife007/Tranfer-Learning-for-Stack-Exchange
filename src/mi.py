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
from collections import OrderedDict

reload(sys)  
sys.setdefaultencoding('utf8')

globalWordCount = defaultdict(int)
globalTotalWordCount = 0
wordCountInDomainName = dict()
totalWordsInDomainName = defaultdict(int)
PMIForDomainName = dict()

RootFolder='../ProcessedData/' 
inputFileNameToDomainName = {'biology_processed.csv':'biology' , 'cooking_processed.csv':'cooking', 'crypto_processed.csv':'crypto', 'diy_processed.csv':'diy', 'robotics_processed.csv':'robotics', 'travel_processed.csv':'travel', 'test_processed.csv':'physics'}
#inputFileName = ['biology_processed.csv']
from calculatePivotWords import getPivotWords








def cleanSentence(sentence):
    sentence = re.sub('[^A-Za-z0-9]+', ' ', sentence).lower()
    sentence = re.sub(' +', ' ', sentence)
    sentence = sentence.strip()
    return sentence


def parseFile(fileName):
    global globalTotalWordCount
    totalCount = 0
    domainName = inputFileNameToDomainName[fileName]

    with open(RootFolder + fileName) as f:
        reader = csv.reader(f)
        wordCountInDomain = defaultdict(int)

        for row in reader:
            questionName = cleanSentence(row[1])
            questionContent = cleanSentence(row[2])
            #tags = row[3]

            wordsInQuestionName = questionName.split(' ')
            wordsInQuestionContent = questionContent.split(' ')
            
            for word in wordsInQuestionName:
                globalWordCount[word] = globalWordCount[word] + 1
                wordCountInDomain[word] = wordCountInDomain[word] + 1
                totalCount += 1
                globalTotalWordCount += 1

            for word in wordsInQuestionContent:
                globalWordCount[word] = globalWordCount[word] + 1
                wordCountInDomain[word] = wordCountInDomain[word] + 1
                totalCount += 1
                globalTotalWordCount += 1


            wordCountInDomainName[domainName] = wordCountInDomain
            totalWordsInDomainName[domainName] = totalCount



def calculatePMIForAllDomains():
    global globalTotalWordCount
    for domainName in wordCountInDomainName:
        wordCountInDomain = wordCountInDomainName[domainName]
        totalWords = totalWordsInDomainName[domainName]
        PMI = defaultdict(int)

        for word in wordCountInDomain:
            if wordCountInDomain[word] < 5:
                continue
            PwordDoc = float(wordCountInDomain[word])/totalWords
            Pword = float(globalWordCount[word])/globalTotalWordCount
            PDoc = 1.0/len(inputFileNameToDomainName)
            
            temp = PwordDoc/(Pword * PDoc)

            if temp == 0:
                PMI[word] = 0
            else:
                PMI[word] = np.log(temp)

        #for i, word in enumerate(PMISorted):
        #    print word
        #print 'XXXXXXXXXXXXXXXXX\n\n\n\n'

        PMIForDomainName[domainName] = PMI


def predictUsingMI(fileName):
    domainName = inputFileNameToDomainName[fileName]
    pivotWords = getPivotWords(['physics'], 2000)
    PMI = PMIForDomainName[domainName]
    with open(RootFolder + fileName) as f:
        reader = csv.reader(f)

        for row in reader:
            questionName = cleanSentence(row[1])
            questionContent = cleanSentence(row[2])

            wordsInQuestionName = questionName.split(' ')
            wordsInQuestionContent = questionContent.split(' ')
            
            tagDict = dict()
            for word in wordsInQuestionName:
                tagDict[word] = PMI[word]

            #for word in wordsInQuestionContent:
            #    tagDict[word] = PMI[word]

            tagCandidates = sorted(tagDict.items(), key=operator.itemgetter(1), reverse=True)

            j = 0

            predictedTags = []
            for word,val in tagCandidates:
                if j > 2:
                    break

                if word not in pivotWords and len(word) > 1:
                    j = j + 1
                    predictedTags.append(word)

            print  row[0]+',' + ' '.join(predictedTags)


for fileName in inputFileNameToDomainName:
    parseFile(fileName)

calculatePMIForAllDomains()
predictUsingMI('test_processed.csv')



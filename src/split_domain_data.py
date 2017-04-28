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


RootFolder = '../ProcessedData/'
inputFileNameToDomainName = {'biology_processed.csv': 'biology', 'cooking_processed.csv': 'cooking',
                             'crypto_processed.csv': 'crypto', 'diy_processed.csv': 'diy',
                             'robotics_processed.csv': 'robotics', 'travel_processed.csv': 'travel',
                             'test_processed.csv': 'physics'}

def cleanSentence(sentence):
    sentence = re.sub('[^A-Za-z0-9]+', ' ', sentence).lower()
    sentence = re.sub(' +', ' ', sentence)
    sentence = sentence.strip()
    return sentence


def parseTestFile(fileName):
    questionNameList = []
    questionContentList = []

    with open(RootFolder + fileName) as f:
        reader = csv.reader(f)
        wordCountInDomain = defaultdict(int)

        for row in reader:
            questionName = cleanSentence(row[1])
            questionContent = cleanSentence(row[2])
            questionNameList.append(questionName)
            questionContentList.append(questionContent)

    return questionNameList, questionContentList






def parseFileSplitData(fileName, ratio_of_labeled = 0.5):
    questionNameList = []
    questionContentList = []
    questionTagList = []
    with open(RootFolder + fileName) as f:
        reader = csv.reader(f)
        wordCountInDomain = defaultdict(int)

        for row in reader:
            questionName = cleanSentence(row[1])
            questionContent = cleanSentence(row[2])
            tagList = cleanSentence(row[3])
            tagList = tagList.split()
            questionNameList.append(questionName)
            questionContentList.append(questionContent)
            questionTagList.append(tagList)

    num_labeled_rows = int(ratio_of_labeled * len(questionContentList))

    labeled_data = (questionNameList[:num_labeled_rows], questionContentList[:num_labeled_rows], questionTagList[:num_labeled_rows])

    unlabeled_data = (questionNameList[num_labeled_rows:], questionContentList[num_labeled_rows:])

    return labeled_data, unlabeled_data

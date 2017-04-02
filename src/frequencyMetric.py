#!/usr/bin/python
# encoding=utf8 

import csv
from HTMLParser import HTMLParser
from collections import defaultdict
import sys  
import re
import os

# Change the default encoding
reload(sys)  
sys.setdefaultencoding('utf8')

wordCount = defaultdict(int)

def countFrequencyOfWords(questionName, questionContent, tags):
    wordsInQuestionName = questionName.split(' ')
    wordsInQuestionContent = questionContent.split(' ')
    individualTags = tags.split(' ')
    for words in wordsInQuestionContent:
        wordCount[words] = wordCount[words] + 1

def parseFile(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        for row in reader:
            questionName = row[1]
            questionContent = row[2]
            tags = row[3]
            countFrequencyOfWords(questionName, questionContent, tags)

#inputFileName = ['biology_processed.csv', 'cooking_processed.csv', 'crypto_processed.csv', 'diy_processed.csv', 'robotics_processed.csv', 'travel_processed.csv']
inputFileName = ['biology_processed.csv']

for i in range(len(inputFileName)):
    parseFile('../ProcessedData/' + inputFileName[i])


for key in wordCount:
    print key + ':' + str(wordCount[key])

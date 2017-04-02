#!/usr/bin/python
# encoding=utf8 

import csv
from HTMLParser import HTMLParser
import sys  
import re
import os

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
    sentence = re.sub('\.', ' ', sentence).lower()
    sentence = re.sub(' +', ' ', sentence)
    sentence = sentence.strip()
    return sentence
    

def countTagOccurenceInQuestion(questionName, questionContent, tags):
    questionName = cleanSentence(questionName)
    questionContent = cleanSentence(questionContent)
    tags = cleanSentence(tags) 

    individualTags = tags.split(' ')

    for tag in individualTags:
        print tag + " in " + questionName + "\n" + questionContent
        print getCountOfWordInSentence(tag, questionName)
        print getCountOfWordInSentence(tag, questionContent)

    print '---------------------------------'

def parseFile(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        print reader
        for row in reader:
            questionName = row[1]
            questionContent = row[2]
            tags = row[3]
            countTagOccurenceInQuestion(questionName, questionContent, tags)

#inputFileName = ['biology_processed.csv', 'cooking_processed.csv', 'crypto_processed.csv', 'diy_processed.csv', 'robotics_processed.csv', 'travel_processed.csv']
inputFileName = ['biology_processed.csv']

for i in range(len(inputFileName)):
    parseFile('../ProcessedData/' + inputFileName[i])

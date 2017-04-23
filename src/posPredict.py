#!/usr/bin/python
# encoding=utf8 

import csv
from HTMLParser import HTMLParser
from collections import defaultdict
import sys  
import re
import os
import nltk


# Change the default encoding
reload(sys)  
sys.setdefaultencoding('utf8')

#Uncomment the following line to print logs
# printCountInfo = True
printCountInfo = False



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
    

def countTagOccurenceInQuestion(questionId, questionName, questionContent, tags, countTagsDictionary):
    questionName = cleanSentence(questionName)
    questionContent = cleanSentence(questionContent)
    tags = cleanSentence(tags) 

    individualTags = tags.split(' ')

    if printCountInfo == True:
        print questionName + "\n" + questionContent + "\n"

    numberOfTags = 0
    numberOfTagsFoundInNameOrContent = 0

    for tag in individualTags:
        numberOfTags += 1
        countInName = getCountOfWordInSentence(tag, questionName)
        countInContent = getCountOfWordInSentence(tag, questionContent)
        if countInName > 0 or countInContent > 0:
            numberOfTagsFoundInNameOrContent += 1
            
        if printCountInfo == True:
            print tag + " occurrence count:"
            print "\t In question name:" + str(countInName)
            print "\t In question content:" + str(countInContent)

    if printCountInfo == True:
        print 'Finished processing'
        print '---------------------------------'
    # Make an entry in dictionary for this questionId
    countTagsDictionary[questionId] = (numberOfTagsFoundInNameOrContent, numberOfTags)

def consolidateResults(countTagsDictionary, fileName):
    percRanges = [(0 , 0), (.1, .25), (.26, .50), (.51, .75), (.76, 1.0)]
    countArr = []
    totalQuestions = 0
    rangeDictionary = defaultdict(int)

    for key in countTagsDictionary:
        totalQuestions += 1
        (numOfTagsFoundInQuestion, TotalTagsInQuestion) = countTagsDictionary[key]
        perc = float(numOfTagsFoundInQuestion) / TotalTagsInQuestion
        for (lower, upper) in percRanges:
            if perc >= lower and perc <= upper:
                rangeDictionary[(lower, upper)] += 1
                break
                
    print "\n\nFilename: " + fileName
    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    print "Total number of questions:" + str(totalQuestions)
    for key in percRanges:
        print str(key) + ":" + str(float(rangeDictionary[key]) / totalQuestions)



def parseFile(fileName):
    countTagsDictionary = dict()
    with open(fileName) as f:
        reader = csv.reader(f)
        for row in reader:
            #countTagOccurenceInQuestion(row[0], row[1], row[2], row[3], countTagsDictionary)
            output = nltk.pos_tag(nltk.word_tokenize(cleanSentence(row[1])))
            i = 0
            ans = ""
            flag = False
            ans2 = ""
            for word in output:
                i = i + 1
                ans = ans + word[0] + "(" + word[1] + ") "
                ans2 = ans2 + word[1] + " "
                for tag in row[3].split():
                    if (word[0] == tag):
                        print "tag:" + word[0] + "," + str(i)
                        flag = True
            if flag and ans2.endswith("IN NN "):
                print ans
                print ans2
                print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    #consolidateResults(countTagsDictionary, fileName)

#inputFileName = ['biology_processed.csv', 'cooking_processed.csv', 'crypto_processed.csv', 'diy_processed.csv', 'robotics_processed.csv', 'travel_processed.csv']
inputFileName = ['cooking_processed.csv']


for i in range(len(inputFileName)):
   parseFile('../ProcessedData/' + inputFileName[i])


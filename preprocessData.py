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

# Keep relevant information from the HTML tags
class HTMLSanitizer(HTMLParser):

    def __init__(self, fileHdl):
        HTMLParser.__init__(self)
        self.currentTag = ''
        self.fileHdl = fileHdl

    def handle_starttag(self, tag, attrs):
        self.currentTag = tag

    def handle_endtag(self, tag):
        None

    def handle_data(self, data):
        if self.currentTag != 'code':
            data = re.sub('[^A-Za-z0-9.]+', ' ', data)
            self.fileHdl.write(data)



def parseFile(fileName):
    with open(fileName) as f:
        print 'Processing: ' + fileName
        reader = csv.reader(f)
        splitFileName = fileName.split('.')
        splitFileName[0] = splitFileName[0] + '_processed'
        processedFileName = '.'.join(splitFileName)
        with open(processedFileName, "w") as processedF:
            parser = HTMLSanitizer(processedF)
            for row in reader:
                #Id
                processedF.write(row[0] + ',')
                #Question name
                processedF.write('"' + re.sub('[^A-Za-z0-9.]+', ' ', row[1]) + '","')
                #Question content
                parser.feed(row[2])
                #Tags
                processedF.write('","' + re.sub('[^A-Za-z0-9.]+', ' ', row[3]) + '"\n')

def parseTest(fileName):
    with open(fileName) as f:
        print 'Processing: ' + fileName
        reader = csv.reader(f)
        splitFileName = fileName.split('.')
        splitFileName[0] = splitFileName[0] + '_processed'
        processedFileName = '.'.join(splitFileName)
        with open(processedFileName, "w") as processedF:
            parser = HTMLSanitizer(processedF)
            for row in reader:
                #Id
                processedF.write(row[0] + ',')
                #Question name
                processedF.write('"' + re.sub('[^A-Za-z0-9.]+', ' ', row[1]) + '","')
                #Question content
                parser.feed(row[2])
                processedF.write('"\n')


inputFileName = ['biology.csv', 'cooking.csv', 'crypto.csv', 'diy.csv', 'robotics.csv', 'travel.csv']
testFileName = ['test.csv']

for i in range(len(inputFileName)):
    parseFile(inputFileName[i])
    os.remove(inputFileName[i])


for i in range(len(testFileName)):
    parseTest(testFileName[i])
    os.remove(testFileName[i])

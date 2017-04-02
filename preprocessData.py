#!/usr/bin/python
# encoding=utf8 

import csv
from HTMLParser import HTMLParser
import sys  
import re

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
            data = re.sub('[^A-Za-z0-9-.]+', ' ', data)
            self.fileHdl.write(data)



def parseFile(fileName):
    with open(fileName) as f:
        print fileName
        reader = csv.reader(f)
        splitFileName = fileName.split('.')
        splitFileName[0] = splitFileName[0] + '_processed'
        processedFileName = '.'.join(splitFileName)
        with open(processedFileName, "w") as processedF:
            parser = HTMLSanitizer(processedF)
            for row in reader:
                processedF.write(row[0] + ', ')
                processedF.write('"' + re.sub('[^A-Za-z0-9-.]+', ' ', row[1]) + '", "')
                parser.feed(row[2])
                processedF.write('", ' + row[3] + "\n")


inputFileName = ['biology.csv', 'cooking.csv', 'crypto.csv', 'diy.csv', 'robotics.csv', 'travel.csv']

for i in range(len(inputFileName)):
    parseFile(inputFileName[i])




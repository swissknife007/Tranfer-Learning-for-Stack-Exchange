import csv
#import nltk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from collections import  Counter, defaultdict
import sys
import re
import json

from nltk import word_tokenize

reload(sys)
sys.setdefaultencoding('utf8')

file_path = './'
file_names = []


def parse_lda_topics(file_name):
    input_file = file(file_name)
    file_content = input_file.read()
    file_content = list(file_content)
    print(type(file_content))
    for item in file_content:
        print(item)
    return file_content

def get_domain_name(file_name):
    assert(len(file_name) > 4)
    return file_name[:4]

def create_file_names():
    file_names.append(file_path + 'biology_lda.txt')
    file_names.append(file_path + 'cooking_lda.txt')
    file_names.append(file_path + 'crypto_lda.txt')
    file_names.append(file_path + 'diy_lda.txt')
    file_names.append(file_path + 'robotics_lda.txt')


create_file_names()

for file_name in file_names:
    parse_lda_topics(file_name)
    break
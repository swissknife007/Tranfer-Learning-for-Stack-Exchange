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



def get_inverted_dict():
    inverted_dict  = dict()
    for key in inputFileNameToDomainName:
        inverted_dict[inputFileNameToDomainName[key]] = key
    return inverted_dict

def get_tags(domain_name):

    tag_file = file(RootFolder + domain_name)
    tag_lines = tag_file.readlines()

    tag_dict = dict()
    for tag in tag_lines:
        tag_dict[tag[:-1]] = 1

    return tag_dict

def get_domain_words_union_tags(domain_name, num_domain_words):
    PMI_domains, _, _, _, _, _ = calculatePMIForAllDomains()
    PMI_domain = PMI_domains[domain_name]
    domain_tags = get_tags(domain_name)
    domain_words = dict()

    for word in domain_tags:
        if len(domain_words) == num_domain_words:
            break
        domain_words[word] = 1

    for word in PMI_domain:
        if len(domain_words) == num_domain_words:
            break
        domain_words[word]  = 1


    return list(domain_words.keys())



#tag_lines = get_domain_words_union_tags('physics', 100)
#print tag_lines

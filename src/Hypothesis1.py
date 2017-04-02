import csv
#import nltk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from collections import  Counter, defaultdict
import sys
import re

from nltk import word_tokenize

reload(sys)
sys.setdefaultencoding('utf8')

'''
from nltk.parse.stanford import StanfordDependencyParser

path_to_jar = 'path_to/stanford-parser-full-2014-08-27/stanford-parser.jar'
path_to_models_jar = 'path_to/stanford-parser-full-2014-08-27/stanford-parser-3.4.1-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

result = dependency_parser.raw_parse('I shot an elephant in my sleep')
dep = result.next()
list(dep.triples())

'''
file_path = './../ProcessedData/'

file_names = []
domain_pos_tag_dict_title = dict()
domain_pos_tag_dict_content = dict()
domain_freq_unigrams_dict_content = dict()
domain_freq_unigrams_dict_title = dict()
domain_freq_bigrams_dict_content = dict()
domain_freq_bigrams_dict_title = dict()
domain_tag_dict = dict()

def create_file_names():
    file_names.append(file_path + 'biology_processed.csv')
    file_names.append(file_path + 'cooking_processed.csv')
    file_names.append(file_path + 'crypto_processed.csv')
    file_names.append(file_path + 'diy_processed.csv')
    file_names.append(file_path + 'robotics_processed.csv')



def get_domain_name(file_name):
    assert(len(file_name) > 4)

    return file_name[len(file_path):-5-len('processed')]

def init_pos_dicts ():

    for file_name in file_names:
        domain_pos_tag_dict_content[get_domain_name(file_name)] = defaultdict(int)
        domain_pos_tag_dict_title[get_domain_name(file_name)] = defaultdict(int)
        domain_freq_unigrams_dict_content[get_domain_name(file_name)] = defaultdict(int)
        domain_freq_unigrams_dict_title[get_domain_name(file_name)] = defaultdict(int)
        domain_freq_bigrams_dict_content[get_domain_name(file_name)] = defaultdict(int)
        domain_freq_bigrams_dict_title[get_domain_name(file_name)] = defaultdict(int)
        domain_tag_dict[get_domain_name(file_name)] = defaultdict(int)

def get_freq_count_dict(text, n_gram):
    vectorizer = CountVectorizer(ngram_range=(n_gram, n_gram))

    # Don't need both X and transformer; they should be identical
    X = vectorizer.fit_transform([text])
    matrix_terms = np.array(vectorizer.get_feature_names())

    # Use the axis keyword to sum over rows
    matrix_freq = np.asarray(X.sum(axis=0)).ravel()
    count_dict = defaultdict(int)
    #for term, count in zip(matrix_terms, matrix_freq):
    #    count_dict[term] = matrix_freq
    return matrix_freq

def clean_word (word):
    word = word.strip(' ')
    word = word.lower()
    #re.sub(' +', ' ', word)
    word = re.sub('[^a-zA-Z0-9 \n\.]', ' ', word)
    re.sub(' +', ' ', word)
    word = word.strip(' ')

    return word

def countFrequencyOfWords(file_name, questionName, questionContent, tags):

    '''
    wordsInQuestionName = word_tokenize(questionName)
    wordsInQuestionContent = word_tokenize(questionContent)
    '''
    domain_name = get_domain_name(file_name)

    questionName = questionName.strip().replace('.', ' ')
    questionContent = questionContent.strip().replace('.', ' ')
    wordsInQuestionName = questionName.split()
    wordsInQuestionContent = questionContent.split()

    individualTags = tags.split(' ')

    for tag in individualTags:
        domain_tag_dict[domain_name][clean_word(tag)] = 1

    prev_word = '*'
    for words in wordsInQuestionContent:
        words = clean_word(words)

        domain_freq_unigrams_dict_content[domain_name][words] += 1
        domain_freq_bigrams_dict_content[domain_name][(words, prev_word)] += 1
        prev_word = words
    prev_word = '*'

    for words in wordsInQuestionName:
        words = clean_word(words)
        domain_freq_unigrams_dict_title[domain_name][words] += 1
        domain_freq_bigrams_dict_title[domain_name][(words, prev_word)] += 1
        prev_word = words

    #return domain_freq_unigrams_dict_title, domain_freq_unigrams_dict_content, domain_freq_bigrams_dict_title, domain_freq_bigrams_dict_content

def analyze_text(freq_dict, tag_dict, domain_file):

    for tag in tag_dict:
        if tag in freq_dict:
            domain_file.write(tag +  " " + str(freq_dict[tag]) +'\n')

def read_csv_file(file_name):

    domain_name = get_domain_name(  file_name)
    with open(file_name) as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        row_counter = 0
        for row in spamreader:
           row_counter += 1
           questionContent = questionName = tags = ''
           for colnum, col in enumerate(row):
            if(colnum == 2):
                questionContent = col
            if colnum == 1:
                questionName = col
            if colnum == 3:
                tags = col
            countFrequencyOfWords(file_name, questionName, questionContent, tags)
            '''
            pos_tags = nltk.pos_tag(nltk.word_tokenize(text))
            for word, pos_tag in pos_tags:
            domain_pos_tag_dict_title[domain_name][pos_tag] += 1
            '''
                #print pos_tags
                #print domain_pos_tag_dict_title

create_file_names()
init_pos_dicts()
for file_name in file_names:
    read_csv_file(file_name)
    domain_name = get_domain_name(file_name)
    '''
    print domain_freq_unigrams_dict_title[domain_name]
    print domain_freq_unigrams_dict_content[domain_name]
    print domain_freq_bigrams_dict_content[domain_name]
    print domain_freq_bigrams_dict_title[domain_name]
    '''
    print("Domain name", domain_name)
    domain_file = file(domain_name+"tag_freq.txt", 'w')
    analyze_text(domain_freq_unigrams_dict_title[domain_name], domain_tag_dict[domain_name], domain_file)
    domain_file.write(".............Content Frequencies.....")
    analyze_text(domain_freq_unigrams_dict_content[domain_name], domain_tag_dict[domain_name], domain_file)
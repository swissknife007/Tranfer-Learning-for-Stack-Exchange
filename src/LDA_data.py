import csv
import sys

import gensim
from gensim import corpora
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words

reload(sys)

file_path = './../ProcessedData/'
file_names = []

def get_domain_name(file_name):
    assert(len(file_name) > 4)

def create_file_names():
    file_names.append(file_path + 'biology_processed.csv')
    file_names.append(file_path + 'cooking_processed.csv')
    file_names.append(file_path + 'crypto_processed.csv')
    file_names.append(file_path + 'diy_processed.csv')
    file_names.append(file_path + 'robotics_processed.csv')

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

doc_set = []
def read_csv_file(file_name):

    domain_name = get_domain_name(  file_name)
    with open(file_name) as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        row_counter = 0
        for row in spamreader:
           row_counter += 1
           if(row_counter > 100):
               break
           questionContent = questionName = tags = ''
           for colnum, col in enumerate(row):
            if(colnum == 2):
                questionContent = col
            if colnum == 1:
                questionName = col
            if colnum == 3:
                tags = col
            doc = questionContent + questionName
            doc_set.append(doc)
            '''
            pos_tags = nltk.pos_tag(nltk.word_tokenize(text))
            for word, pos_tag in pos_tags:
            domain_pos_tag_dict_title[domain_name][pos_tag] += 1
            '''
                #print pos_tags
                #print domain_pos_tag_dict_title


create_file_names()
'''
# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health."


# compile sample documents into a list
doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

'''

# list for tokenized documents in loop
texts = []
doc_set = doc_set[:100]
for file in file_names:
    read_csv_file(file)
# loop through document list
for i in doc_set:
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=20)

print(ldamodel.print_topics(num_topics=3, num_words=10))
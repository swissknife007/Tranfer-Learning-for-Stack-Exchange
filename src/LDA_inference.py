import csv
import sys
from gensim import corpora, models, similarities
import gensim
from gensim import corpora
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from collections import Counter
from nltk.corpus import stopwords




reload(sys)

file_path = './../ProcessedData/'
file_names = []


    

def create_file_names():
    #file_names.append(file_path + 'biology_processed.csv')
    #file_names.append(file_path + 'cooking_processed.csv')
    #file_names.append(file_path + 'crypto_processed.csv')
    #file_names.append(file_path + 'diy_processed.csv')
    file_names.append(file_path + 'robotics_processed.csv')
    #file_names.append(file_path + 'test_processed.csv')

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()


def read_csv_file(file_ptr, return_tags = False):

    doc_set = []
    doc_set_titles = []
    doc_set_contents = []
    doc_ids = []
    doc_tags = []
    #domain_name = get_domain_name(  file_name)
    #print("file_name", file_ptr)
    with open(file_ptr,'rU') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        row_counter = 0
        for row in spamreader:
           row_counter += 1
           if(row_counter > 10):
               break
           questionContent = questionName = tags = ''
           for colnum, col in enumerate(row):
            if(colnum == 2):
                questionContent = col
            if colnum == 1:
                questionName = col
            if colnum == 3:
                tags = col.split()
            if colnum == 0:
		q_id = col 
           doc = questionName + questionName + questionContent
           doc_set.append(doc)
           doc_set_titles.append(questionName)
           doc_set_contents.append(questionContent)
           doc_ids.append(q_id)
           doc_ids.append(tags)

    if return_tags == False:
 	   return doc_set, doc_set_titles, doc_set_contents, doc_ids

    return doc_set, doc_set_titles, doc_set_contents, doc_ids, doc_tags


def train():

	for file_name in file_names:
		texts = []
		doc_set, doc_titles,doc_content, _ ,  doc_tags = read_csv_file(file_name, True)
		tag_dict = Counter()
		title_dict = Counter()
		content_dict = Counter()
		title_tag_dict = Counter()
		content_tag_dict = Counter()
		mutual_tag_title_dict = dict()
		mutual_tag_content_dict = dict()

		for tag in doc_set:

			tag_dict[tag] += 1
		
		for i in doc_titles:
        
       			raw = i.lower()
        		tokens = tokenizer.tokenize(raw)

       
        		stopped_tokens = [i for i in tokens if not i in en_stop]
	
        		stopped_tokens = [word for word in stopped_tokens if word not in stopwords.words('english')]

       			
        		texts.append(stopped_tokens)
			
			for token in token_words:

				title_dict[token] += 1
						
		for i in doc_content:
        
       			raw = i.lower()

        		tokens = tokenizer.tokenize(raw)

       
        		stopped_tokens = [i for i in tokens if not i in en_stop]
	
        		stopped_tokens = [word for word in stopped_tokens if word not in stopwords.words('english')]

       			
        		texts.append(stopped_tokens)
			
			for token in token_words:

				content_dict[token] += 1

		
		for token in title_dict:

			token_dict[token] += 1

			for tag in tag_dict:

				title_tag_dict[(tag, token)] += 1

					
		for token in content_dict:

			content_dict[token] += 1

			for tag in tag_dict:

				content_tag_dict[(tag, token)] += 1
		
		
							
create_file_names()
train()


for file_ptr in file_names:
    texts = []
    #doc_set = doc_set[:100]
    #print("file_name", file_ptr)
    doc_set, _, _, _ = read_csv_file(file_ptr)
    doc_set = doc_set[:]
# loop through document list
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]
	
        stopped_tokens = [word for word in stopped_tokens if word not in stopwords.words('english')]
	
	
        # stem tokens
        #stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        # add tokens to list
        texts.append(stopped_tokens)

     
    dictionary = corpora.Dictionary(texts)

       
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    num_topics = 10
    dict_words = Counter()
    ldamodel = gensim.models.ldamodel.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dictionary, passes=20)

    #ldamodel.get_document_topics()
    #print(ldamodel.print_topics(num_topics=20, num_words=40))
    #break

    for topic in range(num_topics):
        words = ldamodel.show_topic(topic, 40)
        for word,_ in words:
            dict_words[word] = 1

    print(len(dict_words))
    _, doc_set_titles,doc_set_contents, doc_ids = read_csv_file(file_ptr)

    output_file = file('submission_90.csv', 'w')
    output_file.write("\"id\", \"tags\"\n")

    #print("doc size", len(doc_ids))

    doc_counter = 0

    for (title, content, qid) in zip(doc_set_titles, doc_set_contents, doc_ids):

        title_words = title.split(" ")
	content_words = content.split(" ")
	tag_dict = Counter()

        #print("title_Words", title_words)

        for title_word in title_words:
            if title_word in dict_words:
                 tag_dict[title_word] += 1

        
        #print("content words", content_words)
        for content_word in content_words:
            if content_word in dict_words:
                tag_dict[content_word] += 1
        #print(topic_terms)
    
    	predicted_tags = tag_dict.most_common(3)

    	tag_str = '\"'

    	for  word, count in predicted_tags:
        	tag_str += word + ' '
        if(tag_str[-1] == ' '):
		tag_str = tag_str[:-1]
        tag_str += '\"'
        qid = "\"" + str(qid) + "\""
    	output_file.write(str(qid) + "," + tag_str + '\n')
	print (doc_counter)
	doc_counter += 1

    output_file.close()

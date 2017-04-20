from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn import preprocessing
from sklearn.datasets import dump_svmlight_file
from pivot_selection import MISelector
from bolt.io import MemoryDataset

topic2FileNames = {'biology': 'biology_processed', 'cooking': 'cooking_processed', 'crypto': 'crypto_processed', 'diy': 'diy_processed', 'robotics': 'robotics_processed', 'travel': 'travel_processed'}
ROOT_DIR = '../../ProcessedData/'

def parseFile(fileName):
    rawData = pd.read_csv(fileName)
    return rawData

def dump_data(X, y, vocabulary, classes, svmFileName, vocFileName, classesFileName):
    dump_svmlight_file(X, y, svmFileName)
    write_list_to_file(vocabulary, vocFileName)
    write_list_to_file(classes, classesFileName)

def countvectorize(X_q, y_q):
    X_vectorizer = CountVectorizer(stop_words = 'english', max_df = 0.90, min_df = 5)
    # X_vectorizer = CountVectorizer()
    X_counts = X_vectorizer.fit_transform(X_q)
    if y_q != None:
        le = preprocessing.LabelEncoder()
        y_counts = le.fit_transform(y_q)
        return X_counts, y_counts, X_vectorizer.vocabulary_, le.classes_
    else:
        return X_counts, None, X_vectorizer.vocabulary_, None

def write_list_to_file(lst, lstFileName):
    with open(lstFileName, 'w') as fh:
        for word in lst:
            fh.write(word)
            fh.write('\n')

def convert_multilabel_to_single_label(rawData):

    assert len(rawData.title) == len(rawData.tags)
    assert len(rawData.content) == len(rawData.tags)
    titles = rawData.title
    contents = rawData.content
    tags = rawData.tags
    ntitles = []
    ncontents = []
    ntags = []
    for title, content, tag in zip(titles, contents, tags):
        tag_words = tag.split(' ')
        for word in tag_words:
            ntitles.append(title)
            ncontents.append(content)
            ntags.append(word)

    assert len(ntitles) == len(ntags)
    assert len(ncontents) == len(ntags)

    return ntitles, ncontents, ntags

def getPivotWords(fileName, common_words, k):
    ds = MemoryDataset.load(fileName)
    selector = MISelector()
    pivot_generator = selector.select(ds)
    pivot_words = []
    for word in pivot_generator:
        if not word in common_words:
            continue
        pivot_words.append(word)
        if len(pivot_words) >= k:
            break
    return pivot_words

def getWords_from_idx(src_vocabulary, pivot_words_idx):
    inv_map_ = {v: k for k, v in src_vocabulary.iteritems()}
    pivot_words = []
    for idx in pivot_words_idx:
        pivot_words.append(inv_map_[idx])

    return pivot_words

def get_common_words(src_vocabulary, tgt_vocabulary):
    common_words = []
    for word in tgt_vocabulary:
        if word in src_vocabulary:
            common_words.append(src_vocabulary[word])

    return common_words

if __name__ == '__main__':
    target_rawData = parseFile(ROOT_DIR + 'test_processed.csv')
    # use titles for now
    tgt_X, _, tgt_vocabulary, _ = countvectorize(target_rawData.title, None)
    for topic, fn in topic2FileNames.iteritems():
        print 'Processing topic: ', topic
        rawData = parseFile(ROOT_DIR + fn + '.csv')
        ntitles, ncontents, ntags = convert_multilabel_to_single_label(rawData)
        # use titles for now
        src_X, src_y, src_vocabulary, src_classes = countvectorize(ntitles, ntags)
        svmFileName = ROOT_DIR + fn + '.svm'
        vocFileName = ROOT_DIR + fn + '.vocb'
        classesFileName = ROOT_DIR + fn + '.labels'
        dump_data(src_X, src_y, src_vocabulary, src_classes, svmFileName, vocFileName, classesFileName)
        common_words_idx = get_common_words(src_vocabulary, tgt_vocabulary)
        common_words = getWords_from_idx(src_vocabulary, common_words_idx)
        print common_words
        pivot_words_idx = getPivotWords(svmFileName, common_words_idx, 2000)
        pivot_words = getWords_from_idx(src_vocabulary, pivot_words_idx)
        write_list_to_file(pivot_words, ROOT_DIR + fn + '.pivots')

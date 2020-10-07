""" File: corpusStreams.py
    Description:  The gensim LSA (Latent Semantic Analysis or Latent Semantic
    Indexing) and pLSA topic modeling modules allows for memory-efficient
    training via preprocessed document corpus to "vector-space model."

    This script preprocesses the document corpus (either whole-chats or
    questions-only) and produces:
    (1) corpus dictionary (.dict file), and
    (2) corpus bag-of-words vectorization stream (.mm file).

    Note: It is memory-efficient to represent the documents only by their (integer)
    ids. The mapping between the document words and ids is called a dictionary
    which is saves in a .dict file for later usage.

    Using the dictionary vectorize, the vectorized documents are saves in a
    .mm file for later usage.
    
"""

from pprint import pprint  # pretty-printer
from collections import defaultdict
from gensim import corpora
from six import iteritems


#Global Variables - select appropriate chat file based on preprocessing
FILE_NAME_OF_CORPUS = 'wholeChatsFilePOS_N_ADJ_V'
##FILE_NAME_OF_CORPUS = 'wholeChatsFilePOS_N_ADJ'
##FILE_NAME_OF_CORPUS = 'wholeChatsFile'  # NO POS preprocessing so all parts of speech
##FILE_NAME_OF_CORPUS = 'onlyQuestionsFile'  # Only initial question of chats


### Load stop words from file stop_words.txt
stopList = []
stopFile = open('stop_words.txt', 'r')
for line in stopFile:
    stopList.append(line.strip().lower())
stoplist = set(stopList)
print("number of stop words in stop_words.txt file", len(stoplist))

# Convert whole chats to vectors using a document representation called a
# bag-of-words.  Each chat is represented by one vector where each
# vector element represents a question-answer pair in the style of:
# "How many times does the word 'system' appear in the document? Once."

# It is advantageous to represent the chat words only by their (integer)
# ids. The mapping between the chat words and ids is called a dictionary.

##Here we assigned a unique integer id to all words appearing in the corpus with
##the gensim.corpora.dictionary.Dictionary class. This sweeps across the texts,
##collecting word counts and relevant statistics. 


# collect statistics about all tokens, i.e., words
dictionary = corpora.Dictionary(line.lower().split() for line in open(FILE_NAME_OF_CORPUS+'.txt'))
# remove stop words and words that appear only once
stop_ids = [
    dictionary.token2id[stopword]
    for stopword in stoplist
    if stopword in dictionary.token2id
]
once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
dictionary.compactify()  # remove gaps in id sequence after words that were removed

dictionary.save(FILE_NAME_OF_CORPUS+'.dict')  # store the dictionary, for future reference
print(dictionary)
##print(dictionary.token2id)

# create a vector stream to avoid loading the whole vector into memory at one time
class MyCorpus(object):
    def __iter__(self):
#        for line in open(FILE_NAME_OF_CORPUS+'_lemmatized.txt'):
        for line in open(FILE_NAME_OF_CORPUS+'.txt'):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split())

corpus_memory_friendly = MyCorpus()  # doesn't load the corpus into memory!

corpora.MmCorpus.serialize(FILE_NAME_OF_CORPUS+'.mm', corpus_memory_friendly)


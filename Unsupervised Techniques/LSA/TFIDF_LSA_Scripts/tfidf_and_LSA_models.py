""" File:  tfidf_and_LSA_models.py
    Description:  Loads the previously created chat corpus dictionary
    (.dict file) and chat corpus bag-of-words vectorization stream (.mm file).

    Performs a transformation from the bag-of-words vectorization to a
    tf-idf (term frequency-inverse document frequency) vectorization model, then
    it performs Latent Semantic Analysis (aka Latent Semantic Indexing) transformation.

    Asks for user input of the number of topics.  It is recommended between 200-500
    topics as the "golden standard." by Bradford. 2008. An empirical study of required
    dimensionality for large-scale latent semantic indexing applications.

    INPUT FILES:
    Previously created (by corpusStreams.py script) chat corpus dictionary
    (.dict file) and chat corpus bag-of-words vectorization stream (.mm file).
    In Global Variables section select:
    1) desired chat preprocessing file,
    2) NUMBER_OF_TOPICS_PRINTED
    3) NUMBER_OF_WORDS_PER_TOPICS

    OUTPUT FILES:
    1) "raw_" text (.txt) file listing topics with each word scored
    2) "TFIDF_LSA_" text (.txt) file containing only the text for the
       specified number of topics with the specified number of words per topic
    
"""

from pprint import pprint  # pretty-printer
from collections import defaultdict
from gensim import corpora
from gensim import models

#Global Variables - select appropriate chat file based on preprocessing
FILE_NAME_OF_CORPUS = 'wholeChatsFilePOS_N_ADJ_V'
##FILE_NAME_OF_CORPUS = 'wholeChatsFilePOS_N_ADJ'
##FILE_NAME_OF_CORPUS = 'wholeChatsFile'  # NO POS preprocessing so all parts of speech
##FILE_NAME_OF_CORPUS = 'onlyQuestionsFile'  # Only initial question of chats

NUMBER_OF_TOPICS_PRINTED = 15
NUMBER_OF_WORDS_PER_TOPICS = 8
##NUMBER_OF_WORDS_PER_TOPICS = 5
##NUMBER_OF_WORDS_PER_TOPICS = 10

import nltk
# NOTE: uncomment below to pop up download tool
# nltk.download()

from nltk.corpus import stopwords

from gensim import corpora
from six import iteritems
import gensim

dictionary = gensim.utils.SaveLoad.load(FILE_NAME_OF_CORPUS+'.dict')

print(dictionary)
##print(dictionary.token2id)

corpus = corpora.MmCorpus(FILE_NAME_OF_CORPUS+'.mm')
##print(corpus)
'''
MmCorpus(9146 documents, 4255 features, 76350 non-zero entries)
'''
# create transformation
'''
Here I transform documents from the bag-of-words vector representation into
the TF-Idf vector model. This process serves two goals:

1) To bring out hidden structure in the corpus, discover relationships between
words and use them to describe the documents in a new and (hopefully) more
semantic way.

2) To make the document representation more compact. This both improves efficiency
(new representation consumes less resources) and efficacy (marginal data trends
are ignored, noise-reduction).

The transformations are standard Python objects, typically initialized by
means of a training corpus:
'''
tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model

# Apply a transformation to a whole corpus and write out the tf-idf text file:
corpus_tfidf = tfidf[corpus]

'''
Documents:
hello can you help me find a call number for a book
can you help me find books about threats to siberian tigers
hi could you help explain to me how to find books on the library website
'''
# Initialize an LSI transformation
numberOfTopics = int(input("How many topics for LSA would you like (recommended between 200-500): "))
lsi = models.LsiModel(corpus_tfidf, id2word = dictionary, num_topics=numberOfTopics)
# create a double wrapper over chat corpus: bow -> tfidf -> fold-in-lsi
corpus_lsi = lsi[corpus_tfidf]

topicList = lsi.print_topics(NUMBER_OF_TOPICS_PRINTED)
corpus_tfidf_and_lsa_fileName = "raw_" +FILE_NAME_OF_CORPUS+'_tfidf_and_lsa.txt'
outputFileName = "TFIDF_LSA_"+FILE_NAME_OF_CORPUS+"_"+str(NUMBER_OF_TOPICS_PRINTED)+ \
                 "topics_"+str(NUMBER_OF_WORDS_PER_TOPICS)+"words.txt"
corpus_tfidf_and_lsa_file = open(corpus_tfidf_and_lsa_fileName, 'w')
outputFile = open(outputFileName,'w')
corpus_tfidf_and_lsa_file.write("File: " + corpus_tfidf_and_lsa_fileName + '\n\n')
outputFile.write("File: " + outputFileName + '\n\n')
for topicIndex in range(NUMBER_OF_TOPICS_PRINTED):
    corpus_tfidf_and_lsa_file.write(str(topicList[topicIndex])+'\n')
    line = str(topicList[topicIndex])
    topicString = ""
    startIndex = 0
    for count in range(NUMBER_OF_WORDS_PER_TOPICS):
        wordStart = line.find('*"', startIndex) + 2
        wordEnd = line.find('"', wordStart) - 1
        topicString += line[wordStart:wordEnd+1] + " "
        startIndex = wordEnd + 1
    outputFile.write(topicString+"\n")

outputFile.close()
corpus_tfidf_and_lsa_file.close()
print("Topics written to file:",outputFileName)


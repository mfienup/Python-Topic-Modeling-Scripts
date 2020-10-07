""" File:  GuidedLDA.py  

    Description:  Loads a previously created preprocessed chat corpus, then performs
    topic modeling utilizing GuidedLDA model.

    Here we are used the GuidedLDA package is available at GitHub:
    https://github.com/vi3k6i5/GuidedLDA
    NOTE:  We had difficulty installing GuidedLDA, but we were finally successful
    by following the work-around posted at:
    https://github.com/dex314/GuidedLDA_WorkAround

    INPUT FILES:
    Previously created preprocessed chat corpus from either:
    1) wholeChatsFilePOS_N_ADJ_V.csv -- preprocessing keeping nouns, adjectives, and verbs
    2) wholeChatsFilePOS_N_ADJ.csv -- preprocessing keeping nouns and adjectives
    3) wholeChatsFile.csv -- NO POS preprocessing so all parts of speech
    4) onlyQuestionsFile.csv -- Only initial question of chats

    OUTPUT FILES:
    1) "GuidedLDA_" text (.txt) file listing topics GuidedLDA found
    with seeds specified and confidence specified

"""

import re, sys, random, math
import numpy as np
from lda import guidedlda as glda
from lda import glda_datasets as gldad

from collections import Counter
from timeit import default_timer as timer

from time import time

#Global Variables - select appropriate chat file based on preprocessing
##FILE_NAME_OF_CORPUS = 'wholeChatsFilePOS_N_ADJ_V'
FILE_NAME_OF_CORPUS = 'wholeChatsFilePOS_N_ADJ'
##FILE_NAME_OF_CORPUS = 'wholeChatsFile'  # NO POS preprocessing so all parts of speech
##FILE_NAME_OF_CORPUS = 'onlyQuestionsFile'  # Only initial question of chats

NUMBER_OF_TOPICS_PRINTED = 15

NUMBER_OF_WORDS_PER_TOPICS = 8
##NUMBER_OF_WORDS_PER_TOPICS = 5
##NUMBER_OF_WORDS_PER_TOPICS = 10

##SEED_CONFIDENCE = 0.0
##SEED_CONFIDENCE = 0.25
##SEED_CONFIDENCE = 0.50
SEED_CONFIDENCE = 0.75
##SEED_CONFIDENCE = 1.0


### Load stop words from file stop_words.txt
stopList = []
stopFile = open('stop_words.txt', 'r')
for line in stopFile:
    stopList.append(line.strip().lower())
stoplist = set(stopList)
print("number of stop words in stop_words.txt file", len(stoplist))

### Load selected preprocessed chat documents
documentsFile = open(FILE_NAME_OF_CORPUS+".csv", 'r')

docIndexToIndexInCSVDict = {}
docs = []
docIndex = 0
word2id = {}
id2word = {}
wordList = []
wordId = 0
for line in documentsFile:
    docLineSplit = line.split(",")
    documentLine = docLineSplit[1]
    newDoc = ""
    for word in documentLine.strip().split():
        if word not in stoplist:
            if word not in word2id:
                word2id[word] = wordId
                id2word[wordId] = word
                wordList.append(word)
                wordId += 1
            newDoc += word + " "
    if len(newDoc) > 0:
        docs.append(newDoc)
        #print(docLineSplit[0])
        docIndexToIndexInCSVDict[docIndex] = int(docLineSplit[0].strip())
        docIndex += 1
numDocs = len(docs)
numWords = len(word2id)
vocab = tuple(wordList)

X = np.ndarray(shape=(numDocs, numWords), dtype=int)

word_counts = Counter()

documents = []
word_topics = {}
topic_totals = np.zeros(NUMBER_OF_TOPICS_PRINTED)

for docIndex, docLine in enumerate(docs):
    
    for word in docLine.strip().split():
        wordId = word2id[word]
        X[docIndex][wordId] += 1

seed_topic_list = [['interlibrary', 'loan', 'request'],
                   ['hour', 'time', 'today'],
                   ['floor', 'librarian', 'research'],
                   ['camera', 'digital', 'hub'],
                   ['access', 'article', 'journal'],
                   ['access', 'article', 'database'],
                   ['access', 'account','campus'],
                   ['research', 'source', 'topic']]

model = glda.GuidedLDA(n_topics=NUMBER_OF_TOPICS_PRINTED, n_iter=100,
                       random_state=7, refresh=20)

seed_topics = {}
for t_id, st in enumerate(seed_topic_list):
    for word in st:
        seed_topics[word2id[word]] = t_id


model.fit(X, seed_topics=seed_topics, seed_confidence=SEED_CONFIDENCE)

print("\nSeeds",str(seed_topic_list),"\n")
print("\nTopics using seeds with confidence",SEED_CONFIDENCE,":")

# Display and write to file the results of CorEx with no anchors
fileName = "GuidedLDA_seeds_"+str(len(seed_topic_list))+"_confidence_"+ \
           str(SEED_CONFIDENCE)+"_"+FILE_NAME_OF_CORPUS+"_"+str(NUMBER_OF_TOPICS_PRINTED) \
           +"topoics_"+str(NUMBER_OF_WORDS_PER_TOPICS)+"words.txt"
outputFile = open(fileName, 'w')
outputFile.write("File: " + fileName +"\n\n")

topic_word = model.topic_word_
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(NUMBER_OF_WORDS_PER_TOPICS+1):-1]
##    print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    topicStr = '{}'.format(' '.join(topic_words))
    print(topicStr)
    outputFile.write(topicStr+"\n")
outputFile.close()

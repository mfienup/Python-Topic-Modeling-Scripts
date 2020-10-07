""" File:  PyMallet_LDA.py

    Description:  Loads a previously created preprocessed chat corpus, then performs
    topic modeling utilizing LDA (Latent Dirichlet Allocation).

    Here we are used the LDA implementation from GitHub PyMallet at:
    https://github.com/mimno/PyMallet
    The LDA code below is based on their lda_reference.py code written in Python
    The PyMallet project has an MIT License see below.

    INPUT FILES:
    Previously created preprocessed chat corpus from either:
    1) wholeChatsFilePOS_N_ADJ_V.csv -- preprocessing keeping nouns, adjectives, and verbs
    2) wholeChatsFilePOS_N_ADJ.csv -- preprocessing keeping nouns and adjectives
    3) wholeChatsFile.csv -- NO POS preprocessing so all parts of speech
    4) onlyQuestionsFile.csv -- Only initial question of chats

    OUTPUT FILES:
    1) "raw_" text (.txt) file listing topics with each word scored
    2) "PyMallet_LDA_" text (.txt) file containing only the text for the
       specified number of topics with the specified number of words per topic

MIT License

Copyright (c) 2019 mimno

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
##from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
##from corextopic import corextopic as ct
##import pandas as pd
##import nltk

import re, sys, random, math
import numpy as np
from collections import Counter
from timeit import default_timer as timer

from time import time

#Global Variables - select appropriate chat file based on preprocessing
##FILE_NAME_OF_CORPUS = 'wholeChatsFilePOS_N_ADJ_V'
##FILE_NAME_OF_CORPUS = 'wholeChatsFilePOS_N_ADJ'
FILE_NAME_OF_CORPUS = 'wholeChatsFile'  # NO POS preprocessing so all parts of speech
##FILE_NAME_OF_CORPUS = 'onlyQuestionsFile'  # Only initial question of chats

NUMBER_OF_TOPICS_PRINTED = 15
NUMBER_OF_WORDS_PER_TOPICS = 8
##NUMBER_OF_WORDS_PER_TOPICS = 5
##NUMBER_OF_WORDS_PER_TOPICS = 10

doc_smoothing = 0.5
word_smoothing = 0.01


word_pattern = re.compile("\w[\w\-\']*\w|\w")


def sample(num_iterations):
    for iteration in range(num_iterations):
        
        start = timer()
        
        for document in documents:
            
            doc_topic_counts = document["topic_counts"]
            token_topics = document["token_topics"]
            doc_length = len(token_topics)
            for token_topic in token_topics:
                
                w = token_topic["word"]
                old_topic = token_topic["topic"]
                word_topic_counts = word_topics[w]
                
                ## erase the effect of this token
                word_topic_counts[old_topic] -= 1
                topic_totals[old_topic] -= 1
                doc_topic_counts[old_topic] -= 1
                
                ###
                ### SAMPLING DISTRIBUTION
                ###
                
                ## Does this topic occur often in the document?
                topic_probs = (doc_topic_counts + doc_smoothing) / (doc_length + NUMBER_OF_TOPICS_PRINTED * doc_smoothing)
                ## Does this word occur often in the topic?
                topic_probs *= (word_topic_counts + word_smoothing) / (topic_totals + smoothing_times_vocab_size)
                
                ## sample from an array that doesn't sum to 1.0
                sample = random.uniform(0, np.sum(topic_probs))
                
                new_topic = 0
                while sample > topic_probs[new_topic]:
                    sample -= topic_probs[new_topic]
                    new_topic += 1
                
                ## add back in the effect of this token
                word_topic_counts[new_topic] += 1
                topic_totals[new_topic] += 1
                doc_topic_counts[new_topic] += 1
                
                token_topic["topic"] = new_topic
        end = timer()
        print(end - start)
                

def entropy(p):
    ## make sure the vector is a valid probability distribution
    p = p / np.sum(p)
    
    result = 0.0
    for x in p:
        if x > 0.0:
            result += -x * math.log2(x)
            
    return result

def print_topic(topic):
    sorted_words = sorted(vocabulary, key=lambda w: word_topics[w][topic], reverse=True)
    
    for i in range(20):
        w = sorted_words[i]
        print("{}\t{}".format(word_topics[w][topic], w))

def print_all_topics():
    for topic in range(NUMBER_OF_TOPICS_PRINTED):
        sorted_words = sorted(vocabulary, key=lambda w: word_topics[w][topic], reverse=True)
        print(" ".join(sorted_words[:20]))

### Load stop words from file stop_words.txt
stopList = []
stopFile = open('stop_words.txt', 'r')
for line in stopFile:
    stopList.append(line.strip().lower())
stoplist = set(stopList)
print("number of stop words in stop_words.txt file", len(stoplist))

documentsFile = open(FILE_NAME_OF_CORPUS+".csv", 'r')

docIndexToIndexInCSVDict = {}
docs = []
docIndex = 0
for line in documentsFile:
    docLineSplit = line.split(",")
    documentLine = docLineSplit[1]
    newDoc = ""
    for word in documentLine.strip().split():
        if word not in stoplist:
            newDoc += word + " "
    if len(newDoc) > 0:
        docs.append(newDoc)
        docIndexToIndexInCSVDict[docIndex] = int(docLineSplit[0].strip())
        docIndex += 1
n_samples = len(docs)
print("len(docs)",len(docs))

word_counts = Counter()

documents = []
word_topics = {}
topic_totals = np.zeros(NUMBER_OF_TOPICS_PRINTED)


for line in docs:
    #line = line.lower()
    
    tokens = word_pattern.findall(line)
    
    ## remove stopwords, short words, and upper-cased words
    tokens = [w for w in tokens if not w in stoplist and len(w) >= 3 and not w[0].isupper()]
    word_counts.update(tokens)
    
    doc_topic_counts = np.zeros(NUMBER_OF_TOPICS_PRINTED)
    token_topics = []
    
    for w in tokens:
        
        ## Generate a topic randomly
        topic = random.randrange(NUMBER_OF_TOPICS_PRINTED)
        token_topics.append({ "word": w, "topic": topic })
        
        ## If we haven't seen this word before, initialize it
        if not w in word_topics:
            word_topics[w] = np.zeros(NUMBER_OF_TOPICS_PRINTED)
        
        ## Update counts: 
        word_topics[w][topic] += 1
        topic_totals[topic] += 1
        doc_topic_counts[topic] += 1
    
    documents.append({ "original": line, "token_topics": token_topics, "topic_counts": doc_topic_counts })

## Now that we're done reading from disk, we can count the total
##  number of words.
vocabulary = list(word_counts.keys())
vocabulary_size = len(vocabulary)

smoothing_times_vocab_size = word_smoothing * vocabulary_size


sample(100)
fileName = "PyMallet_LDA_"+FILE_NAME_OF_CORPUS+"_"+str(NUMBER_OF_TOPICS_PRINTED) \
           +"topoics_"+str(NUMBER_OF_WORDS_PER_TOPICS)+"words.txt"
outputFile = open(fileName, 'w')
outputFile.write("File: " + fileName +"\n\n")
rawFileName = "raw_PyMallet_LDA_"+FILE_NAME_OF_CORPUS+"_"+str(NUMBER_OF_TOPICS_PRINTED) \
           +"topoics_"+str(NUMBER_OF_WORDS_PER_TOPICS)+"words.txt"
outputFileRaw = open(rawFileName, 'w')
outputFileRaw.write("File: " + rawFileName +"\n\n")

for topic in range(NUMBER_OF_TOPICS_PRINTED):
    sorted_words = sorted(vocabulary, key=lambda w: word_topics[w][topic], reverse=True)
    topicStr = " ".join(sorted_words[:NUMBER_OF_WORDS_PER_TOPICS])
    outputFile.write(topicStr+"\n")
    outputFileRaw.write(topicStr+"\n")
    print(topicStr)
    for i in range(NUMBER_OF_WORDS_PER_TOPICS):
        w = sorted_words[i]
        print("{}\t{}".format(word_topics[w][topic], w))
        outputFileRaw.write("{}\t{}".format(word_topics[w][topic], w) +"\n")
    
outputFile.close()
outputFileRaw.close()

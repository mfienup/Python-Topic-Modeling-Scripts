""" File:  CorEx.py  

    Description:  Loads a previously created preprocessed chat corpus, then performs
    topic modeling utilizing CorEx (Correlation Explanation) model.

    Here we are used the CorEx package available at GitHub:
    https://github.com/gregversteeg/corex_topic


    INPUT FILES:
    Previously created preprocessed chat corpus from either:
    1) wholeChatsFilePOS_N_ADJ_V.csv -- preprocessing keeping nouns, adjectives, and verbs
    2) wholeChatsFilePOS_N_ADJ.csv -- preprocessing keeping nouns and adjectives
    3) wholeChatsFile.csv -- NO POS preprocessing so all parts of speech
    4) onlyQuestionsFile.csv -- Only initial question of chats

    OUTPUT FILES:
    1) "CorEx_no_anchors_" text (.txt) file listing topics CorEx found with no anchors specified
    2) "CorEx_anchors_" text (.txt) file listing topics CorEx found with anchors specified

"""
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from corextopic import corextopic as ct
import pandas as pd
import nltk

from time import time

#Global Variables - select appropriate chat file based on preprocessing
##FILE_NAME_OF_CORPUS = 'wholeChatsFilePOS_N_ADJ_V'
FILE_NAME_OF_CORPUS = 'wholeChatsFilePOS_N_ADJ'
##FILE_NAME_OF_CORPUS = 'wholeChatsFile'  # NO POS preprocessing so all parts of speech
##FILE_NAME_OF_CORPUS = 'onlyQuestionsFile'  # Only initial question of chats

NUMBER_OF_TOPICS_PRINTED = 15
##NUMBER_OF_WORDS_PER_TOPICS = 8
NUMBER_OF_WORDS_PER_TOPICS = 5
##NUMBER_OF_WORDS_PER_TOPICS = 10

### Load stop words from file stop_words.txt
stopList = []
stopFile = open('stop_words.txt', 'r')
for line in stopFile:
    stopList.append(line.strip().lower())
stoplist = set(stopList)
print("number of stop words in stop_words.txt file", len(stoplist))

### Load selected preprocessed chat documents
documentsFile = open(FILE_NAME_OF_CORPUS + ".csv", 'r')

docIndexToIndexInCSVDict = {}
documents = []
docIndex = 0
for line in documentsFile:
    docLineSplit = line.split(",")
    documentLine = docLineSplit[1]
    newDoc = ""
    for word in documentLine.strip().split():
        if word not in stoplist:
            newDoc += word + " "
    if len(newDoc) > 0:
        documents.append(newDoc)
        #print(docLineSplit[0])
        docIndexToIndexInCSVDict[docIndex] = int(docLineSplit[0].strip())
        docIndex += 1
n_samples = len(documents)
print("len(documents)",len(documents))

# CorEx uses an TF-IDF vectorization
vectorizer = TfidfVectorizer(
    max_df=.5,
    min_df=10,
    max_features=None,
##    ngram_range=(1, 2),  for bi-grams
##    ngram_range=(1,3),   for bi-grams and tri-grams
    ngram_range=(1,1),     # for no bi-grams or tri-grams
    norm=None,
    binary=True,
    use_idf=False,
    sublinear_tf=False
)

# Fit chat corpus to TF-IDF vectorization
vectorizer = vectorizer.fit(documents)
tfidf = vectorizer.transform(documents)
vocab = vectorizer.get_feature_names()
print("len(vocab)",len(vocab))

# Apply CorEx with no anchors for a comparison
anchors = []
model = ct.Corex(n_hidden=NUMBER_OF_TOPICS_PRINTED, seed=42) # n_hidden specifies the # of topics
model = model.fit(tfidf, words=vocab)

# Display and write to file the results of CorEx with no anchors
fileName = "CorEx_no_anchors_"+FILE_NAME_OF_CORPUS+"_"+str(NUMBER_OF_TOPICS_PRINTED) \
           +"topoics_"+str(NUMBER_OF_WORDS_PER_TOPICS)+"words.txt"
outputFile = open(fileName, 'w')
outputFile.write("File: " + fileName +"\n\n")

print("\nCorEx Topics with no anchors:")
for i, topic_ngrams in enumerate(model.get_topics(n_words=NUMBER_OF_WORDS_PER_TOPICS)):
    topic_ngrams = [ngram[0] for ngram in topic_ngrams if ngram[1] > 0]
    print("Topic #{}: {}".format(i+1, ", ".join(topic_ngrams)))
    outputFile.write("{}".format(" ".join(topic_ngrams))+"\n")
outputFile.close()

# Anchors designed to nudge the model towards
## 8 anchors without bi-grams
anchors = [['interlibrary', 'loan', 'request'],
                   ['hour', 'time', 'today'],
                   ['floor', 'librarian', 'research'],
                   ['camera', 'digital', 'hub'],
                   ['access', 'article', 'journal'],
                   ['access', 'article', 'database'],
                   ['access', 'account','campus'],
                   ['research', 'source', 'topic']]

## remove anchor words that are not in the chat corpus
anchors = [
    [a for a in topic if a in vocab]
    for topic in anchors
]

model = ct.Corex(n_hidden=NUMBER_OF_TOPICS_PRINTED, seed=42)
model = model.fit(
    tfidf,
    words=vocab,
    anchors=anchors, # Pass the anchors in here
    anchor_strength=3 # Tell the model how much it should rely on the anchors
)
print("\nAnchors",str(anchors),"\n")
print("\nTopics after anchors:")

# Display and write to file the results of CorEx with no anchors
fileName = "CorEx_anchors_"+str(len(anchors))+"_"+FILE_NAME_OF_CORPUS+"_"+str(NUMBER_OF_TOPICS_PRINTED) \
           +"topoics_"+str(NUMBER_OF_WORDS_PER_TOPICS)+"words.txt"
outputFile = open(fileName, 'w')
outputFile.write("File: " + fileName +"\n\n")

print("\nCorEx Topics with anchors:")
for i, topic_ngrams in enumerate(model.get_topics(n_words=NUMBER_OF_WORDS_PER_TOPICS)):
    topic_ngrams = [ngram[0] for ngram in topic_ngrams if ngram[1] > 0]
    print("Topic #{}: {}".format(i+1, ", ".join(topic_ngrams)))
    outputFile.write("{}".format(" ".join(topic_ngrams))+"\n")
outputFile.close()

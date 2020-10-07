""" File:  LDA_model.py  

    Description:  Loads a previously created preprocessed chat corpus, then performs
    topic modeling utilizing LDA (Latent Dirichlet Allocation).

    We used the scikit-learn.org (sklearn) LDA module.

    INPUT FILES:
    Previously created preprocessed chat corpus from either:
    1) wholeChatsFilePOS_N_ADJ_V.csv -- preprocessing keeping nouns, adjectives, and verbs
    2) wholeChatsFilePOS_N_ADJ.csv -- preprocessing keeping nouns and adjectives
    3) wholeChatsFile.csv -- NO POS preprocessing so all parts of speech
    4) onlyQuestionsFile.csv -- Only initial question of chats

    OUTPUT FILES:
    1) "raw_" text (.txt) file listing topics with each word scored
    2) "LDA_" text (.txt) file containing only the text for the
       specified number of topics with the specified number of words per topic
"""
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
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

N_FEATURES = 1000

def print_top_words(model, feature_names, n_top_words):
    """ Displays the specified top topics and top words to screen"""
    for topic_idx, topic in enumerate(model.components_):
        
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        message += "\n "
        message += " ".join([feature_names[i]+" ("+str(model.components_[topic_idx][i])+")\n"
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

def write_file_top_words(model, feature_names, n_top_words, fileName):
    outputFile = open("raw_"+fileName, 'w')
    outputFileTopics = open(fileName, 'w')
    outputFile.write("File: "+"raw_"+fileName+"\n\n")
    outputFileTopics.write("File: "+fileName+"\n\n")
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        topicStr = " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        outputFileTopics.write(topicStr+"\n")

        message += topicStr + "\n "
        message += " ".join([feature_names[i]+" ("+str(model.components_[topic_idx][i])+")\n"
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        outputFile.write(message+"\n")

    outputFile.close()
    outputFileTopics.close()

### Read stop words from file stop_words.txt
stopList = []
stopFile = open('stop_words.txt', 'r')
for line in stopFile:
    stopList.append(line.strip().lower())
stoplist = set(stopList)
print("number of stop words in stop_words.txt file", len(stoplist))

## Read specified chat corpus
documentsFile = open(FILE_NAME_OF_CORPUS+".csv", 'r')

docIndexToIndexInCSVDict = {}
documents = []
docCSVLines = []
docIndex = 0
for line in documentsFile:
    docLineSplit = line.split(",")
    docCSVLine = int(docLineSplit[0])
    documentLine = docLineSplit[1]
    newDoc = ""
    for word in documentLine.strip().split():
        if word not in stoplist:
            newDoc += word + " "
    if len(newDoc) > 0:
        documents.append(newDoc)
        docCSVLines.append(docCSVLine)
        #print(docLineSplit[0])
        docIndexToIndexInCSVDict[docIndex] = int(docLineSplit[0].strip())
        docIndex += 1
N_SAMPLES = len(documents)
print("N_SAMPLES",N_SAMPLES, "len(docIndexToIndexInCSVDict)",len(docIndexToIndexInCSVDict))

# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=N_FEATURES, stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()

#no_topics = 15

# Fit the LDA model
print("Fitting the LDA model",
      "no_topics=%d and n_features=%d..."
      % (NUMBER_OF_TOPICS_PRINTED, N_FEATURES))
t0 = time()
lda_model = LatentDirichletAllocation(NUMBER_OF_TOPICS_PRINTED, max_iter=50, learning_method='online',
                                learning_decay = 0.7,
                                learning_offset=50.,
                                random_state=0)
lda_fit = lda_model.fit(tf)
lda_output = lda_model.transform(tf)

topicsnames = ["Topic"+str(i) for i in range(NUMBER_OF_TOPICS_PRINTED)]

docnames = ["Doc" + str(docCSVLines[i]) for i in range(len(documents))]

df_document_topic = pd.DataFrame(np.round(lda_output,2),columns=topicsnames, index= docnames)
dominant_topic = np.argmax(df_document_topic.values, axis=1)
df_document_topic['dominant_topic'] = dominant_topic

print(df_document_topic.head(NUMBER_OF_TOPICS_PRINTED))
print("lda_output:\n",lda_output)
print("LDA done in %0.3fs." % (time() - t0))

# Print topics to screen and write topics to files
print("\nTopics in LDA model:")
fileName = "LDA_"+FILE_NAME_OF_CORPUS+"_"+str(NUMBER_OF_TOPICS_PRINTED) \
           +"topoics_"+str(NUMBER_OF_WORDS_PER_TOPICS)+"words.txt"

print_top_words(lda_fit, tf_feature_names, NUMBER_OF_WORDS_PER_TOPICS)
write_file_top_words(lda_fit, tf_feature_names, NUMBER_OF_WORDS_PER_TOPICS, fileName)


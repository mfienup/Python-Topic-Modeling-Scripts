""" File:  tfidf_and_pLSA_models.py

    Description:  Loads a previously created preprocessed chat corpus, then performs
    topic modeling by first utilizing a tf-idf (term frequency-inverse document frequency)
    vectorization model, then utilizing pLSA (Probabilistic Latent Semantic Analysis).
    Two variations of pLSA were performed:
    the NMF model (Frobenius norm) and NMF model (generalized Kullback-Leibler divergence).

    We used the scikit-learn.org (sklearn) pLDA module since gensim does not seem to
    support pLDA modeling. (Note:  I'm not a fan of the scikit-learn documentation and examples!)

    Performs a transformation from the bag-of-words vectorization to a
    tf-idf (term frequency-inverse document frequency) vectorization model, then
    it performs Probabilistic Latent Semantic Analysis transformation to determine the top topics
    from the chat data.

    INPUT FILES:
    Previously created preprocessed chat corpus from either:
    1) wholeChatsFilePOS_N_ADJ_V.csv -- preprocessing keeping nouns, adjectives, and verbs
    2) wholeChatsFilePOS_N_ADJ.csv -- preprocessing keeping nouns and adjectives
    3) wholeChatsFile.csv -- NO POS preprocessing so all parts of speech
    4) onlyQuestionsFile.csv == Only initial question of chats

    OUTPUT FILES:
    1) "raw_" text (.txt) file listing topics with each word scored
    2) "TFIDF_pLSA_" text (.txt) file containing only the text for the
       specified number of topics with the specified number of words per topic

Acknowledgements:  Adaptted from the example at:
https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html
Original code by
Authors: Olivier Grisel <olivier.grisel@ensta.org>, Lars Buitinck, Chyi-Kwei Yau <chyikwei.yau@gmail.com>
"""

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
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
    """ Writes the specified top topics and top words to screen"""
    outputFile = open("raw_"+fileName, 'w')
    outputFileTopics = open(fileName, 'w')
    outputFile.write("File: "+"raw_"+fileName+"\n\n")
    outputFileTopics.write("File: "+fileName+"\n\n")
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        topicStr = " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        outputFileTopics.write(topicStr+"\n")
        message += topicStr
        message += "\n "
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
N_SAMPLES = len(documents)
print("N_SAMPLES",N_SAMPLES, "len(docIndexToIndexInCSVDict)",len(docIndexToIndexInCSVDict))

# Vectorize raw documents to tf-idf matrix: 
tfidf_vectorizer = TfidfVectorizer(stop_words='english',
                                   use_idf=True,
                                   smooth_idf=True)
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(documents)
print("fit_transform done in %0.3fs." % (time() - t0))

# Fit the NMF pLSA model (Frobenius norm)
print("Fitting the NMF model (Frobenius norm) with tf-idf features, "
      "N_SAMPLES=%d and N_FEATURES=%d..."
      % (N_SAMPLES, N_FEATURES))
t0 = time()
nmf = NMF(n_components=NUMBER_OF_TOPICS_PRINTED, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

# Print topics to screen and write topics to files
print("\nTopics in NMF model (Frobenius norm):")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, NUMBER_OF_WORDS_PER_TOPICS)
fileName = "TFIDF_pLSA_"+FILE_NAME_OF_CORPUS+"_NMF-model_FrobeniusNorm_" \
           +str(NUMBER_OF_TOPICS_PRINTED)+"topoics_"+str(NUMBER_OF_WORDS_PER_TOPICS)+"words.txt"
write_file_top_words(nmf, tfidf_feature_names, NUMBER_OF_WORDS_PER_TOPICS,fileName)

# Fit the NMF model (Kullback-Leibler)
print("Fitting the NMF model (generalized Kullback-Leibler divergence) with "
      "tf-idf features, N_SAMPLES=%d and N_FEATURES=%d..."
      % (N_SAMPLES, N_FEATURES))
t0 = time()
nmf = NMF(n_components=NUMBER_OF_TOPICS_PRINTED, random_state=1,
          beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
          l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

# Print topics to screen and write topics to files
print("\nTopics in NMF model (generalized Kullback-Leibler divergence):")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, NUMBER_OF_WORDS_PER_TOPICS)
fileName = "TFIDF_pLSA_"+FILE_NAME_OF_CORPUS+"_NMF-model_Kullbac-Leibler_" \
           +str(NUMBER_OF_TOPICS_PRINTED)+"topoics_"+str(NUMBER_OF_WORDS_PER_TOPICS)+"words.txt"
write_file_top_words(nmf, tfidf_feature_names, NUMBER_OF_WORDS_PER_TOPICS,fileName)


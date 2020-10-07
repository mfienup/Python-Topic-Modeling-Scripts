
This topic-modeling study utilized chat data (.csv) collected 
from the LibChat module of UNI's Rod library SpringShare platform 
between 4/10/2015 and 5/31/2019.  

This directory Preprocessing_Scripts contains subdirectories for various preprocessing techiques
that were applied to the raw chat data throughout the project.  In general 
all variations "cleaned" the raw chat data by: 
1) removing timestamps, 
2) removing chat patron and librarian identifiers, 
3) removing http tags (e.g., URLs), 
4) removing non-ASCII characters,
5) removing stopwords, and 
6) lemmatized words using nltk.WordNetLemmatizer() 

The subdirectories for the various preprocessing techiques:

preprocessing_wholeChats - whole chats kept (after using only above 6 "cleaning" steps)

preprocessing_onlyQuestions - only initial questions asked by the chat patrons were kept

preprocessing_wholeChats_POS_N_ADJ - whole chats were analyzed for Parts-Of_Speech (POS) with
only nouns and adjectives kept

preprocessing_wholeChats_POS_N_ADJ_V - whole chats were analyzed for Parts-Of_Speech (POS) with
only nouns, adjectives, and verbs kept
This directory contains the scripts and data/output files where chats are analyzed to extract 
only the initial question of each chat. The original chat data (.csv) from the LibChat 
module of UNI's library SpringShare platform contained a "Initial Question" column which was not 
enabled until 11/1/2018 and then only sporadically used by chat patrons.  If the Initial Question
column of a chat was not used, then the chat text was analyzed to extract the initial question.

Additionally the question text is "cleaned" by: 
1) removing timestamps, 
2) removing chat patron and librarian identifiers, 
3) removing http tags (e.g., URLs), 
4) removing non-ASCII characters,
5) removing stopwords, and 
6) lemmatized words using nltk.WordNetLemmatizer() 

The scripts and data/output files are:

processChatCSV_onlyQuestions.py - script to read chat data .csv file and writes 
the processed chat's initial question to two text files:
1) a (.csv) with one chat per line formatted as:  chat line # in original .csv, initial question of chat, and
2) a (.txt) with only the text of a chat one per line

INPUT Files:  
1) original_without_identifiable_info_chat_transcripts_9942_041015_053119.csv
2) stop_words.txt - file containing stop words

OUTPUT Files: onlyQuestionsFile.csv and onlyQuestionsFile.txt
1) onlyQuestionsFile.csv with one chat per line formatted as:
   chat line # in original .csv, initial question of chat, and
2) onlyQuestionsFile.txt with only the processed initial question of each chat one per line

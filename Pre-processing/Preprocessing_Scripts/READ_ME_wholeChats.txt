This directory contains the scripts and data/output files where whole chats are analyzed to "clean" the text by: 
1) removing timestamps, 
2) removing chat patron and librarian identifiers, 
3) removing http tags (e.g., URLs), 
4) removing non-ASCII characters,
5) removing stopwords, and 
6) lemmatized words using nltk.WordNetLemmatizer() 

The scripts and data/output files are:

processChatCSV_wholeChats.py - script to read chat data .csv file and writes 
the processed chat to two text files:
1) a (.csv) with one chat per line formatted as:  chat line # in original .csv, whole chat, and
2) a (.txt) with only the text of a chat one per line

INPUT Files:  
1) original_without_identifiable_info_chat_transcripts_9942_041015_053119.csv
2) stop_words.txt - file containing stop words

OUTPUT Files: wholeChatsFile.csv and wholeChatsFile.txt
1) wholeChatsFile.csv with one chat per line formatted as:
   chat line # in original .csv, whole chat, and
2) wholeChatsFile.txt with only the processed text of each chat one per line


 
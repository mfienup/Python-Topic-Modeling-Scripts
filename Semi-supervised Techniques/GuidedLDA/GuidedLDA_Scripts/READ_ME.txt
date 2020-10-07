This directory contains the scripts and necessary data files to
analyze chat corpus by performs topic modeling utilizing GuidedLDA

Here we are used the GuidedLDA package is available at GitHub:
https://github.com/vi3k6i5/GuidedLDA
NOTE:  We had difficulty installing GuidedLDA, but we were finally successful
by following the work-around posted at:
https://github.com/dex314/GuidedLDA_WorkAround

The files are:

1) GuidedLDA.py - contains the script to analyze chat corpus by performs 
topic modeling utilizing GuidedLDA 

2) INPUT (.csv) FILES - previously created preprocessed chat corpus from either:
wholeChatsFilePOS_N_ADJ_V.csv -- preprocessing keeping nouns, adjectives, and verbs
wholeChatsFilePOS_N_ADJ.csv -- preprocessing keeping nouns and adjectives
wholeChatsFile.csv -- NO POS preprocessing so all parts of speech
onlyQuestionsFile.csv -- Only initial question of chats
 

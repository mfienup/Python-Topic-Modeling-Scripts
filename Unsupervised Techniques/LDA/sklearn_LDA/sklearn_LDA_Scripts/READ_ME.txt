This directory contains the scripts and necessary data files to
analyze chat corpus by performs topic modeling utilizing LDA 
(Latent Dirichlet Allocation).

Note: We used the scikit-learn.org (sklearn) LDA module.

The files are:

1) LDA_models.py - contains the script to analyze chat corpus by performs 
topic modeling utilizing LDA

2) INPUT (.csv) FILES - previously created preprocessed chat corpus from either:
wholeChatsFilePOS_N_ADJ_V.csv -- preprocessing keeping nouns, adjectives, and verbs
wholeChatsFilePOS_N_ADJ.csv -- preprocessing keeping nouns and adjectives
wholeChatsFile.csv -- NO POS preprocessing so all parts of speech
onlyQuestionsFile.csv -- Only initial question of chats
 

This directory contains the scripts and necessary data files to
analyze chat corpus by first vectorizing it and performing a TF-IDF 
(Term Frequency–Inverse Document Frequency) transformation, and 
finally performing a pLSA (Probabilistic Latent Semantic Analysis)
transformation.  Two variations of pLSA were performed:
1) the NMF model (Frobenius norm) and 
2) NMF model (generalized Kullback-Leibler divergence).


The files are:

1) TFIDF_pLSA_models.py - contains the script to analyze chat corpus by 
first vectorizing it and performing a TF-IDF transformation, and Finally 
performing a pLSA transformation.

2) INPUT (.csv) FILES - previously created preprocessed chat corpus from either:
wholeChatsFilePOS_N_ADJ_V.csv -- preprocessing keeping nouns, adjectives, and verbs
wholeChatsFilePOS_N_ADJ.csv -- preprocessing keeping nouns and adjectives
wholeChatsFile.csv -- NO POS preprocessing so all parts of speech
onlyQuestionsFile.csv -- Only initial question of chats
 

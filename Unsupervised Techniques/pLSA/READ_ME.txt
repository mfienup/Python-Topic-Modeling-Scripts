This directory contains the scripts, data files, and output files from
analyzing the chat corpus by first vectorizing it and performing a TF-IDF 
(Term Frequency–Inverse Document Frequency) transformation, and 
finally performing a pLSA (Probabilistic Latent Semantic Analysis)
transformation.  Two variations of pLSA were performed:
1) the NMF model (Frobenius norm) and 
2) NMF model (generalized Kullback-Leibler divergence).

The two subdirectories contain:
1) TFIDF_pLSA_Scripts - contains the scripts and necessary data files to
analyze chat corpus by first vectorizing it, performing a TF-IDF 
transformation, and Finally performing a pLSA transformation.

2) Output - topic files resulting from the TF-IDF and pLSA transformations.
Two types of text (.txt) files are included:
a) "raw_" text (.txt) file listing topics with each word scored
   (e.g., raw_TFIDF_pLSA_wholeChatsFile_NMF-model_FrobeniusNorm_15topoics_8words.txt)
b) "TFIDF_pLSA_" text (.txt) file containing only the text for the
   specified number of topics with the specified number of words 
   per topic (e.g., TFIDF_pLSA_wholeChatsFile_NMF-model_FrobeniusNorm_15topoics_8words.txt)




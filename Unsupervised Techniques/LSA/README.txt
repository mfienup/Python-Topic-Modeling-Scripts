This directory contains the scripts and necessary data files to
analyze chat corpus by first vectorizing it, performing a TF-IDF 
(Term Frequency–Inverse Document Frequency) transformation, and 
finally performing a LSA (Latent Semantic Analysis, or Latent 
Semantic Indexing) transformation.  

The other two subdirectories contain:

1) TFIDF_LSA_Scripts - contains the scripts and necessary data files to
analyze chat corpus by first vectorizing it, performing a TF-IDF 
transformation, and Finally performing a LSA transformation.

2) Output - topic files resulting from the TF-IDF and LSA transformations.
Two types of text (.txt) files are included:
a) "raw_" text (.txt) file listing topics with each word scored
   (e.g., raw_wholeChatsFile_tfidf_and_lsa.txt)
b) "TFIDF_LSA_" text (.txt) file containing only the text for the
   specified number of topics with the specified number of words 
   per topic (e.g., TFIDF_LSA_wholeChatsFile_15topics_8words.txt)

This directory contains the scripts and necessary data files to
analyze chat corpus by first vectorizing it, performing a TF-IDF 
(Term Frequency–Inverse Document Frequency) transformation, and 
finally performing a LSA (Latent Semantic Analysis, or Latent 
Semantic Indexing) transformation.  

Processing is split into two parts:

corpusStreams.py - script to preprocesses the document corpus (either 
whole-chats or questions-only) to its vectorized form, and then saves 
the results in files:
(1) corpus dictionary (.dict file), and
(2) corpus bag-of-words vectorization stream (.mm file), and (.mm.index file)

tfidf_and_LSA_models.py - script that reads the vectorized form these 
files and then performing a TF-IDF (Term Frequency–Inverse Document 
Frequency) transformation followed by a LSA (Latent Semantic Analysis, 
or Latent Semantic Indexing) transformation.

OUTPUT FILES:
1) "raw_" text (.txt) file listing topics with each word scored
   (e.g., raw_wholeChatsFile_tfidf_and_lsa.txt)
2) "TFIDF_LSA_" text (.txt) file containing only the text for the
   specified number of topics with the specified number of words 
   per topic (e.g., TFIDF_LSA_wholeChatsFile_15topics_8words.txt)

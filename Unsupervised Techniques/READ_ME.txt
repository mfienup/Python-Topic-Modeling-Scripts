This directory contains subdirectories each containing 
scripts, data files, and output files for analyzing the 
chat corpus by various unsupervised topic modeling techniques.

The subdirectories are:
1) LSA - analyzes chat corpus by first vectorizing it, performing a TF-IDF 
(Term Frequency–Inverse Document Frequency) transformation, and 
finally performing a LSA (Latent Semantic Analysis, or Latent 
Semantic Indexing) transformation using gensim module

2) pLSA - analyzes the chat corpus by first vectorizing it and performing a TF-IDF 
(Term Frequency–Inverse Document Frequency) transformation, and 
finally performing a pLSA (Probabilistic Latent Semantic Analysis)
transformation using the scikit-learn.org (sklearn) pLDA module.  
Two variations of pLSA were performed:
a) the NMF model (Frobenius norm) and 
b) NMF model (generalized Kullback-Leibler divergence).

3) LDA - analyzes the chat corpus by performs topic modeling utilizing LDA 
(Latent Dirichlet Allocation).  Two implementations fo LDA were used:
a) sklearn_LDA - scikit-learn.org (sklearn) LDA module.

b) PyMallet_LDA - the LDA implementation from GitHub PyMallet at:
https://github.com/mimno/PyMallet

4) STTM - This directory contains the output of analyzing the chat corpus by 
performs topic modeling utilizing a Java software package called STTM (Short
Text Topic Modeling) available at:
https://github.com/qiang2100/STTM.


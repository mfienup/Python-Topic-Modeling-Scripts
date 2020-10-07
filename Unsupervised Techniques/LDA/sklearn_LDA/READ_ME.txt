This directory contains the scripts, data files, and output files from
analyzing the chat corpus by performs topic modeling utilizing LDA 
(Latent Dirichlet Allocation).

Note: We used the scikit-learn.org (sklearn) LDA module.


The two subdirectories contain:
1) sklearn_LDA_Scripts - contains the scripts and necessary data files to
analyze chat corpusby performs topic modeling utilizing LDA 
(Latent Dirichlet Allocation) transformation.

2) Output - topic files resulting from the LDA transformations.
Two types of text (.txt) files are included:
a) "raw_" text (.txt) file listing topics with each word scored
   (e.g., raw_LDA_wholeChatsFile_15topoics_8words.txt)
b) "LDA_" text (.txt) file containing only the text for the
   specified number of topics with the specified number of words 
   per topic (e.g., LDA_wholeChatsFile_15topoics_8words.txt)




This directory contains the output of analyzing the chat corpus by 
performs topic modeling utilizing a Java software package called STTM (Short
Text Topic Modeling) available at:
https://github.com/qiang2100/STTM.

The main motivation for exploring this tool was to try the DMM (Dirichlet 
Multinomial Mixture) algorithm which is claimed to work well on short text 
documents with a single topic per document.  For comparison we the included STTM's 
output of algorithms for LDA and BTM (Biterm topic modeling).

Article by the authors included in file:
Short Text Topic Modeling Techiques.pdf

Jipeng Qiang, Zhenyu Qian, Yun Li, Yunhao Yuan, and Xindong Wu.
Short Text Topic Modeling Techniques, Applications, and Performance: 
A Survey.  JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, APRIL 2019 

The three subdirectories contain:
1) STTM_DMM_Output - output files of analyzing preprocessed chat corpus using
STTM's DMM algorithm

2) STTM_LDA_Output - output files of analyzing preprocessed chat corpus using
STTM's LDA algorithm

3) STTM_BTM_Output - output files of analyzing preprocessed chat corpus using
STTM's BTM algorithm

NOTE:  The STTM package included its own PMI (pointwise mutual information) analysis
tool which generally agreed with our internally developed TC-PMI analysis.
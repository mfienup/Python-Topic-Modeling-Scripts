Going beyond unsupervised-learning topic models:  (LSA, pLSA, LDA), we decided
to focus on semi-supervised learning approaches to try to improve the quality
of the topics.

Semi-supervised approaches allow the user to specify sets of anchor/seed words which 
can be used to "nudge" the topic modeling.  Some possible reasons to nudge the topic modeling:
a) split a found topic into possibly two separate topics,
b) combine topics that should be related,
c) suggest new topics that where not originally found,
d) collect into a "garbage" topic noise words interfering with other topics
   (seems like these should be stopwords???) 

Two semi-supervised techniques were explored:

1) CorEx - subdirectory contains current scripts, output, and some 
background articles on CorEX (Correlation Explanation)
CorEx package available at GitHub:  
https://github.com/gregversteeg/corex_topic

2) GuidedLDA - subdirectory contains current scripts, output, and some 
background material on GuidedLDA
GuidedLDA package is available at GitHub:
https://github.com/vi3k6i5/GuidedLDA
NOTE:  We had difficulty installing GuidedLDA, but we were finally successful
by following the work-around posted at:
https://github.com/dex314/GuidedLDA_WorkAround
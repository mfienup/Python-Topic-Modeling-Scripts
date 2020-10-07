This directory contains the scripts and necessary data files to
analyze chat corpus by performs topic modeling utilizing LDA 
(Latent Dirichlet Allocation).

Here we are used the LDA implementation from GitHub PyMallet at:
https://github.com/mimno/PyMallet
The LDA code below is based on their lda_reference.py code written in Python
The PyMallet project has an MIT License see below.

The files are:

1) PyMallet_LDA_models.py - contains the script to analyze chat corpus by performs 
topic modeling utilizing LDA

2) INPUT (.csv) FILES - previously created preprocessed chat corpus from either:
wholeChatsFilePOS_N_ADJ_V.csv -- preprocessing keeping nouns, adjectives, and verbs
wholeChatsFilePOS_N_ADJ.csv -- preprocessing keeping nouns and adjectives
wholeChatsFile.csv -- NO POS preprocessing so all parts of speech
onlyQuestionsFile.csv -- Only initial question of chats
 


MIT License

Copyright (c) 2019 mimno

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


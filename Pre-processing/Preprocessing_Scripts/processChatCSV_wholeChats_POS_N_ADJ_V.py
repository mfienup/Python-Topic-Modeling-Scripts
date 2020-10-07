""" File:  processChatCSV_wholeChats_POS_N_ADJ_V.py
    Description:  Takes as input raw chat data .csv file and each chat is analyzed
    to keep only Parts-of-Speech (POS) including nouns, adjectives, and verbs.
    
    Takes as input raw chat data .csv file:
    original_without_identifiable_info_chat_transcripts_9942_041015_053119.csv
    It containing only columns:
    Timestamp, Duration (seconds), Initial Question, Message Count, Transcript
    and produces a list-of-lists called transcriptDialogList with a format:
    [[<excel index int>, "Initial question string", [Transcript split by chat responses which including initial
    question]], ...]

    This transcriptDialogList is used to write two text files with one chat dialog per line.
    It writes each processed chat keeping only POS of nouns, adjectives, and verbs to two text files:
    1) wholeChatsFilePOS_N_ADJ_V.csv with one chat per line formatted as:
       chat line # in original .csv, whole chat, and
    2) wholeChatsFilePOS_N_ADJ_V.txt with only the processed text of each chat one per line

    Additional processing:  words are lemmatized using nltk.WordNetLemmatizer()
"""

import re
import nltk
import gensim
from nltk.stem import WordNetLemmatizer

lemmatizer = nltk.WordNetLemmatizer()

# "constants"
INPUT_CSV_FILE_NAME = "original_without_identifiable_info_chat_transcripts_9942_041015_053119.csv"
WHOLE_CHATS_OUTPUT_FILE_NAME = "wholeChatsFilePOS_N_ADJ_V.csv"
WHOLE_CHATS_OUTPUT_FILE_NAME_TXT = "wholeChatsFilePOS_N_ADJ_V.txt"

POS_LIST = ['n','a','v']  # n - noun and a - adjective other possibilities: v -verb, r - adverb, 'other'
STOP_WORD_FILE_NAME = "stop_words.txt"

def getStopWords(stopWordFileName):
    stopWordDict = {}
    stopWordFile = open(stopWordFileName, 'r')

    for line in stopWordFile:
        word = line.strip().lower()
        stopWordDict[word] = None
        
    return stopWordDict


stopWordsDict = getStopWords(STOP_WORD_FILE_NAME)


def main():
    transcriptList = readRawChats(INPUT_CSV_FILE_NAME)
    initialQuestionCount = 0
    transIndex = 2  # Assumes Excel .cvs had a column-header in line 1
    transcriptDialogList = []
    for trans in transcriptList:
        transDialogList = generateTranscriptDialogList(trans)
        initialQuestion = findInitialQuestion(trans, transIndex)
        if initialQuestion == None:
            initialQuestion = findInitialQuestionInDialog(transDialogList,transIndex)           
        else:
            initialQuestionCount+= 1
            
        transcriptDialogList.append([transIndex, initialQuestion, transDialogList])
        transIndex += 1
    writeWholeChatsToFile(transcriptDialogList)
    
    return transcriptDialogList

def readRawChats(inFile):
    """
        Reads .csv file and split into transcripts by splitting on the Timestamp which includes the Date.
        The returned transcriptList is a list-of-lists where each "outer" list item contains information about
        a single chat.  
    """

    inFile = open(inFile, "r")  # NOTE .csv file assumed to have column-headings line

    dateAtStartCount = 0
    transcriptList = []
    currentTranscriptLines = []

    for line in inFile:
        frontOfLine = line[:6]
        if frontOfLine.count("/") == 2:
            dateAtStartCount += 1
            if dateAtStartCount == 1: #ignore header line
                currentTranscriptLines = [line.strip()]
            else:
                transcriptList.append(currentTranscriptLines)
                currentTranscriptLines = [line.strip()]
        else:
            currentTranscriptLines.append(line.strip())
    transcriptList.append(currentTranscriptLines)
    
    return transcriptList


def findInitialQuestion(transList, transIndex):
    """
        Takes in transList which is a list of strings containing the information about a single chat.
        The index 0 string will contain the Initial Question field, which it returns if it exists; otherwise
        None is returned."
    """
    
    firstCommaIndex = transList[0].find(",")
    if firstCommaIndex == -1:
        print("First comma not found")
        return None
    else:
        secondCommaIndex = transList[0].find(",",firstCommaIndex+1)
        if secondCommaIndex == -1:
            print("Second comma not found")
            return None
        else:
            thirdCommaIndex = transList[0].find(",",secondCommaIndex+1)
            if thirdCommaIndex == -1:
                thirdCommaIndex = len(transList[0])-1
           
            #print(secondCommaIndex, thirdCommaIndex)
            if secondCommaIndex + 1 == thirdCommaIndex:
                return None
            else:
                return transList[0][secondCommaIndex+1:thirdCommaIndex]

            
def generateTranscriptDialogList(trans):
    
    transcriptDialogList = []
    transStr = " ".join(trans)  # merge transcript back to a single string

    #split by time-stamps to get a dialogList
    transTimeIndexList = []
    for index in range(2,len(transStr)-6):
        if transStr[index] == ":" and transStr[index+3] == ":" and transStr[index+1:index+3].isdigit() and transStr[index+4:index+6].isdigit():
            transTimeIndexList.append(index-2)
    dialogList = []
    for i in range(len(transTimeIndexList)-1):
        dialogList.append(transStr[transTimeIndexList[i]:transTimeIndexList[i+1]])
    if len(transTimeIndexList) == 0:
        dialogList.append(transStr)
    else:
        dialogList.append(transStr[transTimeIndexList[-1]:])
    
    return dialogList    

def findInitialQuestionInDialog(dialogList, chatIndex):
    """ If the 'Initial question' column in the .csv file was empty, this function is called
        to find and return the initial question from the chat dialog."""

    for i in range(len(dialogList)):
        helpYouCount = dialogList[i].lower().count("help you")
        welcomeCount = dialogList[i].lower().count("welcome")
        infoDeskCount = dialogList[i].lower().count("info desk")
        try:
            if helpYouCount == 0 and welcomeCount == 0 and infoDeskCount == 0 and len(dialogList[i]) >= 40:
                return dialogList[i]
                
        except:
            print("\n\nNO QUESTION FOUND! ",chatIndex)
            break

def removeTags(fileStr):
    current = 0
    while True:
        #print("Next char:",fileStr[current])
        openAngleBracketIndex = fileStr.find('<',current)
        if openAngleBracketIndex == -1:
            break
        spaceIndex = fileStr.find(' ', openAngleBracketIndex+1)
        if spaceIndex == -1:
            break
        else:
            current = spaceIndex
        endStr = "</"+fileStr[openAngleBracketIndex+1:spaceIndex]+'>'

        endIndex = fileStr.find(endStr, spaceIndex)
        if endIndex == -1:
            current = spaceIndex
        else:
            endIndex = endIndex+len(endStr)

            #print(openAngleBracketIndex, endStr, endIndex+len(endStr))
            fileStr = fileStr[:openAngleBracketIndex]+ \
                      fileStr[endIndex:]
            #print(fileStr)
            current = openAngleBracketIndex
    return fileStr


"""
NOTE: The nltk.pos_tag function returns the Penn Treebank tag for the word but we just want
whether the word is a noun, verb, adjective or adverb. We need a short simplification routine to translate from
the Penn tag to a simpler tag.
"""


def simplify(penn_tag):
    """ Simplify Penn tags to n (NOUN), v (VERB), a (ADJECTIVE) or r (ADVERB)"""
    pre = penn_tag[0]
    
    if pre == 'J':
        return 'a'
    elif pre == 'R':
        return 'r'
    elif pre == 'V':
        return 'v'
    elif pre == 'N':
        return 'n'
    else:
        return 'other'

def preprocess(text, stop_words):
    """ Preprocesses the text to remove stopwords, lemmatizes each word and only includes
        words that are POS in the global POS_LIST"""

    toks = gensim.utils.simple_preprocess(str(text), deacc=True)
    wn = WordNetLemmatizer()
    return [wn.lemmatize(tok, simplify(pos)) for tok, pos in nltk.pos_tag(toks)
            if tok not in stop_words and simplify(pos) in POS_LIST]
        
def writeInitialQuestion(questionFile,  wholeChatsFileTxt, question):
    """ Write a cleaned up version of the initial question to the question file. """
    cleanQuestion = ""
    question = question.lower()

    colonCount = question.count(":")

    if colonCount >= 3:  # time-stamp ##:##:## - person: question
        colonOneIndex = question.find(":")
        colonTwoIndex = question.find(":", colonOneIndex+1)
        colonThreeIndex = question.find(":", colonTwoIndex+1)
        question = question[colonThreeIndex+1:]
    elif colonCount >= 1:
        colonOneIndex = question.find(":")
        question = question[colonOneIndex+1:]
        
    question = question.replace('&#x27;', "'")
    question = question.replace('&#x2F;', " ")
    question = question.replace('&nbsp;', " ")
    question = question.replace('&quot;','"')

    ### HERE CLEAN UP <xyz ......</xyz>, e.g., <a href.....</a>, <span ... </span>

    question = removeTags(question)
    question = question.replace('.','Z')
    question = question.replace('!','Z')
    question = question.replace('?','Z')
    
    masterWordList = []
    sentenceList = question.split("Z")
    for question in sentenceList:
        wordList = question.split()
        cleanQuestion = ""
        for word in wordList:
            cleanWord = ""
            for char in word:
                if char >= 'a' and char <= 'z':
                    cleanWord += char
            if len(cleanWord) > 0 and len(cleanWord) < 30:  #upper bound to eliminate url's
                cleanQuestion += lemmatizer.lemmatize(cleanWord) + " "
        pos_wordList = preprocess(cleanQuestion, stopWordsDict)
          
        masterWordList.extend(pos_wordList)
    chatCleaned = " ".join(masterWordList)
    questionFile.write(chatCleaned)
    wholeChatsFileTxt.write(chatCleaned)

def writeChatDialog(excelLineNumber, wholeChatsFile,  wholeChatsFileTxt, dialogList):
    """ Writes a chat's dialog to a line in the text file. """
    for i in range(len(dialogList)):
        helpYouCount = dialogList[i].lower().count("help you")
        welcomeCount = dialogList[i].lower().count("welcome")
        infoDeskCount = dialogList[i].lower().count("info desk")
            
        writeInitialQuestion(wholeChatsFile,  wholeChatsFileTxt, dialogList[i])
        wholeChatsFile.write(" ")  # separate end of this line with start of next line
        wholeChatsFileTxt.write(" ")  # separate end of this line with start of next line
        
   
def writeWholeChatsToFile(transcriptDialogList):
    """ Writes a whole chat's dialog one per line to a text file.  Removed from
        the line of text is:
        1) time-stamps and names:  e.g., '13:45:42 - Jordan:'
        2) all punctuations
    """

    wholeChatsFile = open(WHOLE_CHATS_OUTPUT_FILE_NAME, "w")
    wholeChatsFileTxt = open(WHOLE_CHATS_OUTPUT_FILE_NAME_TXT, "w")
    wholeChatsCount = 0
    for transcriptDialog in transcriptDialogList:

        if transcriptDialog[1] is not None:
            wholeChatsFile.write(str(transcriptDialog[0])+",")

            # check to see if initial question is already in the chat dialog
            timeStampAndNameList = re.findall(r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9] - [\w\s]+:', transcriptDialog[1])
            
            if len(timeStampAndNameList) == 0:  # no time-stamp so from 'initial question' column of .csv
                # write initial question to file since it is not part of the chat dialog
                writeInitialQuestion(wholeChatsFile, wholeChatsFileTxt, transcriptDialog[1])
                wholeChatsFile.write(" ")
                wholeChatsFileTxt.write(" ")
            writeChatDialog(transcriptDialog[0],wholeChatsFile,  wholeChatsFileTxt, transcriptDialog[2])
            
            #wholeChatsFile.write("\n")
            wholeChatsCount += 1
            wholeChatsFile.write("\n")
            wholeChatsFileTxt.write("\n")
    print("Whole Chats Count:", wholeChatsCount)
    wholeChatsFile.close()
    wholeChatsFileTxt.close()
    
t = main()  # start main running

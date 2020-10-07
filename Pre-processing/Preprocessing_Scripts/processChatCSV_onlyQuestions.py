""" File:  processChatCSV_onlyQuestions.py
    Description:  Takes as input raw chat data .csv file and each chat is analyzed to extract 
    only the initial question of each chat. The original chat data (.csv) from the LibChat 
    module of UNI's library SpringShare platform contained a "Initial Question" column which was not 
    enabled until 11/1/2018 and then only sporadically used by chat patrons.  If the Initial Question
    column of a chat was not used, then the chat text was analyzed to extract the initial question.

    Additionally the question text is "cleaned" by: 
    1) removing timestamps, 
    2) removing chat patron and librarian identifiers, 
    3) removing http tags (e.g., URLs), 
    4) removing non-ASCII characters,
    5) removing stopwords, and 
    6) lemmatized words using nltk.WordNetLemmatizer() 

    Takes as input raw chat data .csv file:
    original_without_identifiable_info_chat_transcripts_9942_041015_053119.csv
    It containing only columns:
    Timestamp, Duration (seconds), Initial Question, Message Count, Transcript
    and produces a list-of-lists called transcriptDialogList with a format:
    [[<excel index int>, "Initial question string", [Transcript split by chat responses which including initial
    question]], ...]

    This transcriptDialogList is used to write two text files with one chat dialog per line.
    It writes each processed chat keeping only POS of nouns and adjectives to two text files:
    1) onlyQuestionsFile.csv with one chat per line formatted as:
       chat line # in original .csv, initial question of chat, and
    2) onlyQuestionsFile.txt with only the processed initial question of each chat one per line

"""
import nltk

lemmatizer = nltk.WordNetLemmatizer()


# "constants"
## 9943 version only had chat Transcipt which was missing the Initial Question column which seemed important...
## INPUT_CSV_FILE_NAME = "original_without_identifiable_info_chat_transcripts_9943_041015_053119.csv"
INPUT_CSV_FILE_NAME = "original_without_identifiable_info_chat_transcripts_9942_041015_053119.csv"
QUESTION_ONLY_OUTPUT_FILE_NAME = "onlyQuestionsFile.csv"
QUESTION_ONLY_OUTPUT_FILE_NAME_TXT = "onlyQuestionsFile.txt"

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

    print("\nlen(transcriptList)", len(transcriptList))
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

    print("Number of initial questions from Initial Question column of .csv:", initialQuestionCount)
    
    questionFile = open(QUESTION_ONLY_OUTPUT_FILE_NAME, "w")
    questionTxtFile = open(QUESTION_ONLY_OUTPUT_FILE_NAME_TXT, "w")
    questionCount = 0
    for transcriptDialog in transcriptDialogList:
        if transcriptDialog[1] is not None:
            questionCount = writeInitialQuestion(transcriptDialog[0], questionFile, questionTxtFile, transcriptDialog[1], questionCount)

    print("Total Question Count:", questionCount)
    questionFile.close()
    questionTxtFile.close()
    
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
                #questionFile.write(str(chatIndex)+" in ["+str(i)+"]"+dialogList[i]+"\n")
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

def writeInitialQuestion(chatIndexInCSV, questionFile, questionTxtFile, question, questionCount):
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
##    question = question.replace('&#x2F;', "/")  # replace with space since / used to separate words
    question = question.replace('&#x2F;', " ")
    question = question.replace('&nbsp;', " ")
    question = question.replace('&quot;','"')

    ### HERE CLEAN UP <xyz ......</xyz>, e.g., <a href.....</a>, <span ... </span>
    question = removeTags(question)
    
    wordList = question.split()
    for word in wordList:
        cleanWord = ""
        for char in word:
            if char >= 'a' and char <= 'z':
                cleanWord += char
        if len(cleanWord) > 0:
            cleanWord = lemmatizer.lemmatize(cleanWord)
            if cleanWord not in stopWordsDict:
                cleanQuestion += cleanWord + " "
    if len(cleanQuestion) > 0:        
        questionFile.write(str(chatIndexInCSV)+","+cleanQuestion[:-1]+"\n")
        questionTxtFile.write(cleanQuestion[:-1]+"\n")
        questionCount += 1

    return questionCount
    
t = main()  # start main running

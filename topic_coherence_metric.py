""" File: topic_coherence_metric.py
    Calculates the topic coherence metrics TC-PMI, TC-LCP, and TC-NZ for set of topics.
    User inputs:
       docFileName: pre-processed chat document file e.g. wholeChatsFilePOS.csv
         (Assumes one line per document formatted as: column 0 chat-transcript line # in .xlsx file and
          column 1 cleaned chat transcript)
       topicsFile: text file containing topics one per line e.g., STTM_BTM_POS_15topics_8words.txt
    Input Files needed:  "stop_words.txt"

    Output file: TC_metrics_+topicsFile file name contains the PMI, LCP and NZ for individual topics
       and the average PMI, LCP and NZ for all the topics.

"""
import math

EPSILON = 0.000000001

def main():
    #docFileName = "wholeChatsFilePOS.csv"
    docFileName = input("Enter the pre-processed chat document file, e.g. wholeChatsFilePOS.csv")
    stopWordFileName = "stop_words.txt"
    #topicsFile = "STTM_BTM_POS_15topics_8words.txt"
    topicsFile = input("Enter the text file containing topics one per line e.g., STTM_BTM_POS_15topics_8words.txt")
    stopWordDict = getStopWords(stopWordFileName)

    outputFileName = "TC_metrics_"+topicsFile

    coOccurrenceDict = {}
    wordDict = {}
    topicsList, topicsCoOccurrenceList, coOccurrenceDict, wordDict = findcoOoccurrencesAndWordsInTopics(topicsFile)
    numberOfTopics = len(topicsList)
    print("# topics", numberOfTopics)
    
    docCount = tallycoOoccurrencesAndWordsInDocs(docFileName, coOccurrenceDict, wordDict)

    counts = list(coOccurrenceDict.values())
    print("# 0s", counts.count(0))
    for cooccurrence in coOccurrenceDict:
        if coOccurrenceDict[cooccurrence] == 0:
            print(cooccurrence)

    makeProbabilities(docCount, coOccurrenceDict, wordDict)

    outputFile = open(outputFileName, 'w')

    outputFile.write("File: "+outputFileName+"\n\n")
    
    sumPMI = 0.0
    sumLCP = 0.0
    sumNZ = 0
    index = 0
    for topicCoOccurrence in topicsCoOccurrenceList:
        topicPMI = calculateTopicPMI(topicCoOccurrence, coOccurrenceDict, wordDict)
        topicLCP = calculateTopicLCP(topicCoOccurrence, coOccurrenceDict, wordDict)
        topicNZ = calculateTopicNZ(topicCoOccurrence, coOccurrenceDict)
        outputFile.write(topicsList[index]+"\n")
        outputFile.write("PMI = %.3f  " % (topicPMI))
        outputFile.write("LCP = %.3f  " % (topicLCP))
        outputFile.write("NZ = %d\n" % (topicNZ))
        sumPMI += topicPMI
        sumLCP += topicLCP
        sumNZ += topicNZ
        index += 1
    averagePMI = sumPMI/numberOfTopics
    averageLCP = sumLCP/numberOfTopics
    averageNZ = sumNZ/numberOfTopics
    outputFile.write("\nAverage PMI of all topics: %.3f\n" % (averagePMI))
    outputFile.write("\nAverage LCP of all topics: %.3f\n" % (averageLCP))
    outputFile.write("\nAverage NZ of all topics: %.3f\n" % (averageNZ))
    outputFile.close()

def makeProbabilities(docCount, coOccurrenceDict, wordDict):
    """ Converses the raw counts in the coOccurrenceDict and wordDict into probabilities."""
    for coOccurrence in coOccurrenceDict:
        coOccurrenceDict[coOccurrence] /= float(docCount)
    for word in wordDict:
        wordDict[word] /= float(docCount)

def calculateTopicPMI(topicCoOccurrenceList, coOccurrenceDict, wordDict):
    """ Calculates and returns a topic's total PMI. """ 
    sumPMI = 0.0
    for topicCoOccurrence in topicCoOccurrenceList:
        sumPMI += calculatePMI(topicCoOccurrence, coOccurrenceDict, wordDict)
    return sumPMI/len(topicCoOccurrenceList)

def calculateTopicLCP(topicCoOccurrenceList, coOccurrenceDict, wordDict):
    """ Calculates and returns a topic's total LCP. """ 
    sumLCP = 0.0
    for topicCoOccurrence in topicCoOccurrenceList:
        firstWord, secondWord = topicCoOccurrence
        sumLCP += calculateLCP(firstWord, topicCoOccurrence, coOccurrenceDict, wordDict)
        sumLCP += calculateLCP(secondWord, topicCoOccurrence, coOccurrenceDict, wordDict)
    return sumLCP/(2*len(topicCoOccurrenceList))

def calculateTopicNZ(topicCoOccurrenceList, coOccurrenceDict):
    """ Calculates and returns a topic's total NZ. """ 
    sumNZ = 0
    for topicCoOccurrence in topicCoOccurrenceList:
        if coOccurrenceDict[topicCoOccurrence] == 0.0:
            sumNZ += 1
    return sumNZ


def calculatePMI(topicCoOccurrence, coOccurrenceDict, wordDict):
    """ Calculates and returns the PMI for a pair of words in the topicCoOccurrence tuple. """
    wordI, wordJ = topicCoOccurrence
    PMI = math.log((coOccurrenceDict[topicCoOccurrence]+EPSILON)/(wordDict[wordI]*wordDict[wordJ]),10)
    return PMI
        
        
def calculateLCP(word, topicCoOccurrence, coOccurrenceDict, wordDict):
    """ Calculates and returns the LCP for a word in the pair of words in the topicCoOccurrence tuple. """
    LCP = math.log((coOccurrenceDict[topicCoOccurrence]+EPSILON)/(wordDict[word]),10)
    return LCP
        
        
def tallycoOoccurrencesAndWordsInDocs(docFileName, coOccurrenceDict, wordDict):
    """ Tallys across all the documents (in file docFileName) the word pair co-occurrences in coOccurrenceDict, and
        individual words in wordDict."""
    docFile = open(docFileName, "r")
    docCount = 0
    for line in docFile:
        document = line.strip().split(',')[1]
        emptyDoc = tallyCoOccurrencesInDoc(document, coOccurrenceDict, wordDict)
        if not emptyDoc:
            docCount += 1
    return docCount

def tallyCoOccurrencesInDoc(document, coOccurrenceDict, wordDict):
    """ Tallys for an individual document the word pair co-occurrences in coOccurrenceDict, and
        individual words in wordDict."""
    docCoOccurrenceDict = {}
    docWordDict = {}
    
    wordList = document.strip().split()
    if len(wordList) == 0:
        return True   # empty document
    
    # eliminate duplicate words by converting to a set and back
    wordSet = set(wordList)
    wordList = list(wordSet)

    wordList.sort()
    for first in range(len(wordList)):
        if wordList[first] in wordDict:
            wordDict[wordList[first]] += 1
        for second in range(first+1,len(wordList)):
            coOccurrenceTuple = (wordList[first], wordList[second])
            if coOccurrenceTuple in coOccurrenceDict:
                coOccurrenceDict[coOccurrenceTuple] += 1
    return False   # not empty document

def findcoOoccurrencesAndWordsInTopics(topicsFileName):
    """ Processes the topics file and returns:
        topicsList - list of strings with one whole topic as a string,
        topicsCoOccurrenceList - a list-of-lists with the inner-list being the list word pairs as tuples within a topic,
        coOccurrenceDict - keys are tuple of word pairs that co-occur in the topics with their associated values of 0,
        wordDict - keys are words that occur in the topics with their associate values of 0."""

    topicsFile = open(topicsFileName, "r")
    fileNameLine = topicsFile.readline()
    blankLine = topicsFile.readline()
    topicsCoOccurrenceList = []
    coOccurrenceDict = {}
    wordDict = {}
    topicTupleList = []
    topicsList = []
    for line in topicsFile:
        topicTupleList = []
        topicsList.append(line.strip())
        wordList = line.strip().split()
        wordList.sort()
        for first in range(len(wordList)):
            wordDict[wordList[first]] = 0
            for second in range(first+1,len(wordList)):
                coOccurrenceTuple = (wordList[first], wordList[second])
                coOccurrenceDict[coOccurrenceTuple] = 0
                topicTupleList.append(coOccurrenceTuple)
        topicsCoOccurrenceList.append(topicTupleList)
    return topicsList, topicsCoOccurrenceList,coOccurrenceDict, wordDict


def getStopWords(stopWordFileName):
    """ Reads the stop-words file and returns a dictionary containing all the stop-words."""
    stopWordDict = {}
    stopWordFile = open(stopWordFileName, 'r')

    for line in stopWordFile:
        word = line.strip().lower()
        stopWordDict[word] = None
    return stopWordDict
        
main()

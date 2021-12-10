import sys
import pprint

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    # Add each line into a list which we'll work on
    codeLines = []
    for line in lines:
        line = line.rstrip()
        codeLines.append(line)
    return codeLines

# Check if character passed in is an opening character
def isOpeningChar(char):
    if char == '(' or char == '[' or char == '{' or char == '<':
        return True
    else:
        return False

# Check to see if the two brackets align
def bracketsMatch(openingChar, closingChar):
    if ((openingChar == '(' and closingChar == ')') or
        (openingChar == '[' and closingChar == ']') or
        (openingChar == '{' and closingChar == '}') or
        (openingChar == '<' and closingChar == '>')):
        return True
    else:
        return False

# Close out all the remaining characters
def completeCharBuffer(openingCharBuffer):
    closeString = []
    while len(openingCharBuffer) > 0:
        openChar = openingCharBuffer.pop()
        if openChar == '(':
            closeString.append(')')
        elif openChar == '[':
            closeString.append(']')
        elif openChar == '{':
            closeString.append('}')
        elif openChar == '<':
            closeString.append('>')
    return closeString
    
# Scan through each line of code and flag the first illegal character encountered
# If no illegal characters are encountered, generate an autocompletion string 
def parseLines(codeLines):
    illegalChars = []
    completionStrings = []
    for line in codeLines:
        legalString = True
        openingCharBuffer = []
        for char in line:
            # If it's an opening char, add it to our buffer and continue
            if isOpeningChar(char):
                openingCharBuffer.append(char)
            # If it's a closing char, pop our buffer and see if the two align. If they do, continue.  Else flag the illegal char and move on to the next line
            else:
                prevChar = openingCharBuffer.pop()
                if not bracketsMatch(prevChar, char):
                    illegalChars.append(char)
                    legalString = False
                    break
        # If we make it to here without encountering an illegal character, close the remaining brackets in the buffer and append it to our completionStrings list
        if legalString:
            completionStrings.append(completeCharBuffer(openingCharBuffer))
    return illegalChars, completionStrings

# Sum up the scores for all the illegal characters found
def getSyntaxErrorScore(illegalChars):
    score = 0
    for char in illegalChars:
        if char == ')':
            score = score + 3
        elif char == ']':
            score = score + 57
        elif char == '}':
            score = score + 1197
        elif char == '>':
            score = score + 25137
    return score

# Find the median completion score for all the completion strings passed in
def getCompletionScore(completionStrings):
    completionScores = []
    for string in completionStrings:
        stringScore = 0
        for char in string:
            stringScore = stringScore * 5
            if char == ')':
                stringScore = stringScore + 1
            elif char == ']':
                stringScore = stringScore + 2
            elif char == '}':
                stringScore = stringScore + 3
            elif char == '>':
                stringScore = stringScore + 4
        completionScores.append(stringScore)

    # Now that we have our full list of scores, sort them and find the median score
    completionScores.sort()
    finalScoreIndex = int(len(completionScores) / 2)
    finalScore = completionScores[finalScoreIndex]
    return finalScore

# Are we running against test or input?
runFlag = sys.argv[1]
codeLines = getData(runFlag)
illegalChars, completionStrings = parseLines(codeLines)
syntaxScore = getSyntaxErrorScore(illegalChars)
completionScore = getCompletionScore(completionStrings)
print("Syntax score: " + str(syntaxScore) + " Completion score: " + str(completionScore))
print("Done!")

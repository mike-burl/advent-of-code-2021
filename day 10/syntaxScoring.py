import sys

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
    
# Scan through each line of code and flag the first illegal character encountered
def getIllegalChars(codeLines):
    illegalChars = []
    for line in codeLines:
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
                    break
    return illegalChars

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

# Are we running against test or input?
runFlag = sys.argv[1]
codeLines = getData(runFlag)
illegalChars = getIllegalChars(codeLines)
finalAnswer = getSyntaxErrorScore(illegalChars)
print(str(finalAnswer))
print("Done!")

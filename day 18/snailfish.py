import sys
import math

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    snailNums = []
    for line in lines:
        line = line.rstrip()
        snailNums.append(line)
    return snailNums

# Explode the snail number a single time, return true if the explode condition is hit
def explodeNum(snailNum):
    # Iterate across the string until we hit a depth of 4 or deeper along with two integers
    # At that point explode the pair
    depth = -1
    openIndex = 0
    closeIndex = 0
    prevNumIndex = -1
    explosion = False
    for index, char in enumerate(snailNum):
        if char == '[':
            depth += 1
            openIndex = index
        elif char == ']':
            depth -= 1
        # If the depth is still under 4, we want to keep track of our last encountered numerical digit
        if depth < 4 and char.isdigit():
            prevNumIndex = index
        # Check to see if we've hit our exploding digit
        if depth >= 4 and char.isdigit():
            explosion = True
            # Get left and right number
            closeIndex = snailNum.find("]", openIndex)
            numPair = snailNum[openIndex+1:closeIndex].split(",")
            # We'll do the following steps from right to left to help prevent headaches with string indexes
            # Find the next number to the right and add our right number to it
            rightNumFound = False
            rightNumIndex = -1
            rightNumIndexStart = snailNum.find("]", index)
            for nextNumIndex in range(rightNumIndexStart, len(snailNum)):
                if snailNum[nextNumIndex].isdigit() and rightNumFound == False:
                    rightNumFound = True
                    rightNumIndex = nextNumIndex
                # We found the end of the right digit.  Swap things out and break
                elif not snailNum[nextNumIndex].isdigit() and rightNumFound == True:
                    rightNum = int(snailNum[rightNumIndex:nextNumIndex]) + int(numPair[1])
                    snailNum = snailNum[:rightNumIndex] + str(rightNum) + snailNum[nextNumIndex:]
                    break
            # Next we'll explode the center into a zero
            snailNum = snailNum[:openIndex] + "0" + snailNum[rightNumIndexStart+1:]
            # If prevNumIndex has any value besides -1, add our left number to whatever number exists there
            if prevNumIndex > -1:
                prevNumString = ""
                for prevNumStartingIndex in range(prevNumIndex, 0, -1):
                    if not snailNum[prevNumStartingIndex].isdigit():
                        # We hit a non-numerical character, time to swap things out
                        prevNum = int(snailNum[prevNumStartingIndex+1:prevNumIndex+1]) + int(numPair[0])
                        snailNum = snailNum[:prevNumStartingIndex+1] + str(prevNum) + snailNum[prevNumIndex+1:]
                        break
            break
    return snailNum, explosion

# Split the snail number a single time, return true if a split occurs
def splitNum(snailNum):
    split = False
    firstDigitLoc = -1
    finalDigitLoc = -1
    # Iterate until we find a two digit number
    for index, char in enumerate(snailNum):
        if char.isdigit() and firstDigitLoc == -1:
            firstDigitLoc = index
        elif char.isdigit() and firstDigitLoc != -1:
            finalDigitLoc = index
        elif not char.isdigit() and finalDigitLoc == -1:
            firstDigitLoc = -1
        elif not char.isdigit() and finalDigitLoc != -1:
            # Split our number
            split = True
            number = int(snailNum[firstDigitLoc:finalDigitLoc+1])
            leftNum = str(math.floor(number / 2))
            rightNum = str(math.ceil(number / 2))
            snailNum = snailNum[:firstDigitLoc] + "[" + leftNum + "," + rightNum + "]" + snailNum[index:]
            break
    return snailNum, split
            
# Add two snail numbers together
def addSnailNums(numA, numB):
    # First append the two together
    returnNum = "[" + numA + "," + numB + "]"
    # Now loop over the resulting sum and explode/split any pairs
    exploded = True
    split = True
    while exploded or split:
        returnNum, exploded = explodeNum(returnNum)
        if not exploded:
            # We'll implement the split logic here later
            returnNum, split = splitNum(returnNum)
    return returnNum

# Parse snail number string into a list
def parseSnailNum(snailNumString):
    if(snailNumString.isnumeric()):
        return int(snailNumString)
    snailNumString = snailNumString[1:-1]
    returnTree = []
    level = 0
    for index, char in enumerate(snailNumString):
        if char == '[':
            level += 1
        elif char == ']':
            level -= 1
        elif char == ',' and level == 0:
            returnTree.append(parseSnailNum(snailNumString[:index]))
            returnTree.append(parseSnailNum(snailNumString[index+1:]))
            break
    return returnTree

# Get the pair's magnitude
def getPairMagnitude(pair):
    leftVal = 0
    rightVal = 0
    if isinstance(pair[0], int):
        leftVal = 3 * pair[0]
    else:
        leftVal = 3 * getPairMagnitude(pair[0])
    if isinstance(pair[1], int):
        rightVal = 2 * pair[1]
    else:
        rightVal = 2 * getPairMagnitude(pair[1])
    return leftVal + rightVal

# Get the snail magnitude of the snail number
def getMagnitude(finalSnailNum):
    snailTree = parseSnailNum(finalSnailNum)
    magnitude = getPairMagnitude(snailTree)
    return magnitude
    
# Are we running against test or input?
runFlag = sys.argv[1]
snailNums = getData(runFlag)
print("# of snailNums: " + str(len(snailNums)))
finalSnailNum = snailNums[0]
for index, snailNum in enumerate(snailNums[1:]):
    finalSnailNum = addSnailNums(finalSnailNum, snailNum)
    print(str((index+1)/(len(snailNums)-1))[0:4] + "% done")
print(str(finalSnailNum))
snailMagnitude = getMagnitude(finalSnailNum)
print(str(snailMagnitude))

import sys
from collections import Counter

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    # Extract the starting polymer string and put the pair insertion rules into a map
    polymer = lines[0].rstrip()
    insertionMap = {}
    for line in lines[2:]:
        line = line.rstrip()
        pair = line.split(" -> ")
        insertionMap[pair[0]] = pair[1]
    return polymer, insertionMap

# Iterate over the keys from both maps and add up the counts in both
def mergeCharMaps(charMapA, charMapB):
    returnCharMap = {}
    keys = set(charMapA.keys()) | set(charMapB.keys())
    for key in keys:
        returnCharMap[key] = charMapA.get(key, 0) + charMapB.get(key, 0)
    return returnCharMap
    
# Recursive function.  If currentStep < numSteps, expand each pair and delve another step deeper
# If currentStep = numSteps, return a map of counts for the characters
# Sum up the character counts of subfunctions
# If we're at the bottom of our stack, strip out one instance of the stripLeftChar if it's defined
def expandPolymer(currentStep, numSteps, polymer, insertionMap, stripLeftChar):
    if currentStep == 10 or currentStep == 20:
        print("currentStep: " + str(currentStep) + " numSteps: " + str(numSteps) + " polymer: " + polymer + " stripLeftChar: " + str(stripLeftChar))
    # We will always expand the polymer string first
    polyList = list(polymer)
    insertList = []
    for index, char in enumerate(polyList[:-1]):
        lookupKey = polyList[index] + polyList[index + 1]
        insertChar = insertionMap[lookupKey]
        insertList.append(insertChar)
    expandedList = []
    for index, char in enumerate(polyList[:-1]):
        expandedList.append(char)
        expandedList.append(insertList[index])
    expandedList.append(polyList[len(polyList) - 1])
    polymer = ''.join(expandedList)
    #print("Polymer expanded to: " + polymer)
    # Now that we have the expanded polymer, see if we're popping up the stack or going deeper down
    # If we've reached the target depth, convert into a character map and return
    if currentStep == numSteps:
        charMap = Counter(polymer)
        #print("We're at the bottom: " + str(charMap))
        if stripLeftChar:
            charMap[stripLeftChar] = charMap[stripLeftChar] - 1
            #print("Returning modified charMap: " + str(charMap))
            return charMap
        else:
            #print("Returning unmodified charMap")
            return charMap
    # Else we split our polymer into the recursive function and add up the results
    charMap = {}
    # If stripLeftChar is still None then we're all the way on the left of the tree
    if not stripLeftChar:
        charMap = expandPolymer((currentStep + 1), numSteps, polymer[:2], insertionMap, None)
    else:
        charMap = expandPolymer((currentStep + 1), numSteps, polymer[:2], insertionMap, polymer[0:1])
    # Now iterate over the remaining pairs and add their results to our charMap
    for index, char in enumerate(expandedList[1:-1]):
        nextCharMap = expandPolymer((currentStep + 1), numSteps, ''.join(expandedList[index+1:index+3]), insertionMap, expandedList[index+1])
        charMap = mergeCharMaps(charMap, nextCharMap)
    return charMap

# Find the most and least common characters, then subtract the least count from the most count to get our final score
def getFinalScore(polymer):
    charMap = Counter(polymer)
    highScore = max(charMap.values())
    lowScore = min(charMap.values())
    finalScore = highScore - lowScore
    return finalScore
    
# Are we running against test or input?
runFlag = sys.argv[1]
numSteps = int(sys.argv[2])
polymer, insertionMap = getData(runFlag)
print("Template: " + polymer)
print("Insertion map: " + str(insertionMap))
polymerFreqs = expandPolymer(1, numSteps, polymer, insertionMap, None)
print(str(polymerFreqs))
finalScore = getFinalScore(polymerFreqs)
print("Final score: " + str(finalScore))
print("Done!")

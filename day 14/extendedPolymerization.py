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

# Expand the polymer a single time
def expandPolymer(polymer, insertionMap):
    # We'll keep a list of characters for both the original polymer along with the insertion characters
    # This way it will be easy to zipper the two together to make our final string
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
    return ''.join(expandedList)

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
for step in range(numSteps):
    polymer = expandPolymer(polymer, insertionMap)
print("Final polymer length: " + str(len(polymer)))
finalScore = getFinalScore(polymer)
print("Final score: " + str(finalScore))
print("Done!")

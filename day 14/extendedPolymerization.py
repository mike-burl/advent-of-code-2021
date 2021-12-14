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

# Find the most and least common characters, then subtract the least count from the most count to get our final score
def getFinalScore(charCounts):
    highScore = max(charCounts.values())
    lowScore = min(charCounts.values())
    finalScore = highScore - lowScore
    return finalScore

# Initialize our pair counters
def getPairCounts(polymer, insertionMap):
    keys = insertionMap.keys()
    pairCounts = {key: 0 for key in keys}
    for index, char in enumerate(polymer[:-1]):
        pairCounts[polymer[index:index+2]] = pairCounts[polymer[index:index+2]] + 1
    return pairCounts

# Initialize an empty pair counter
def getNewPairCounter():
    keys = insertionMap.keys()
    pairCounts = {key: 0 for key in keys}
    return pairCounts

# Are we running against test or input?
runFlag = sys.argv[1]
numSteps = int(sys.argv[2])
polymer, insertionMap = getData(runFlag)
# Initialize the char counts
charCounts = Counter(polymer)
pairCounts = getPairCounts(polymer, insertionMap)
# Expand for number of steps input by user
for step in range(numSteps):
    newPairCounts = getNewPairCounter()
    # For each step iterate over the pairCount dictionary
    for key, value in pairCounts.items():
        # If the value is zero we don't care, skip it
        if value > 0:
            # Get the character we'll be introducing with this pair
            newChar = insertionMap[key]
            # Increment the charCount for how many pairs we have
            charCounts[newChar] = charCounts[newChar] + value
            # Get the two new pairs the current pair expands into
            newKeyA = key[0] + newChar
            newKeyB = newChar + key[1]
            # Increment the two new keys into the newPairCounter
            newPairCounts[newKeyA] = newPairCounts[newKeyA] + value
            newPairCounts[newKeyB] = newPairCounts[newKeyB] + value
    pairCounts = newPairCounts
finalScore = getFinalScore(charCounts)
print("Final score: " + str(finalScore))
print("Done!")

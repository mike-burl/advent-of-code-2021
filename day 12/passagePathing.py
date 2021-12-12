import sys
import pprint

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()        
    # We'll build our paths using a dictionary.  For each entry we'll add a path for each side
    passages = {}
    for line in lines:
        line = line.rstrip()
        caves = line.split("-")
        if caves[0] in passages:
            passages[caves[0]].append(caves[1])
        else:
            passages[caves[0]] = [caves[1]]
        if caves[1] in passages:
            passages[caves[1]].append(caves[0])
        else:
            passages[caves[1]] = [caves[0]]
    return passages

# Recursively traverse the graph
def getSubPaths(currentCave, path, passages):
    path.append(currentCave)
    # If we're at the end just return one
    if currentCave == "end":
        print(str(path))
        return 1
    # Otherwise we need to get the list of passages attached to our cave, see which we're able to visit
    subPathCount = 0
    subPathList = passages[currentCave]
    for subPath in subPathList:
        # If the subPath is lowercase we need to made sure we haven't already visited it
        # Remember that lists are implicitly passed by reference, so for each recursive iteration we'll need to copy the path list
        if subPath.islower() and subPath not in path:
            subPathCount = subPathCount + getSubPaths(subPath, path.copy(), passages)
        elif subPath.isupper():
            subPathCount = subPathCount + getSubPaths(subPath, path.copy(), passages)
    return subPathCount

# Are we running against test or input?
runFlag = sys.argv[1]
passages = getData(runFlag)
# We'll solve this recursively.  Use a list of strings to keep track of what our current path is
# For each node, iterate through the dictionary to find all caves attached to our current cave
# If the connected cave is upper case, we'll just go to it.  If the cave is lower case, check to make sure
# that it isn't in our list of visited caves already.  Return the sum of each of the sub-paths.  If we hit
# the end, return one.  If we can't move to any other caves, return zero.
path = []
numPaths = getSubPaths("start", path, passages)
print("Number of unique paths: " + str(numPaths))
print("Done!")

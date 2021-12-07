import sys

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()

    # For each line we're going to remove all whitespace, split on '->', then split again on commas
    for line in lines:
        line = "".join(line.split())
        line = "".join(line.replace("->", ","))
        line = line.split(",")
        line = list(map(int, line))
        crabPositions = []
        # Put all of our crab positions into a list
        for crabPosition in line:
            crabPositions.append(crabPosition)
        # Now sort the list
        return sorted(crabPositions)

# Build an index of crab positions to make calculating distance shifts easier later
def buildCrabPositionIndex(crabPositions):
    rightMostPosition = crabPositions[len(crabPositions) - 1]
    crabCounts = [0] * (rightMostPosition + 1)
    for crabPosition in crabPositions:
        crabCounts[crabPosition] = crabCounts[crabPosition] + 1
    return crabCounts

# Sum up all crabs to the right of our starting position
def getRightCrabs(crabCounts):
    rightCrabCount = 0
    rightCrabDistance = 0
    for index, crabCount in enumerate(crabCounts[1:]):
        # We only care about crabs to the right so start at index position 1
        # For each index we'll add the number of crabs stored to the count, then calculate the distance
        # from zero, multiply it by the number of crabs there and add it to the total right distance
        if crabCount > 0:
            rightCrabCount = rightCrabCount + crabCount
            rightCrabDistance = rightCrabDistance + ((index+1) * crabCount)
    return rightCrabCount, rightCrabDistance

# Find the ideal position for all crab submarines to move to while minimizing fuel usage
def findIdealPosition(crabPositions, crabCounts):
    # We'll initialize at the leftmost crab
    currentCrabs = crabCounts[crabPositions[0]]
    # Since we're starting at the leftmost crab, leftCrabs is safe to initialize at zero
    leftCrabCount = 0
    leftCrabDistance = 0
    rightCrabCount, rightCrabDistance = getRightCrabs(crabCounts)
    idealDistance = rightCrabDistance
    idealPosition = 0

    # Now we iterate to the right.  Keep track of the number of crabs to the left and right along with their distances
    for index, crabCount in enumerate(crabCounts):
        # skip the first index since this has already been handled
        if index == 0:
            continue
        leftCrabCount = leftCrabCount + crabCounts[index - 1]
        leftCrabDistance = leftCrabDistance + leftCrabCount
        currentCrabs = crabCounts[index]
        rightCrabDistance = rightCrabDistance - rightCrabCount
        rightCrabCount = rightCrabCount - currentCrabs
        if (leftCrabDistance + rightCrabDistance) < idealDistance:
            idealDistance = (leftCrabDistance + rightCrabDistance)
            idealPosition = index

    return idealPosition, idealDistance

# Are we running against test or input?
runFlag = sys.argv[1]

crabPositions = getData(runFlag)
crabCounts = buildCrabPositionIndex(crabPositions)
idealPosition, idealDistance = findIdealPosition(crabPositions, crabCounts)
print("Final answer: (" + str(idealPosition) + "," + str(idealDistance) + ")")
print("Done!")

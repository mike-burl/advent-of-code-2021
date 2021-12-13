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

# Build an index of move costs to use later so we don't have to redo this over and over
# We keep this in its own function as our understanding of move costs may change in the future
def buildMoveCostsIndex(crabCounts):
    totalDistance = len(crabCounts)
    moveCosts = [0]
    for distance in range(1, totalDistance):
        totalCosts = moveCosts[distance - 1] + distance
        moveCosts.append(totalCosts)
    return moveCosts

# Sum up all fuel costs for crabs to the right of our position
def getRightCrabFuel(position, crabCounts, moveCosts):
    rightCrabFuel = 0
    # We only care about crabs to the right so start at the position given to us
    for index, crabCount in enumerate(crabCounts[position + 1:]):
        # For each index we'll see how many crabs exist there and multiply it by it's corresponding moveCost
        if crabCount > 0:
            rightCrabFuel = rightCrabFuel + ((moveCosts[index + 1]) * crabCount)
    return rightCrabFuel

# Sum up all fuel costs for crabs to the left of our position
def getLeftCrabFuel(position, crabCounts, moveCosts):
    leftCrabFuel = 0
    # We only care about crabs to the left so start at zero and move up until we hit our position
    for index, crabCount in enumerate(crabCounts[:position]):
        # For each index we'll see how many crabs exist there and multiply it by it's corresponding moveCost
        if crabCount > 0:
            leftCrabFuel = leftCrabFuel + ((moveCosts[position - index]) * crabCount)
    return leftCrabFuel

# Find the ideal position for all crab submarines to move to while minimizing fuel usage
def findIdealPosition(crabPositions, crabCounts, moveCosts):
    # We'll initialize at the leftmost crab
    idealPosition = 0
    # Since we're starting at the leftmost crab, leftCrabFuel is safe to initialize at zero
    leftCrabFuel = 0
    rightCrabFuel = getRightCrabFuel(0, crabCounts, moveCosts)
    idealFuel = rightCrabFuel

    # Now we iterate to the right.  Recalculate the fuel costs to the right and left and see if it's better than our previous best
    for index, crabCount in enumerate(crabCounts):
        # skip the first index since this has already been handled
        if index == 0:
            continue
        leftCrabFuel = getLeftCrabFuel(index, crabCounts, moveCosts)
        rightCrabFuel = getRightCrabFuel(index, crabCounts, moveCosts)
        totalFuel = leftCrabFuel + rightCrabFuel
        if totalFuel < idealFuel:
            idealFuel = totalFuel
            idealPosition = index
    return idealPosition, idealFuel

# Are we running against test or input?
runFlag = sys.argv[1]

crabPositions = getData(runFlag)
crabCounts = buildCrabPositionIndex(crabPositions)
moveCosts = buildMoveCostsIndex(crabCounts)
idealPosition, idealFuel = findIdealPosition(crabPositions, crabCounts, moveCosts)
print("Final answer: (" + str(idealPosition) + "," + str(idealFuel) + ")")
print("Done!")

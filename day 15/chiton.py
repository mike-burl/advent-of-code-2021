import sys
import pprint
import math

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()

    # We'll extract the input into a standard 2d list
    # Repeat the process five times in both the x and y directions
    riskMap = []
    for i in range(5):
        for line in lines:
            line = line.rstrip()
            riskLine = []
            # We want to loop this process five times
            for j in range(5):
                for number in line:
                    wrappedNumber = int(number) + j + i
                    if wrappedNumber > 9: 
                        wrappedNumber = wrappedNumber - 9
                    riskLine.append(wrappedNumber)
            riskMap.append(riskLine)
    return riskMap

# Iterate through the four neighbors of the passed position and find the lowest cost viable neighbor
# Only return if the cost is associated with an unvisited node
# If no viable neighbors exist, return None, None
def getBestNeighbor(pos, risk):
    global totalRiskMap
    global riskMap
    viableNeighbor = False
    bestRisk = math.inf
    bestNeighbor = []
    xPos = pos[0]
    yPos = pos[1]
    # Check North
    if xPos > 0 and totalRiskMap[xPos - 1][yPos] == math.inf:
        viableNeighbor = True
        if riskMap[xPos - 1][yPos] < bestRisk:
            bestRisk = riskMap[xPos - 1][yPos]
            bestNeighbor = [(xPos - 1), yPos]
    # Check South
    if xPos < (len(riskMap) - 1) and totalRiskMap[xPos + 1][yPos] == math.inf:
        viableNeighbor = True
        if riskMap[xPos + 1][yPos] < bestRisk:
            bestRisk = riskMap[xPos + 1][yPos]
            bestNeighbor = [(xPos + 1), yPos]
    # Check East
    if yPos > 0 and totalRiskMap[xPos][yPos - 1] == math.inf:
        viableNeighbor = True
        if riskMap[xPos][yPos - 1] < bestRisk:
            bestRisk = riskMap[xPos][yPos - 1]
            bestNeighbor = [xPos, (yPos - 1)]
    # Check West
    if yPos < (len(riskMap) - 1) and totalRiskMap[xPos][yPos + 1] == math.inf:
        viableNeighbor = True
        if riskMap[xPos][yPos + 1] < bestRisk:
            bestRisk = riskMap[xPos][yPos + 1]
            bestNeighbor = [xPos, (yPos + 1)]
    # If we found a viable neighbor, return the best one
    if viableNeighbor:
        return bestRisk, bestNeighbor
    else:
        return None, None

# Are we running against test or input?
runFlag = sys.argv[1]
riskMap = getData(runFlag)
# Starting point is (0,0) with a score of 0
initialPosition = [0, 0]
initialRisk = 0
# Initialize the overall risk map as being all infinite
totalRiskMap = []
for x in range(len(riskMap)):
    row = []
    for y in range(len(riskMap[0])):
        row.append(math.inf)
    totalRiskMap.append(row)
totalRiskMap[0][0] = initialRisk
# Get the seed values for our first move so our while loop will have something to work with
firstRisk, firstMove = getBestNeighbor(initialPosition, initialRisk)
endPosition = [len(riskMap) - 1, len(riskMap[0]) - 1]
possibleMoves = []
possibleMoves.append([initialPosition, initialRisk, firstRisk, firstMove])
# This is a textbook Djikstra's shortest path problem.  We'll maintain another 2d list of shortest encountered paths
# which is initialized as all infinite values.  Any time a new branch encounters a new cell, it will check its total
# distance traveled so far.  If it's less than the value in the path map, update the value in the path map and continue
# Iterate until the end position has a non-infinite value
while totalRiskMap[endPosition[0]][endPosition[1]] == math.inf:
    # Sort the list and we'll use the zero index as it will be the next best move
    possibleMoves.sort(key=lambda x: x[2])
    move = possibleMoves[0]
    # Update the risk map if the value is actually lower
    # There are situations where we can hit the same node twice from different directions, this is where we filter those out
    if move[2] < totalRiskMap[move[3][0]][move[3][1]]:
        totalRiskMap[move[3][0]][move[3][1]] = move[2]
        # If the new position has viable neighbors, add it to the list
        newRisk, newMove = getBestNeighbor(move[3], move[2])
        if newRisk != None and newMove != None:
            possibleMoves.append([move[3], move[2], (move[2] + newRisk), newMove])
    # Reevaluate our current node to see if it has any viable neighbors left
    updatedRisk, updatedMove = getBestNeighbor(move[0], move[1])
    # if it does, update it.  If not, remove it from the list
    if updatedRisk != None and updatedMove != None:
        possibleMoves[0] = [move[0], move[1], (move[1] + updatedRisk), updatedMove]
    else:
        del possibleMoves[0]
print("Final answer: " + str(totalRiskMap[endPosition[0]][endPosition[1]]))
print("Done!")

import sys
import pprint
import math

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()

    # We'll extract the input into a standard 2d list
    riskMap = []
    for line in lines:
        line = line.rstrip()
        riskLine = []
        for number in line:
            riskLine.append(int(number))
        riskMap.append(riskLine)
    return riskMap

# Recursive function for branching through entire risk map
def exploreRiskMap(position, totalRisk, stackDepth):
    global totalRiskMap
    global riskMap
    # We're running into the limits of the python interpreter here.  I'm pretty sure our solution won't be 1500 jumps long, so if we bottom out the stack just give up
    stackDepth = stackDepth + 1
    if stackDepth > 1497:
        return
    # Look in each direction for our position.  If the totalRisk + risk in that direction is less than what's in the totalMap
    # then update the total map and move in that direction.  Else do nothing
    # Look up
    if position[0] > 0:
        newRisk = totalRisk + riskMap[position[0] - 1][position[1]]
        if newRisk < totalRiskMap[position[0] - 1][position[1]]:
            #print("North old: " + str(totalRiskMap[position[0] - 1][position[1]]) + " new: " + str(newRisk))
            totalRiskMap[position[0] - 1][position[1]] = newRisk
            newPosition = [(position[0] - 1),position[1]]
            exploreRiskMap(newPosition, newRisk, stackDepth)
    # Look right
    if position[1] < (len(riskMap[0]) - 1):
        newRisk = totalRisk + riskMap[position[0]][position[1]+1]
        if newRisk < totalRiskMap[position[0]][position[1]+1]:
            #print("West old: " + str(totalRiskMap[position[0]][position[1]+1]) + " new: " + str(newRisk))
            totalRiskMap[position[0]][position[1]+1] = newRisk
            newPosition = [position[0],(position[1] + 1)]
            exploreRiskMap(newPosition, newRisk, stackDepth)
    # Look down
    if position[0] < (len(riskMap) - 1):
        newRisk = totalRisk + riskMap[position[0] + 1][position[1]]
        if newRisk < totalRiskMap[position[0] + 1][position[1]]:
            #print("South old: " + str(totalRiskMap[position[0] + 1][position[1]]) + " new: " + str(newRisk))
            totalRiskMap[position[0] + 1][position[1]] = newRisk
            newPosition = [(position[0] + 1),position[1]]
            exploreRiskMap(newPosition, newRisk, stackDepth)
    # Look left
    if position[1] > 0:
        newRisk = totalRisk + riskMap[position[0]][position[1] - 1]
        if newRisk < totalRiskMap[position[0]][position[1] - 1]:
            #print("East old: " + str(totalRiskMap[position[0]][position[1] - 1]) + " new: " + str(newRisk))
            totalRiskMap[position[0]][position[1] - 1] = newRisk
            newPosition = [position[0],(position[1] - 1)]
            exploreRiskMap(newPosition, newRisk, stackDepth)

# Are we running against test or input?
runFlag = sys.argv[1]
riskMap = getData(runFlag)
# Initialize our starting and desired end positions
initialPosition = [0, 0]
endPosition = [len(riskMap), len(riskMap[0])]
# This is a textbook Djikstra's shortest path problem.  We'll maintain another 2d list of shortest encountered paths
# which is initialized as all infinite values.  Any time a new branch encounters a new cell, it will check its total
# distance traveled so far.  If it's less than the value in the path map, update the value in the path map and continue
totalRiskMap = []
for x in range(len(riskMap)):
    row = []
    for y in range(len(riskMap[0])):
        row.append(math.inf)
    totalRiskMap.append(row)
totalRiskMap[0][0] = 0
# This will be a recursive method
sys.setrecursionlimit(1500)
exploreRiskMap(initialPosition, 0, 1)
print(str(totalRiskMap[len(riskMap) - 1][len(riskMap[0]) - 1]))
print("Done!")

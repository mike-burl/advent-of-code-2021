import sys
import pprint

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    # Insert all data into a two dimensional list which will act as our map
    lavaMap = []
    for line in lines:
        line = line.rstrip()
        digitList = []
        for digit in line:
            digitList.append(int(digit))
        lavaMap.append(digitList)
    return lavaMap

# Iterate over the lavamap and add up all of the lowpoints to find our total risk level
def calculateRiskLevel(lavaMap):
    riskLevel = 0
    for x, row in enumerate(lavaMap):
        for y, col in enumerate(row):
            if isLowPoint(x, y, lavaMap):
                riskLevel = riskLevel + lavaMap[x][y] + 1
    return riskLevel

# Check to see if the coordinates provided are a local minima
def isLowPoint(x, y, lavaMap):
    # If at any point we find a bordering value with a lower value, return false
    # North
    if x > 0 and lavaMap[x][y] > lavaMap[x - 1][y]:
        return False
    # South
    elif x < (len(lavaMap) - 1) and lavaMap[x][y] > lavaMap[x + 1][y]:
        return False
    elif y > 0 and lavaMap[x][y] > lavaMap[x][y - 1]:
        return False
    elif y < (len(lavaMap[x]) - 1) and lavaMap[x][y] > lavaMap[x][y + 1]:
        return False

    # Everything else is higher, return True
    return True

# Are we running against test or input?
runFlag = sys.argv[1]
lavaMap = getData(runFlag)
riskLevel = calculateRiskLevel(lavaMap)
print(str(riskLevel))
print("Done!")

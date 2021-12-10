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

# Iterate over the lavamap and find all the lowpoints
def findLowPoints(lavaMap):
    lowPoints = []
    for x, row in enumerate(lavaMap):
        for y, col in enumerate(row):
            if isLowPoint(x, y, lavaMap):
                lowPoints.append([x, y])
    return lowPoints

# Check to see if the coordinates provided are a local minima
def isLowPoint(x, y, lavaMap):
    # If at any point we find a bordering value with a lower value, return false
    # North
    if x > 0 and lavaMap[x][y] >= lavaMap[x - 1][y]:
        return False
    # South
    elif x < (len(lavaMap) - 1) and lavaMap[x][y] >= lavaMap[x + 1][y]:
        return False
    # West
    elif y > 0 and lavaMap[x][y] >= lavaMap[x][y - 1]:
        return False
    # East
    elif y < (len(lavaMap[x]) - 1) and lavaMap[x][y] >= lavaMap[x][y + 1]:
        return False

    # Everything else is higher, return True
    return True

# Expand each lowpoint to find the size of the basin
def calcBasinSizes(lavaMap, lowPoints):
    basinSizes = []
    for lowPoint in lowPoints:
        # We'll maintain a parallel map to see which cells we have and haven't visited already
        visitedPoints = [[False for i in range(len(lavaMap[0]))] for j in range(len(lavaMap))] 
        basinPoints = []
        basinPoints.append(lowPoint)
        visitedPoints[lowPoint[0]][lowPoint[1]] = True
        # We already know we start at a low point, so just expand outwards until we hit 9s
        for basinPoint in basinPoints:
            x = basinPoint[0]
            y = basinPoint[1]
            # Check all neighboring cells.  Only stop if it's already been visited, is 9, or is OoB
            # North
            if x > 0 and not visitedPoints[x - 1][y] and not lavaMap[x - 1][y] == 9:
                basinPoints.append([x-1,y])
                visitedPoints[x-1][y] = True
            # South
            if x < (len(lavaMap) - 1) and not visitedPoints[x + 1][y] and not lavaMap[x + 1][y] == 9:
                basinPoints.append([x+1,y])
                visitedPoints[x+1][y] = True
            # West
            if y > 0 and not visitedPoints[x][y - 1] and not lavaMap[x][y - 1] == 9:
                basinPoints.append([x,y-1])
                visitedPoints[x][y-1] = True
            # East
            if y < (len(lavaMap[x]) - 1) and not visitedPoints[x][y + 1] and not lavaMap[x][y + 1] ==9:
                basinPoints.append([x,y+1])
                visitedPoints[x][y+1] = True
        basinSizes.append(len(basinPoints))
    return basinSizes

# Sort the list then multiply the first three values together
def calcFinalAnswer(basinSizes):
    basinSizes.sort(reverse=True)
    finalAnswer = basinSizes[0] * basinSizes[1] * basinSizes[2]
    return finalAnswer

# Are we running against test or input?
runFlag = sys.argv[1]
lavaMap = getData(runFlag)
lowPoints = findLowPoints(lavaMap)
basinSizes = calcBasinSizes(lavaMap, lowPoints)
finalAnswer = calcFinalAnswer(basinSizes)

print(str(finalAnswer))
print("Done!")

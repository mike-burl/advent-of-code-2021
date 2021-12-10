import sys
import re
import pprint

# global variables
vents = []
ventGrid = []

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
        vents.append(line)

# Initialize the hydrothermal vent grid.  Find the largest X and Y values for our array
def initializeVentGrid():
    biggestX = 0
    biggestY = 0
    for plot in vents:
        if plot[0] > biggestX:
            biggestX = plot[0]
        if plot[1] > biggestY:
            biggestY = plot[1]
        if plot[2] > biggestX:
            biggestX = plot[2]
        if plot[3] > biggestY:
            biggestY = plot[3]
    # Initialize the whole grid as zero to start
    global ventGrid
    ventGrid = [ [0] * (biggestX + 1) for _ in range(biggestY + 1)]

# Plot out each vent if it's vertical or horizontal
def plotVents():
    for vent in vents:
        # Vertical vents
        if vent[0] == vent[2]:
            if vent[3] > vent[1]:
                for x in range(vent[3] - vent[1] + 1):
                    ventGrid[x + vent[1]][vent[0]] = ventGrid[x + vent[1]][vent[0]] + 1
            elif vent[1] > vent[3]:
                for x in range(vent[1] - vent[3] + 1):
                    ventGrid[x + vent[3]][vent[0]] = ventGrid[x + vent[3]][vent[0]] + 1
            else:
                ventGrid[vent[1]][vent[0]] = ventGrid[vent[1]][vent[0]] + 1
        # Horizontal vents
        elif vent[1] == vent[3]:
            if vent[2] > vent[0]:
                for x in range(vent[2] - vent[0] + 1):
                    ventGrid[vent[1]][x + vent[0]] = ventGrid[vent[1]][x + vent[0]] + 1
            elif vent[0] > vent[2]:
                for x in range(vent[0] - vent[2] + 1):
                    ventGrid[vent[1]][x + vent[2]] = ventGrid[vent[1]][x + vent[2]] + 1
            else:
                ventGrid[vent[1]][vent[0]] = ventGrid[vent[1]][vent[0]] + 1
        # Diagonal vents
        else:
            # First find out which direction the diagonal vent is going, then adjust the ventGrid
            # Southeast
            if vent[0] < vent[2] and vent[1] < vent[3]:
                for x in range(vent[2] - vent[0] + 1):
                    ventGrid[vent[1] + x][vent[0] + x] = ventGrid[vent[1] + x][vent[0] + x] + 1
            # Northeast
            elif vent[0] < vent[2] and vent[1] > vent[3]:
                for x in range(vent[2] - vent[0] + 1):
                    ventGrid[vent[1] - x][vent[0] + x] = ventGrid[vent[1] - x][vent[0] + x] + 1
            # Southwest
            elif vent[0] > vent[2] and vent[1] > vent[3]:
                for x in range(vent[0] - vent[2] + 1):
                    ventGrid[vent[3] + x][vent[2] + x] = ventGrid[vent[3] + x][vent[2] + x] + 1
            # Northwest
            else:
                for x in range(vent[0] - vent[2] + 1):
                    ventGrid[vent[3] - x][vent[2] + x] = ventGrid[vent[3] - x][vent[2] + x] + 1

# Sum up the number of cells with a vent count greater than one
def getFinalAnswer():
    cellCount = 0
    for ventLine in ventGrid:
        for cell in ventLine:
            if cell > 1:
                cellCount = cellCount + 1
    return cellCount

# Are we running against test or input?
runFlag = sys.argv[1]

getData(runFlag)

initializeVentGrid()

plotVents()

finalAnswer = getFinalAnswer()
print(str(finalAnswer))
print("Done!")

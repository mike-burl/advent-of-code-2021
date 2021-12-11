import sys
import pprint

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
        
    # Build the octogrid
    octoGrid = []
    for line in lines:
        line = line.rstrip()
        octoLine = []
        for octopus in line:
            octoLine.append(int(octopus))
        octoGrid.append(octoLine)
    return octoGrid

# This function will flash an octopus which will increment all of its neighbors by one
def flash(octoGrid, octopus):
    x = octopus[0]
    y = octopus[1]
    # Flash North
    if x > 0:
        octoGrid[x - 1][y] = octoGrid[x - 1][y] + 1
    # North-East
    if x > 0 and y < (len(octoGrid[x]) - 1):
        octoGrid[x - 1][y + 1] = octoGrid[x - 1][y + 1] + 1
    # East
    if y < (len(octoGrid[x]) - 1):
        octoGrid[x][y + 1] = octoGrid[x][y + 1] + 1
    # South-East
    if x < (len(octoGrid) - 1) and y < (len(octoGrid[x]) - 1):
        octoGrid[x + 1][y + 1] = octoGrid[x + 1][y + 1] + 1
    # South
    if x < (len(octoGrid) - 1):
        octoGrid[x + 1][y] = octoGrid[x + 1][y] + 1
    # South-West
    if x < (len(octoGrid) - 1) and y > 0:
        octoGrid[x + 1][y - 1] = octoGrid[x + 1][y - 1] + 1
    # West
    if y > 0:
        octoGrid[x][y - 1] = octoGrid[x][y - 1] + 1
    # North-West
    if x > 0 and y > 0:
        octoGrid[x - 1][y - 1] = octoGrid[x - 1][y - 1] + 1
    return octoGrid

# Are we running against test or input?
runFlag = sys.argv[1]
numSteps = int(sys.argv[2])
octoGrid = getData(runFlag)
totalFlashes = 0
numSteps = 0
stepFlashes = 0
# Run number of steps as user put in as argument
while stepFlashes != 100:
    stepFlashes = 0
    numSteps = numSteps + 1
    # First incrememnt the energy level of each octopus by 1
    for x, octoLine in enumerate(octoGrid):
        for y, octopus in enumerate(octoLine):
            octoGrid[x][y] = octopus + 1
    # iterate the flash while loop until we have a flash go by without any octopuses flashing
    anyFlash = True
    hasFlashed = {}
    while anyFlash:
        anyFlash = False
        flashList = []
        # Now check for all octopuses with an energy level greater than 9 and add it to the flashList
        for x, octoLine in enumerate(octoGrid):
            for y, octopus in enumerate(octoLine):
                flashKey = str(x) + str(y)
                if octoGrid[x][y] > 9 and flashKey not in hasFlashed:
                    flashList.append([x,y])
        # Flash all the octopuses in the flashList
        for octopus in flashList:
            anyFlash = True
            flashKey = str(octopus[0]) + str(octopus[1])
            hasFlashed[flashKey] = True
            octoGrid = flash(octoGrid, octopus)
    # Now that we're finally done flashing, reset all octopuses with an energy greater than nine
    for x, octoLine in enumerate(octoGrid):
        for y, octopus in enumerate(octoLine):
            if octoGrid[x][y] > 9:
                octoGrid[x][y] = 0
                totalFlashes = totalFlashes + 1
                stepFlashes = stepFlashes + 1
    # print("After step " + str(step + 1) + ":")
    # pprint.pprint(octoGrid)
print("Total steps: " + str(numSteps))
print("Total flashes: " + str(totalFlashes))
print("Done!")

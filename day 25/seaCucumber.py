import sys
import pprint

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    grid = []
    for line in lines:
        row = []
        line = line.rstrip()
        # We'll represent empty cells with a zero, east cucumbers with a 1, and south cucumbers with a 2
        for char in line:
            if char == '.':
                row.append(0)
            elif char == '>':
                row.append(1)
            elif char == 'v':
                row.append(2)
        grid.append(row)

    return grid

inputFlag = sys.argv[1]
cumberGrid = getData(inputFlag)
#pprint.pprint(cumberGrid)
numSteps = 0
anyMoves = True
skip = False
while anyMoves:
    anyMoves = False
    # Loop the East cucumbers 
    for i, row in enumerate(cumberGrid):
        for j, cell in enumerate(row):
            if skip:
                skip = False
                continue
            if cell == 1 and cumberGrid[i][(j+1)%len(row)] == 0:
                skip = True
                anyMoves = True
                cumberGrid[i][(j+1)%len(row)] = 1
                cumberGrid[i][j] = 0
    # Now loop the South
    skip = False
    for j in range(len(cumberGrid[i])):
        for i in range(len(cumberGrid)):
            if skip:
                skip = False
                continue
            if cumberGrid[i][j] == 2 and cumberGrid[(i+1)%len(cumberGrid)][j] == 0:
                skip = True
                anyMoves = True
                cumberGrid[(i+1)%len(cumberGrid)][j] = 2
                cumberGrid[i][j] = 0
    numSteps += 1
    print(numSteps)
print(numSteps)

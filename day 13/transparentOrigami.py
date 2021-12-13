import sys
import pprint

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    # We're not actually running any graph theory with this problem so we'll just store the coordinates in one list and the folds in another
    marks = []
    instructions = []
    for line in lines:
        line = line.rstrip()
        if line.startswith("fold"):
            fold = line.split(" ")[2]
            fold = fold.split("=")
            instructions.append([fold[0], int(fold[1])])
        elif len(line) > 2:
            coordinates = line.split(",")
            marks.append([int(coordinates[0]), int(coordinates[1])])
    return marks, instructions

# fold the mark list horizontally
def horizontalFold(marks, loc):
    for index, mark in enumerate(marks):
        if mark[1] > loc:
            marks[index][1] = loc - (marks[index][1] - loc)
    return marks

# fold the mark list vertically
def verticalFold(marks, loc):
    for index, mark in enumerate(marks):
        if mark[0] > loc:
            marks[index][0] = loc - (marks[index][0] - loc)
    return marks

# Remove duplicate marks
def removeDuplicates(marks):
    dedupedMarks = []
    markSet = set()
    # iterate over the marks and see if the key already exists.  if it does, skip it
    for mark in marks:
        key = str(mark[0]) + str(mark[1])
        if key not in markSet:
            markSet.add(key)
            dedupedMarks.append(mark)
    return dedupedMarks

# Create a grid of dots, iterate through our remaining coordinates to set the pixels, then print it so we see what the answer is
def printFinalAnswer(marks):
    greatestX = 0
    greatestY = 0
    for mark in marks:
        if mark[0] > greatestX:
            greatestX = mark[0]
        if mark[1] > greatestY:
            greatestY = mark[1]
    grid = []
    for Y in range(greatestY + 1):
        line = ""
        for X in range(greatestX + 1):
            line = line + '-'
        grid.append(line)
    for mark in marks:
        grid[mark[1]] = grid[mark[1]][:mark[0]] + '#' + grid[mark[1]][mark[0]+1:]
    pprint.pprint(grid)
    
# Are we running against test or input?
runFlag = sys.argv[1]
marks, instructions = getData(runFlag)
# sort the marks for easy deduping later
marks.sort(key=lambda x: x[0])
print("Starting with " + str(len(marks)) + " visible marks")
# For each fold in the instructions, iterate over the coordinates and modify each point should it land on the folded section of paper
for fold in instructions:
    axis = fold[0]
    loc = fold[1]
    if axis == 'y':
        marks = horizontalFold(marks, loc)
    else:
        marks = verticalFold(marks, loc)
    # Now remove duplicate marks
    marks = removeDuplicates(marks)
print("After folding, " + str(len(marks)) + " visible marks remain")
printFinalAnswer(marks)
print("Done!")

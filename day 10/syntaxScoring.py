import sys

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    # Add each line into a list which we'll work on
    codeLines = []
    for line in lines:
        line = line.rstrip()
        codeLines.append(line)
    return codeLines

# Are we running against test or input?
runFlag = sys.argv[1]
codeLines = getData(runFlag)
print("Done!")

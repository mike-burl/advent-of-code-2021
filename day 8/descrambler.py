import sys

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()

    # For each line we're going to split on the pipe to get the signal input vs. output
    # For now we're only interested in the output
    returnLines = []
    for line in lines:
        line = line.split("|")[1].strip().split(" ")
        returnLines.append(line)
    return returnLines

# Iterate over the output signals and find how many are unique
def getUniqueOutputCount(uniqueSignalCounts, outputSignals):
    uniqueOutputCount = 0
    for signal in outputSignals:
        for digit in signal:
            if len(digit) in uniqueSignalCounts:
                uniqueOutputCount = uniqueOutputCount + 1
    return uniqueOutputCount

# Are we running against test or input?
runFlag = sys.argv[1]

uniqueSignalCounts = [2, 4, 3, 7]
outputSignals = getData(runFlag)
uniqueOutputCount = getUniqueOutputCount(uniqueSignalCounts, outputSignals)
print(str(uniqueOutputCount))
print("Done!")

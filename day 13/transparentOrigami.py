import sys
import pprint

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()        
    paper = []
    instructions = []
    return paper, instructions

# Are we running against test or input?
runFlag = sys.argv[1]
paper, instructions = getData(runFlag)

print("Done!")

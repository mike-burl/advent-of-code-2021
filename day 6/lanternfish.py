import sys
import re
import pprint

# global variables
lanternfish = [0] * 9

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()

    # For each line we're going to remove all whitespace, split on '->', then split again on commas
    for line in lines:
        line = "".join(line.split())
        line = "".join(line.replace("->", ","))
        line = line.split(",")
        global lanternfish
        line = list(map(int, line))
        # Iterate through our starting lanternfish and increment their corresponding index
        for fishTimer in line:
            lanternfish[fishTimer] = lanternfish[fishTimer] + 1

# Simulate lanternfish growth for a certain amount of days
def simulateLanternfish(numDays):
    global lanternfish
    # Start our range on day one
    for dayNum in range(1, numDays + 1):
        newList = [0] * 9
        print("After " + str(dayNum) + " day: " + str(lanternfish))
        # We want to go down the list backwards to prevent losing any data
        for index in range(len(lanternfish) - 1, -1, -1):
            # if the index is eight, spawn new fish
            if index == 8:
                newList[index] = lanternfish[0]
            # if the index is six, we want to get both the resetting fish PLUS the ones with a timer of 7
            elif index == 6:
                newList[index] = lanternfish[0] + lanternfish[index + 1]
            else:
                newList[index] = lanternfish[index + 1]
        lanternfish = newList.copy()

    # Now get the final count of fish
    totalFishCount = 0
    for fishCount in lanternfish:
        totalFishCount = totalFishCount + fishCount
    return totalFishCount

# Are we running against test or input?
runFlag = sys.argv[1]

# How many days are we simulating?
numDays = int(sys.argv[2])

getData(runFlag)

numLanternFish = simulateLanternfish(numDays)

print(str(numLanternFish) + " fish!")

print("Done!")

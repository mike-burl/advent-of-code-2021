import sys
import re
import pprint

# global variables
lanternfish = []
newborns = []

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
        lanternfish = list(map(int, line))

# Simulate lanternfish growth for a certain amount of days
def simulateLanternfish(numDays):
    global lanternfish
    global newborns
    # Start our range on day one
    for dayNum in range(1, numDays + 1):
        # Simulate each lanternfish
        for index, fishTimer in enumerate(lanternfish):
            # if the fish timer is zero, spawn a new fish and reset its value to 6
            if fishTimer == 0:
                newborns.append(8)
                lanternfish[index] = 6
            else:
                lanternfish[index] = fishTimer - 1
        # If we have any newborns, append them and reset the list
        if len(newborns) > 0:
            lanternfish = lanternfish + newborns
            newborns.clear()

    return len(lanternfish)

# Are we running against test or input?
runFlag = sys.argv[1]

# How many days are we simulating?
numDays = int(sys.argv[2])

getData(runFlag)

print("Initial state: " + str(lanternfish))
print("Simulating " + str(numDays) + " days")

numLanternFish = simulateLanternfish(numDays)

print(str(numLanternFish) + " fish!")

print("Done!")

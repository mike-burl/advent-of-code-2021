# Convert binary list to integer
def convertBinaryStringToInt(line):
    value = 0
    for digit in line:
        value = (value << 1) | int(digit)
    return value

# Recursive function for determining the oxygen generator rating
def findOxygenRating(lines, index):
    # First check for our exit condition: if the index value is greater than the length of the line, or if we only have one value left, return
    if len(lines) == 1 or index > len(lines[0]):
        return lines
    
    # We only care about one position, so lists aren't necessary to store these values
    zeroCount = 0
    oneCount = 0
    
    for line in lines:
        if int(line[index]) == 0:
            zeroCount = zeroCount + 1
        else:
            oneCount = oneCount + 1

    # Determine which sublist to return
    # In the event of ties we'll default to 1
    listFlag = -1
    if zeroCount > oneCount:
        lineFlag = 0
    else:
        lineFlag = 1

    # Iterate through the lines and get the sublist based on the flag
    subList = []
    for line in lines:
        if int(line[index]) == lineFlag:
            subList.append(line)
    # Now we recurse downwards.  Increase the index by one and pass in the sublist
    index = index + 1
    return findOxygenRating(subList, index)
    
# Recursive function for determining the CO2 scrubber rating
def findCO2Rating(lines, index):
    # First check for our exit condition: if the index value is greater than the length of the line, or if we only have one value left, return
    if len(lines) == 1 or index > len(lines[0]):
        return lines
    
    # We only care about one position, so lists aren't necessary to store these values
    zeroCount = 0
    oneCount = 0
    
    for line in lines:
        if int(line[index]) == 0:
            zeroCount = zeroCount + 1
        else:
            oneCount = oneCount + 1

    # Determine which sublist to return
    # In the event of ties we'll default to 0
    listFlag = -1
    if zeroCount <= oneCount:
        lineFlag = 0
    else:
        lineFlag = 1

    # Iterate through the lines and get the sublist based on the flag
    subList = []
    for line in lines:
        if int(line[index]) == lineFlag:
            subList.append(line)
    # Now we recurse downwards.  Increase the index by one and pass in the sublist
    index = index + 1
    return findCO2Rating(subList, index)



# first we open the input file and extract all data

print('Opening input file...')

with open('input.txt') as file:
    lines = file.readlines()

# Strip out the carriage returns because ugh
for index, line in enumerate(lines):
    lines[index] = line.rstrip()

# Send the lines list to both the oxygen and CO2 recursive functions
oxygenRatingBinary = findOxygenRating(lines, 0)
co2RatingBinary = findCO2Rating(lines, 0)

oxygenRating = convertBinaryStringToInt(oxygenRatingBinary[0])
co2Rating = convertBinaryStringToInt(co2RatingBinary[0])

finalAnswer = oxygenRating * co2Rating

print("Final answer: " + str(finalAnswer))
print("Done!")

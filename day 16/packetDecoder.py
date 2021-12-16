import sys
import pprint
import math

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    message = lines[0].rstrip()
    return message

# Check to see if the message is an end signal
def isDone(message):
    return not(message) or message == '' or int(message) == 0

# Extract the literal values
def getLiteral(message):
    numStr = ''
    moreNums = True
    while moreNums:
        moreNums = (message[0]=='1')
        numStr += message[1:5]
        message = message[5:]
    return int(numStr,2), message

# Use this function to split the functionality between operator packets
def processOperator(message):
    lengthID = message[0]
    message = message[1:]
    if lengthID == '0':
        length = int(message[:15], 2)
        message = message[15:]
        subPackets = message[:length]
        # There's still more message potentially left, hold it here
        message = message[length:]
        while not isDone(subPackets):
            subPackets = processPacket(subPackets)
    if lengthID == '1':
        numSubPackets = int(message[:11], 2)
        message = message[11:]
        packetCount = 0
        while packetCount < numSubPackets:
            packetCount+=1
            message = processPacket(message)
    return message

# This will determine what kind of packet we're dealing with and split from there
# Version number will be placed into the version list right away
def processPacket(message):
    if isDone(message):
        return None
    # We have a valid packet, first thing's first, stash the version number
    versions.append(int(message[:3], 2))
    packetType = int(message[3:6], 2)
    message = message[6:]
    if packetType == 4:
        value, message = getLiteral(message)
        stack.append(value)
    else:
        stack.append("do this later")
        message = processOperator(message)
        stack.append("do this later")
    return message

# Are we running against test or input?
runFlag = sys.argv[1]
message = getData(runFlag)
binary = ""
finalBinary = ""
# Convert the hexadecimal message to binary
for char in message:
    binary = str("{0:04b}".format(int(char, 16)))
    finalBinary = finalBinary + binary
versions = []
stack = []
processPacket(finalBinary)
print(sum(versions))
print("Done!")

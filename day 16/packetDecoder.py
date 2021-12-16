import sys
from numpy import prod

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
        print("packetType: operator type 0 | message length remaining: " + str(len(message)) + " subPacketLength: " + str(length))
        # There's still more message potentially left, hold it here
        message = message[length:]
        while not isDone(subPackets):
            subPackets = processPacket(subPackets)
    if lengthID == '1':
        numSubPackets = int(message[:11], 2)
        message = message[11:]
        packetCount = 0
        print("packetType: operator type 1 | message length remaining: " + str(len(message)) + " numSubPackets: " + str(numSubPackets))
        while packetCount < numSubPackets:
            packetCount+=1
            message = processPacket(message)
    return message

# Execute what we have on the stack so far
def execute(stack):
    literals = []
    nextInput = stack.pop()
    while isinstance(nextInput, int):
        literals.append(nextInput)
        nextInput = stack.pop()
    # Once there's no numbers left in the stack, we know we have a function
    # Pass the numbers we've extracted to the function on the stack and return the result
    print("Executing function: " + str(nextInput) + " on values: " + str(literals))
    return nextInput(literals)

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
        print("packetType: literal | message length remaining: " + str(len(message)) + " value: " + str(value))
    else:
        stack.append(mathLookup[packetType])
        message = processOperator(message)
        stack.append(execute(stack))
    return message

# Are we running against test or input?
runFlag = sys.argv[1]
message = getData(runFlag)
binary = ""
finalBinary = ""
mathLookup = {0: sum,
         1: (lambda x: int(prod(x))),
         2: min,
         3: max,
         5: (lambda x: 1 if x[1]>x[0] else 0), 
         6: (lambda x: 1 if x[1]<x[0] else 0), 
         7: (lambda x: 1 if x[1]==x[0] else 0) 
         }
# Convert the hexadecimal message to binary
for char in message:
    binary = str("{0:04b}".format(int(char, 16)))
    finalBinary = finalBinary + binary
versions = []
stack = []
processPacket(finalBinary)
print(str(stack[0]))
print("Done!")

import sys
import pprint
import math

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    message = lines[0].rstrip()
    return message

# For now all we care about is version numbers.  First take out the version number, then find out if the packet is a literal or operator
# If it's a literal, we're done.  Just return the version number
# If it's an operator, split the packets out and recurse deeper.  Sum up the numbers they return, add it to the current packet, and return that
def analyzePacket(binaryString, currentPacket, targetPacket, aboveBitLength):
    #print("binary: " + binaryString)
    print("currentPacket: " + str(currentPacket) + " targetPacket: " + str(targetPacket) + " aboveBitLength: " + str(aboveBitLength))
    # Get the packet version and ID
    packetVersion = binaryString[0:3]
    packetTypeID = binaryString[3:6]
    # Convert the version and ID to integers
    packetVersion = int(packetVersion, 2)
    packetTypeID = int(packetTypeID, 2)
    print("packetVersion: " + str(packetVersion))
    print("packetTypeID: " + str(packetTypeID))
    if packetTypeID == 4:
        print("analyzing literal packet...")
        literalValueBinary = binaryString[6:]
        #print("literalValueBinary: " + literalValueBinary)
        groups = [literalValueBinary[i:i+5] for i in range(0, len(literalValueBinary), 5)]
        nextGroups = []
        #print("groups: " + str(groups))
        dropPackets = False
        for group in list(groups):
            if dropPackets:
                nextGroups.append(group)
                groups.remove(group)
                continue
            if group[0] == '0':
                dropPackets = True
        #print("groups after drop: " + str(groups))
        #print("nextGroups: " + str(nextGroups))
        binaryLiteral = ""
        for group in groups:
            binaryLiteral = binaryLiteral + group[1:]
        binaryDecimal = int(binaryLiteral, 2)
        print(binaryLiteral)
        print(str(binaryDecimal))
        nextPacketVersion = 0
        if len(nextGroups) > 0 and targetPacket == 0:
            nextBinaryLiteral = "".join(nextGroups)
            #print("nextBinaryLiteral: " + nextBinaryLiteral)
            nextPacketVersion = analyzePacket(nextBinaryLiteral, 0, 0, 0)
        elif len(nextGroups) > 0 and targetPacket > 0 and currentPacket < targetPacket:
            nextBinaryLiteral = "".join(nextGroups)
            #print("nextBinaryLiteral: " + nextBinaryLiteral)
            nextPacketVersion = analyzePacket(nextBinaryLiteral, (currentPacket + 1), targetPacket, 0)
        return packetVersion + nextPacketVersion
    else:
        print("analyzing operator packet...")
        lengthTypeID = binaryString[6:7]
        packetVersionSum = 0
        print("lengthTypeID: " + lengthTypeID)
        if lengthTypeID == '0':
            bitLength = binaryString[7:22]
            bitLength = int(bitLength, 2)
            print("bitLength: " + str(bitLength))
            packetVersionSum = packetVersionSum + analyzePacket(binaryString[22:(22 + bitLength)], 0, 0, bitLength) 
            if targetPacket > 0 and currentPacket < targetPacket:
                packetVersionSum = packetVersionSum + analyzePacket(binaryString[(22 + bitLength):], (currentPacket + 1), targetPacket, 0)
            elif (bitLength + 22) < aboveBitLength:
                packetVersionSum = packetVersionSum + analyzePacket(binaryString[(22 + bitLength):], 0, 0, (aboveBitLength - 22 - bitLength))
        else:
            numSubPackets = binaryString[7:18]
            numSubPackets = int(numSubPackets, 2)
            print("numSubPackets: " + str(numSubPackets))
            packetVersionSum = analyzePacket(binaryString[18:], 1, numSubPackets, 0)
        return packetVersion + packetVersionSum

# Are we running against test or input?
runFlag = sys.argv[1]
message = getData(runFlag)
binary = ""
finalBinary = ""
# Convert the hexadecimal message to binary
for char in message:
    binary = str("{0:04b}".format(int(char, 16)))
    finalBinary = finalBinary + binary
versionSum = analyzePacket(finalBinary, 0, 0, 0)
print("versionSum: " + str(versionSum))
print("Done!")

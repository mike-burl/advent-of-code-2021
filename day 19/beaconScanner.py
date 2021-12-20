import sys
import math

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    scanners = []
    scanner = []
    numBeacons = 0
    for line in lines:
        line = line.rstrip()
        if "---" in line:
            scanner = []
        elif len(line) == 0:
            scanners.append(scanner)
        else:
            numString = line.split(",")
            numMap = map(int, numString)
            scanner.append(list(numMap))
            numBeacons += int(len(numString)/3)
    print("Number of scanners: " + str(len(scanners)))
    return scanners, numBeacons

# For each beacon we'll find the distance to each other beacon, and sort them to get our 'fingerprint'
def buildFingerprints(srs):
    fingerprints = []
    for srsIndex, beacons in enumerate(srs):
        scannerCollection = []
        for bIndex, beacon in enumerate(beacons):
            fingerprint = []
            for nIndex, neighbor in enumerate(beacons):
                if bIndex == nIndex:
                    # Same beacon, skip this
                    continue
                x = abs(beacon[0] - neighbor[0])
                y = abs(beacon[1] - neighbor[1])
                z = abs(beacon[2] - neighbor[2])
                distance = math.hypot(x, y, z)
                fingerprint.append(distance)
            #fingerprint.sort()
            scannerCollection.append(set(fingerprint))
        fingerprints.append(scannerCollection)
    return fingerprints

# Loop through each set of probes and find where we have at least 11 intersections
def findIntersections(fingerprints):
    overlapCount = 0
    beaconSet = set({})
    for scannerIndex, scanner in enumerate(fingerprints):
        #print("----EVALUATING SCANNER " + str(scannerIndex) + "----")
        for beaconIndex, fingerprint in enumerate(scanner):
            for neighborIndex, neighbor in enumerate(fingerprints):
                if scannerIndex == neighborIndex:
                    continue
                for otherBeaconIndex, otherFingerprint in enumerate(neighbor):
                    coinc = len(set.intersection(fingerprint, otherFingerprint))
                    if coinc >= 11:
                        beaconKeyA = str(scannerIndex) + str(beaconIndex)
                        beaconKeyB = str(neighborIndex) + str(otherBeaconIndex)
                        if beaconKeyA not in beaconSet or beaconKeyB not in beaconSet:
                            overlapCount += 1
                            beaconSet.add(beaconKeyA)
                            beaconSet.add(beaconKeyB)
    return beaconSet, overlapCount
    
# Are we running against test or input?
runFlag = sys.argv[1]
scannerReports, numBeacons = getData(runFlag)
print("Number of beacon signals: " + str(numBeacons))
fingerprints = buildFingerprints(scannerReports)
intersections, overlapCount = findIntersections(fingerprints)
print("Number of unique beacons: " + str(numBeacons - overlapCount))

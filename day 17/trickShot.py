import sys

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    message = lines[0].rstrip()
    message = message[13:]
    coords = message.split(", ")
    xBounds = coords[0][2:].split("..")
    yBounds = coords[1][2:].split("..")
    xBounds = [int(num) for num in xBounds]
    yBounds = [int(num) for num in yBounds]
    return xBounds, yBounds

# Get the minimum viable x velocity
def getMinimumX(xPos):
    x = 1
    xPotential = 0
    xPosReached = False
    while not xPosReached:
        xPotential += x
        if xPotential > xPos:
            return x
        x += 1

# Determine if the coordinates are within our target area
def hitTarget(x, y, xBounds, yBounds):
    if x >= xBounds[0] and x <= xBounds[1] and y >= yBounds[0] and y <= yBounds[1]:
        return True
    else:
        return False
    
# Track the shot based on the x and y velocities and return the highest y value achieved
def trackShot(x, y, xBounds, yBounds):
    xVelocity = x
    yVelocity = y
    xPos = 0
    yPos = 0
    highestY = 0
    while xVelocity > 0 or (xPos <= xBounds[1] and yPos >= yBounds[0]):
        xPos += xVelocity
        yPos += yVelocity
        if yPos > highestY:
            highestY = yPos
        if xVelocity > 0:
            xVelocity -= 1
        yVelocity -= 1
        if hitTarget(xPos, yPos, xBounds, yBounds):
            return highestY
    # If we haven't hit the target by the time our path is exhausted, return zero; this was a miss
    return 0
        
# Are we running against test or input?
runFlag = sys.argv[1]
xBounds, yBounds = getData(runFlag)
xMin = getMinimumX(xBounds[0])
xMax = xBounds[1]
yMin = yBounds[0]
yMax = abs(yMin)
bestAir = 0
for x in range(xMin, xMax):
    for y in range(yMin, yMax):
        shotPeak = trackShot(x, y, xBounds, yBounds)
        if shotPeak > bestAir:
            bestAir = shotPeak
print("Best air achieved: " + str(bestAir))

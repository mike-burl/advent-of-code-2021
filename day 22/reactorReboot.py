import sys

class Cube:
    switch = 'off'
    xUp = 0
    xLo = 0
    yUp = 0
    yLo = 0
    zUp = 0
    zLo = 0
    def __init__(self, command, xUp, xLo, yUp, yLo, zUp, zLo):
        self.switch = command
        self.xUp = xUp
        self.xLo = xLo
        self.yUp = yUp
        self.yLo = yLo
        self.zUp = zUp
        self.zLo = zLo
        self.volume = (xUp + 1 - xLo) * (yUp + 1 - yLo) * (zUp + 1 - zLo)

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    cubes = []
    for line in lines:
        line = line.rstrip()
        onOff = line[:line.find(" ")]
        line = line[line.find(" ")+1:]
        coords = line.split(",")
        x = coords[0][2:]
        y = coords[1][2:]
        z = coords[2][2:]
        xLo = int(x[:x.find('.')])
        xUp = int(x[x.find('.')+2:])
        yLo = int(y[:y.find('.')])
        yUp = int(y[y.find('.')+2:])
        zLo = int(z[:z.find('.')])
        zUp = int(z[z.find('.')+2:])
        cube = Cube(onOff, xUp, xLo, yUp, yLo, zUp, zLo)
        cubes.append(cube)
    return cubes

# Split the cube into subCubes based on the overlap provided
def splitCube(cube, overlap):
    newCubes = []
    if cube.xLo != overlap.xLo:
        newCubes.append([cube.xLo, (overlap.xLo - 1), cube.yLo, cube.yUp, cube.zLo, cube.zUp])
    if cube.xUp != overlap.xUp:
        newCubes.append([(overlap.xUp + 1), cube.xUp, cube.yLo, cube.yUp, cube.zLo, cube.zUp])
    if cube.yLo != overlap.yLo:
        newCubes.append([overlap.xLo, overlap.xUp, cube.yLo, (overlap.yLo - 1), cube.zLo, cube.zUp])
    if cube.yUp != overlap.yUp:
        newCubes.append([overlap.xLo, overlap.xUp, (overlap.yUp + 1), cube.yUp, cube.zLo, cube.zUp])
    if cube.zLo != overlap.zLo:
        newCubes.append([overlap.xLo, overlap.xUp, overlap.yLo, overlap.yUp, cube.zLo, (overlap.zLo - 1)])
    if cube.zUp != overlap.zUp:
        newCubes.append([overlap.xLo, overlap.xUp, overlap.yLo, overlap.yUp, (overlap.zUp + 1), cube.zUp])

    cubeObjs = []
    for newCube in newCubes:
        newCubeObj = Cube("sub", newCube[1], newCube[0], newCube[3], newCube[2], newCube[5], newCube[4])
        cubeObjs.append(newCubeObj)
    return cubeObjs

# Find the overlap between the two cubes passed in
# Return the cube representing both regions
def getOverlap(cubeA, cubeB):
    if cubeA.xUp >= cubeB.xLo and cubeA.xLo <= cubeB.xUp and cubeA.yUp >= cubeB.yLo and cubeA.yLo <= cubeB.yUp and cubeA.zUp >= cubeB.zLo and cubeA.zLo <= cubeB.zUp:
        xLo = max(cubeA.xLo, cubeB.xLo)
        xUp = min(cubeA.xUp, cubeB.xUp)
        yLo = max(cubeA.yLo, cubeB.yLo)
        yUp = min(cubeA.yUp, cubeB.yUp)
        zLo = max(cubeA.zLo, cubeB.zLo)
        zUp = min(cubeA.zUp, cubeB.zUp)
        return Cube("sub", xUp, xLo, yUp, yLo, zUp, zLo)
    
# Run through each cell and apply the 
# Are we running against test or input?
runFlag = sys.argv[1]
cubes = getData(runFlag)
onCubes = []
for cube in cubes:
    # It's possible that our input will start with a group of off instructions
    # Skip these
    if len(onCubes) == 0:
        if cube.switch == 'on':
            onCubes.append(cube)
            continue
        else:
            continue
    else:
        offCubes = []
        if cube.switch == 'on':
            newCubes = [cube]
        else:
            newCubes = []
        for i, onCube in enumerate(onCubes):
            overlapCube = getOverlap(onCube, cube)
            if overlapCube is not None:
                offCubes.append(i)
                newCubes += splitCube(onCube, overlapCube)
        for i in reversed(offCubes):
            del onCubes[i]
        onCubes += newCubes
finalVolume = 0
for onCube in onCubes:
    finalVolume += onCube.volume
print(finalVolume)

import sys
import pprint

class MyList(list):
    def get(self, index, default=None):
        return self[index] if len(self) > index and index >= 0 else default
    
# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    image = MyList([])
    algo = []

    algoLine = lines[0].rstrip()
    for char in algoLine:
        if char == '.':
            algo.append('0')
        else:
            algo.append('1')
    for line in lines[2:]:
        row = MyList([])
        line = line.rstrip()
        for char in line:
            if char == '.':
                row.append('0')
            else:
                row.append('1')
        image.append(row)
    return algo, image

# Add a blank row in each direction for us to expand into
def expandImage(image):
    dimension = len(image)
    blankRow = MyList(['0'] * (dimension + 2))
    newImage = MyList([])
    newImage.append(blankRow)
    for row in image:
        newRow = MyList(['0'] + row + ['0'])
        newImage.append(newRow)
    blankRow = MyList(['0'] * (dimension + 2))
    newImage.append(blankRow)
    return newImage

neighborTuples = ([-1, -1],[-1, 0],[-1, 1],[0, -1],[0, 1],[1, -1],[1, 0],[1, 1])
def getNeighborString(x, y, image):
    returnString = image.get(y-1, MyList(['0'])).get(x-1, '0')
    returnString += image.get(y-1, MyList(['0'])).get(x, '0')
    returnString += image.get(y-1, MyList(['0'])).get(x+1, '0')
    returnString += image.get(y, MyList(['0'])).get(x-1, '0')
    returnString += image.get(y, MyList(['0'])).get(x, '0')
    returnString += image.get(y, MyList(['0'])).get(x+1, '0')
    returnString += image.get(y+1, MyList(['0'])).get(x-1, '0')
    returnString += image.get(y+1, MyList(['0'])).get(x, '0')
    returnString += image.get(y+1, MyList(['0'])).get(x+1, '0')
    return returnString
    
# Take the coordinates and generate the new enhanced cell
def enhanceCell(x, y, image, algo):
    lookupString = getNeighborString(x, y, image)
    lookupInt = int(lookupString, 2)
    newCell = algo[lookupInt]
    return newCell

# Iterate over each cell to generate the new enhanced image by applying the algo to it
def enhanceImage(image, algo):
    enhancedImage = MyList([])
    for y, row in enumerate(image):
        enhancedRow = MyList([])
        for x, cell in enumerate(row):
            newCell = enhanceCell(x, y, image, algo)
            enhancedRow.append(newCell)
        enhancedImage.append(enhancedRow)
    return enhancedImage
            
# Run through each cell and apply the 
# Are we running against test or input?
runFlag = sys.argv[1]
numSteps = int(sys.argv[2])
algo, image = getData(runFlag)
#pprint.pprint(image)
for step in range(numSteps):
    image = expandImage(image)
    image = enhanceImage(image, algo)
    #pprint.pprint(image)
litPixels = 0
for row in image:
    for cell in row:
        if cell == '1':
            litPixels += 1
print(str(litPixels))

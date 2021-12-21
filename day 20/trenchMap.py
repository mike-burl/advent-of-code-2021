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
def expandImage(image, infinite):
    dimension = len(image)
    blankRow = MyList([infinite] * (dimension + 2))
    newImage = MyList([])
    newImage.append(blankRow)
    for row in image:
        newRow = MyList([infinite] + row + [infinite])
        newImage.append(newRow)
    blankRow = MyList([infinite] * (dimension + 2))
    newImage.append(blankRow)
    return newImage

def getNeighborString(x, y, image, infinite):
    returnString = image.get(y-1, MyList([infinite])).get(x-1, infinite)
    returnString += image.get(y-1, MyList([infinite])).get(x, infinite)
    returnString += image.get(y-1, MyList([infinite])).get(x+1, infinite)
    returnString += image.get(y, MyList([infinite])).get(x-1, infinite)
    returnString += image.get(y, MyList([infinite])).get(x, infinite)
    returnString += image.get(y, MyList([infinite])).get(x+1, infinite)
    returnString += image.get(y+1, MyList([infinite])).get(x-1, infinite)
    returnString += image.get(y+1, MyList([infinite])).get(x, infinite)
    returnString += image.get(y+1, MyList([infinite])).get(x+1, infinite)
    return returnString
    
# Take the coordinates and generate the new enhanced cell
def enhanceCell(x, y, image, algo, infinite):
    lookupString = getNeighborString(x, y, image, infinite)
    lookupInt = int(lookupString, 2)
    newCell = algo[lookupInt]
    return newCell

# Iterate over each cell to generate the new enhanced image by applying the algo to it
def enhanceImage(image, algo, infinite):
    enhancedImage = MyList([])
    for y, row in enumerate(image):
        enhancedRow = MyList([])
        for x, cell in enumerate(row):
            newCell = enhanceCell(x, y, image, algo, infinite)
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
    infinite = '0' if step % 2 == 0 else '1'
    image = expandImage(image, infinite)
    image = enhanceImage(image, algo, infinite)
    #pprint.pprint(image)
litPixels = 0
for row in image:
    for cell in row:
        if cell == '1':
            litPixels += 1
print(str(litPixels))

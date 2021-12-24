import pprint

class StateList:
    states = []
    visited = {}
    toVisit = {}
    numEvals = 0
    def binarySearch(self, arr, low, high, x):
        mid = (high + low) // 2
        if high >= low:
            if arr[mid][0] == x:
                return mid
            elif arr[mid][0] > x:
                return self.binarySearch(arr, low, mid - 1, x)
            else:
                return self.binarySearch(arr, mid + 1, high, x)
        else:
            return mid + 1
        
    def addState(self, newState):
        self.numEvals += 1
        key = newState[1]
        val = newState[0]
        if key in self.visited:
            # We've already visited this node.  Skip it
            return
        elif key in self.toVisit and val < self.toVisit[key]:
            # We've found a better path to this key, update it
            self.updateState(newState)
        elif key in self.toVisit and val >= self.toVisit[key]:
            # This is a worse path, ignore this
            return
        else:
            # This has neither been visited or is to be visited.  Add it
            self.insertState(newState)

    def updateState(self, newState):
        # First find the old value and delete it
        oldVal = self.toVisit[newState[1]]
        deleteIndex = self.binarySearch(self.states, 0, len(self.states)-1, oldVal)
        if self.states[deleteIndex][1] == newState[1]:
            del self.states[deleteIndex]
        else:
            # Search up
            hit = False
            for i in range(deleteIndex, len(self.states)-1):
                # If we can't find it moving upwards, break
                if self.states[i][0] > oldVal:
                    break
                elif self.states[i][1] == newState[1]:
                    del self.states[i]
                    hit = True
                    break
            if not hit:
                for i in range(deleteIndex, -1, -1):
                    # If we can't find it moving downwards, break
                    if self.states[i][0] < oldVal:
                        break #This technically should never happen
                    elif self.states[i][1] == newState[1]:
                        del self.states[i]
                        break
        # Now insert the new value
        self.insertState(newState)
            
    def insertState(self, newState):
        self.toVisit[newState[1]] = newState[0]
        insertIndex = self.binarySearch(self.states, 0, len(self.states)-1, newState[0])
        self.states.insert(insertIndex, newState)

    def getState(self):
        nextState = self.states.pop(0)
        del self.toVisit[nextState[1]]
        self.visited[nextState[1]] = nextState[0]
        return nextState

    def toString(self):
        for state in self.states:
            print(str(state))

class Room:
    def __init__(self, prawnA, prawnB, prawnC, prawnD):
        self.occupants = [prawnA, prawnB, prawnC, prawnD]

class Hallway:
    doors = [3, 5, 7, 9]
    def __init__(self, hallwayLength, doorA, doorB, doorC, doorD):
        self.hall = ['E'] * hallwayLength
        self.doors = []
        self.doors.append(Room(doorA[0], doorA[1], doorA[2], doorA[3]))
        self.doors.append(Room(doorB[0], doorB[1], doorB[2], doorB[3]))
        self.doors.append(Room(doorC[0], doorC[1], doorC[2], doorC[3]))
        self.doors.append(Room(doorD[0], doorD[1], doorD[2], doorD[3]))

    def getRoomStrings(self):
        returnString = ''
        for room in self.doors:
            returnString += ''.join(room.occupants)
        return returnString

    def toString(self):
        return ''.join(self.hall) + ":" + self.getRoomStrings()

def getHallwayString(state):
    return state[:11]

def getDoorStrings(state):
    return [state[12:16], state[16:20], state[20:24], state[24:28]]

def buildDoorStrings(doors):
    newDoorStrings = ''
    for door in doors:
        newDoorStrings += door
    return newDoorStrings

# Determine if this is a legal move for the fish
def isLegalHallwayToDoor(fish, dI, door):
    # First see if the fish even wants to go through this door
    if fish == 'A' and dI != 0:
        return False
    elif fish == 'B' and dI != 1:
        return False
    elif fish == 'C' and dI != 2:
        return False
    elif fish == 'D' and dI != 3:
        return False
    # Now see that all the occupants are the same type of fish
    for char in door:
        if char == 'E':
            continue
        elif char != fish:
            return False
    # If we get this far they should be cool with it
    return True

# Get the length of the path from the hallway to the door
# Return -1 if the path is blocked
def pathToDoor(hallway, hI, dI):
    # This is the section of hallway we're concerned with
    goalDoor = 2 + (dI * 2)
    subString = hallway[goalDoor:hI] if hI > goalDoor else hallway[hI+1:goalDoor+1]
    # Make sure it's all empty
    clearPath = True
    for char in subString:
        if char != 'E':
            clearPath = False
            break
    if clearPath:
        return len(subString)
    else:
        return -1
    
moveCosts = {'A':1, 'B':10, 'C':100, 'D':1000}
# Place the hallway fish into its room and calculate the cost it took
def moveHallwayToDoor(hallway, hI, doors, dI, pathCost, cost):
    fish = hallway[hI]
    newHallway = hallway[:hI] + 'E' + hallway[hI + 1:]
    hallwayCost = moveCosts[fish] * pathCost
    door = doors[dI]
    # Start as far back as we can and move forwards
    if door[3] == 'E':
        totalCost = cost + hallwayCost + (moveCosts[fish] * 4)
        newDoor = ['E', 'E', 'E', fish]
        states.addState([totalCost, newHallway + ":" + buildDoorStrings(doors[:dI] + newDoor + doors[dI+1:])])
    elif door[2] == 'E':
        totalCost = cost + hallwayCost + (moveCosts[fish] * 3)
        newDoor = ['E', 'E', fish, fish]
        states.addState([totalCost, newHallway + ":" + buildDoorStrings(doors[:dI] + newDoor + doors[dI+1:])])
    elif door[1] == 'E':
        totalCost = cost + hallwayCost + (moveCosts[fish] * 2)
        newDoor = ['E', fish, fish, fish]
        states.addState([totalCost, newHallway + ":" + buildDoorStrings(doors[:dI] + newDoor + doors[dI+1:])])
    elif door[0] == 'E':
        totalCost = cost + hallwayCost + moveCosts[fish]
        newDoor = [fish, fish, fish, fish]
        states.addState([totalCost, newHallway + ":" + buildDoorStrings(doors[:dI] + newDoor + doors[dI+1:])])
    
# Generate moves for a hallway position to a door
def hallwayToDoor(hallway, hI, doors, dI, cost):
    door = doors[dI]
    # First see if the door is even available
    if door[0] != 'E':
        return
    # If it is, check to see if the door is valid
    fish = hallway[hI]
    if not isLegalHallwayToDoor(fish, dI, door):
        return
    pathCost = pathToDoor(hallway, hI, dI)
    if pathCost > 0:
        # The door is valid and available, let's goooo!
        moveHallwayToDoor(hallway, hI, doors, dI, pathCost, cost)
    else:
        return
    
# Find all possible moves from the hallway and return them along with their associated costs
def getHallwayMoves(state, cost):
    hallway = getHallwayString(state)
    doors = getDoorStrings(state)
    for hI, char in enumerate(hallway):
        if char != 'E':
            for dI, door in enumerate(doors):
                hallwayToDoor(hallway, hI, doors, dI, cost)

# Pop the top fish out of a door and return the new string
def popFish(door):
    newDoor = []
    fishPopped = False
    for char in door:
        if char == 'E':
            newDoor.append(char)
        elif not fishPopped:
            newDoor.append('E')
            fishPopped = True
        else:
            newDoor.append(char)
    return newDoor

illegalRooms = [2, 4, 6, 8]
# Generate all possible moves to the left and right of the door
def getDoorToHallway(hallway, doors, dI, fish, cost):
    originDoorIndex = 2 + (dI * 2)
    # Generate possibilities to the left
    for i in range(originDoorIndex, -1, -1):
        if hallway[i] == 'E':
            if i not in illegalRooms:
                newHallway = hallway[:i] + fish + hallway[i+1:]
                newDoor = popFish(doors[dI])
                totalCost = cost + ((originDoorIndex - i + 1) * moveCosts[fish])
                states.addState([totalCost, newHallway + ":" + buildDoorStrings(doors[:dI] + newDoor + doors[dI+1:])])
        else:
            break
    # Now go right
    for i in range(originDoorIndex, len(hallway)):
        if hallway[i] == 'E':
            if (i) not in illegalRooms:
                newHallway = hallway[:i] + fish + hallway[i+1:]
                newDoor = popFish(doors[dI])
                totalCost = cost + ((i - (originDoorIndex) + 1) * moveCosts[fish])
                states.addState([totalCost, newHallway + ":" + buildDoorStrings(doors[:dI] + newDoor + doors[dI+1:])])
        else:
            break
    
# Generate all possible moves from the given door
def generateDoorMoves(state, dI, doors, cost):
    hallway = getHallwayString(state)
    # is the first, second, third, or fourth position moving
    if doors[dI][0] != 'E':
        getDoorToHallway(hallway, doors, dI, doors[dI][0], cost)
    elif doors[dI][1] != 'E':
        getDoorToHallway(hallway, doors, dI, doors[dI][1], cost + moveCosts[doors[dI][1]])
    elif doors[dI][2] != 'E':
        getDoorToHallway(hallway, doors, dI, doors[dI][2], cost + (moveCosts[doors[dI][2]]*2))
    else:
        getDoorToHallway(hallway, doors, dI, doors[dI][3], cost + (moveCosts[doors[dI][3]]*3))
        

# Check if all fish in the door are happy with where they're at
def doorComplete(door, dI):
    doorSet = ''.join(set(door))
    # If we have three or more characters, we have some unhappy neighbors
    if len(doorSet) >= 3:
        return False
    # If we have two, check to see if the occupants want to be there
    elif len(doorSet) == 2:
        # See if the other character is empty, if it isn't then just return false
        if 'E' not in doorSet:
            return False
        # Let's see what the other character is and if it belongs there  
        elif dI == 0 and 'A' in doorSet:
            return True
        elif dI == 1 and 'B' in doorSet:
            return True
        elif dI == 2 and 'C' in doorSet:
            return True
        elif dI == 3 and 'D' in doorSet:
            return True
        else:
            return False
    # If we get here we just need to see what's in it
    else:
        # It's an empty room, we can't use this to generate moves
        if 'E' in doorSet:
            return True
        elif dI == 0 and 'A' in doorSet:
            return True
        elif dI == 1 and 'B' in doorSet:
            return True
        elif dI == 2 and 'C' in doorSet:
            return True
        elif dI == 3 and 'D' in doorSet:
            return True
        else:
            return False

# Get all possible moves originating from each of the doors
def getDoorMoves(state, cost):
    doors = getDoorStrings(state)
    for dI, door in enumerate(doors):
        if not doorComplete(door, dI):
            generateDoorMoves(state, dI, doors, cost)
            
# Given the state, build a list for all possible moves with their associated costs
def getPossibleMoves(state, cost):
    getHallwayMoves(state, cost)
    getDoorMoves(state, cost)

# Define our hallway
hallway = Hallway(11, ['D', 'D', 'D', 'C'], ['A', 'C', 'B', 'A'], ['C', 'B', 'A', 'B'], ['D', 'A', 'C', 'B'])
endState = 'EEEEEEEEEEE:AAAABBBBCCCCDDDD'
endStateReached = False
states = StateList()
# We want to cache the initial state so we don't hit it again
startingState = hallway.toString()
states.addState([0, startingState])
while not endStateReached:
    nextMove = states.getState()
    if nextMove[1] == endState:
        endStateReached = True
        break
    getPossibleMoves(nextMove[1], nextMove[0])
print(str(nextMove))
print("# of evaluations: " + str(states.numEvals))

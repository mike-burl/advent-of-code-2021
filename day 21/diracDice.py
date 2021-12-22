import sys

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    p1Pos = int(lines[0].rstrip().split(":")[1])
    p2Pos = int(lines[1].rstrip().split(":")[1])
    return p1Pos, p2Pos

# Roll the dice and return the new position and score
def rollDie(pPos, pScore, roll):
    pPos = (pPos + roll) % 10
    if pPos == 0:
        pScore += 10
    else:
        pScore += pPos
    return pPos, pScore

# Recursive function with a cache.  First check out cache to see if this game state has been encountered
# If it has, just return the results
# If it hasn't, we need to simulate it still
def quantumDice(p1Pos, p1Score, p2Pos, p2Score, p1Turn):
    targetScore = 21
    # The mirror state is no different from our current state, just with the player outcomes reversed
    gameState = str(p1Turn) + ":" + str(p1Pos) + ":" + str(p1Score) + ":" + str(p2Pos) + ":" + str(p2Score)
    #print(gameState)
    printOut = gameState
    mirrorState = str(not p1Turn) + str(p2Pos) + str(p2Score) + str(p1Pos) + str(p1Score)
    if gameState in realityCache:
        print("We've already been here: " + gameState)
        return realityCache[gameState]
    elif mirrorState in realityCache:
        mirrorState = realityCache[mirrorState]
        print("This place feels familiar")
        return [mirrorState[1], mirrorState[0]]
    else:
        # This situation hasn't been encountered yet
        # Determine which player's turn it is
        subState = [0, 0]
        if p1Turn:
            # Roll one
            p1R1Pos, p1R1Score = rollDie(p1Pos, p1Score, 1)
            if p1R1Score >= targetScore:
                subState[0] += 1
            else:
                tempState = quantumDice(p1R1Pos, p1R1Score, p2Pos, p2Score, False)
                subState[0] += tempState[0]
                subState[1] += tempState[1]
            #printOut = printOut + "||" + str(subState)
            # Roll Two
            p1R2Pos, p1R2Score = rollDie(p1Pos, p1Score, 2)
            if p1R2Score >= targetScore:
                subState[0] += 1
            else:
                tempState = quantumDice(p1R2Pos, p1R2Score, p2Pos, p2Score, False)
                subState[0] += tempState[0]
                subState[1] += tempState[1]
            #printOut = printOut + "||" + str(subState)
            # Roll Three
            p1R3Pos, p1R3Score = rollDie(p1Pos, p1Score, 3)
            if p1R3Score >= targetScore:
                subState[0] += 1
            else:
                tempState = quantumDice(p1R3Pos, p1R3Score, p2Pos, p2Score, False)
                subState[0] += tempState[0]
                subState[1] += tempState[1]
            #printOut = printOut + "||" + str(subState)
        else:
            # Roll one
            p2R1Pos, p2R1Score = rollDie(p2Pos, p2Score, 1)
            if p2R1Score >= targetScore:
                subState[1] += 1
            else:
                tempState = quantumDice(p1Pos, p1Score, p2R1Pos, p2R1Score, True)
                subState[0] += tempState[0]
                subState[1] += tempState[1]
            #printOut = printOut + "||" + str(subState)
            # Roll Two
            p2R2Pos, p2R2Score = rollDie(p2Pos, p2Score, 2)
            if p2R2Score >= targetScore:
                subState[1] += 1
            else:
                tempState = quantumDice(p1Pos, p1Score, p2R2Pos, p2R2Score, True)
                subState[0] += tempState[0]
                subState[1] += tempState[1]
            #printOut = printOut + "||" + str(subState)
            # Roll Three
            p2R3Pos, p2R3Score = rollDie(p2Pos, p2Score, 3)
            if p2R3Score >= targetScore:
                subState[1] += 1
            else:
                tempState = quantumDice(p1Pos, p1Score, p2R3Pos, p2R3Score, True)
                subState[0] += tempState[0]
                subState[1] += tempState[1]
            #printOut = printOut + "||" + str(subState)
        #print(printOut)
        realityCache[gameState] = subState
        return subState

# Run through each cell and apply the 
# Are we running against test or input?
runFlag = sys.argv[1]
p1Pos, p2Pos = getData(runFlag)
realityCache = {}
wins = quantumDice(p1Pos, 0, p2Pos, 0, True)
print(str(wins))

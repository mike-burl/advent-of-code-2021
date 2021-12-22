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

# We don't actually care about rolling the dice three times, all we care about is the final outcome
# This is the distribution of possible rolls for each turn
quantumCombos = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
# Recursive function with a cache.  First check out cache to see if this game state has been encountered
# If it has, just return the results
# If it hasn't, we need to simulate it still
def quantumDice(p1Pos, p1Score, p2Pos, p2Score, p1Turn):
    targetScore = 21
    # The mirror state is no different from our current state, just with the player outcomes reversed
    gameState = str(p1Turn) + ":" + str(p1Pos) + ":" + str(p1Score) + ":" + str(p2Pos) + ":" + str(p2Score)
    mirrorState = str(not p1Turn) + str(p2Pos) + str(p2Score) + str(p1Pos) + str(p1Score)
    if gameState in realityCache:
        return realityCache[gameState]
    elif mirrorState in realityCache:
        mirrorState = realityCache[mirrorState]
        return [mirrorState[1], mirrorState[0]]
    else:
        # This situation hasn't been encountered yet
        # Determine which player's turn it is
        subState = [0, 0]
        if p1Turn:
            for combo in quantumCombos:
                p1NewPos, p1NewScore = rollDie(p1Pos, p1Score, combo)
                if p1NewScore >= targetScore:
                    subState[0] += quantumCombos[combo]
                else:
                    tempState = quantumDice(p1NewPos, p1NewScore, p2Pos, p2Score, False)
                    subState[0] += (tempState[0] * quantumCombos[combo])
                    subState[1] += (tempState[1] * quantumCombos[combo])
        else:
            for combo in quantumCombos:
                p2NewPos, p2NewScore = rollDie(p2Pos, p2Score, combo)
                if p2NewScore >= targetScore:
                    subState[1] += quantumCombos[combo]
                else:
                    tempState = quantumDice(p1Pos, p1Score, p2NewPos, p2NewScore, True)
                    subState[0] += (tempState[0] * quantumCombos[combo])
                    subState[1] += (tempState[1] * quantumCombos[combo])
        realityCache[gameState] = subState
        return subState

# Run through each cell and apply the 
# Are we running against test or input?
runFlag = sys.argv[1]
p1Pos, p2Pos = getData(runFlag)
realityCache = {}
wins = quantumDice(p1Pos, 0, p2Pos, 0, True)
print(str(wins))

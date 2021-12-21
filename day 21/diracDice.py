import sys

class DeterministicDice:
    currentValue = 0
    numRolls = 0
    def rollDice(self):
        self.numRolls += 1
        self.currentValue += 1
        if self.currentValue == 101:
            self.currentValue = 1
        return self.currentValue

class Player:
    pos = 0
    score = 0
    def __init__(self, position):
        self.pos = position
    def move(self, roll):
        self.pos = (self.pos + roll) % 10
        if self.pos == 0:
            self.score += 10
        else:
            self.score += self.pos
        return self.score
    def roll(self, dice):
        nextMove = dice.rollDice() + dice.rollDice() + dice.rollDice()
        return self.move(nextMove)

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    p1Pos = int(lines[0].rstrip().split(":")[1])
    p2Pos = int(lines[1].rstrip().split(":")[1])
    return p1Pos, p2Pos

# Run through each cell and apply the 
# Are we running against test or input?
runFlag = sys.argv[1]
p1Pos, p2Pos = getData(runFlag)
scoreDict = {}
dice = DeterministicDice()
p1 = Player(p1Pos)
p2 = Player(p2Pos)
while p1.roll(dice) < 1000 and p2.roll(dice) < 1000:
    pass
print(str(p1.score))
print(str(p2.score))
print(str(dice.numRolls))
print(str(p2.score * dice.numRolls))

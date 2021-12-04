import sys
import re
import pprint

# global variables
width = 5
height = 5
draws = []
boards = []

# Keep the indexes of all winning boards so we can skip them for efficiency reasons and to also keep track of when we've found the ULTIMATE LOSER
winningBoards = []

# Open the data file and extract our data
def getData(runFlag):
    print('Opening input file...')

    with open(runFlag + '.txt') as file:
        lines = file.readlines()

    # The first line is the numbers drawn
    global draws
    draws = lines[0].rstrip().split(",")

    # All following lines are the bingo boards
    board = []
    row = []
    rowsConsumed = 0
    for index, line in enumerate(lines[2:]):
        if len(line) > 1:
            # We have a line with real information in it. Scrub out double spaces, split into a list, then append it to the board
            line = re.sub(' +', ' ', line)
            row = line.strip().split(" ")
            board.append(row)
            rowsConsumed = rowsConsumed + 1

            # Now check to see if we've consumed a full board
            if rowsConsumed == height:
                boards.append(board)
                board = []
                row = []
                rowsConsumed = 0

# Check the x and y axis of the board to see if we have a bingo in either direction
def checkBingo(boardNum, x, y):
    board = boards[boardNum]
    # x-axis check
    hitCount = 0
    for xIter in range(5):
        if board[y][xIter] == 'X':
            hitCount = hitCount + 1
            if hitCount == 5:
                #Bingo!  Add the boardNum to the winner's list.  If it's the last board, we'll return True.  Otherwise we'll pretend the game is still going
                winningBoards.append(boardNum)
                if len(winningBoards) < len(boards):
                    return False
                else:
                    return True
        else:
            # Miss! Reset the hit counter and break the loop
            hitCount = 0
            break
    # y-axis check
    for yIter in range(5):
        if board[yIter][x] == 'X':
            hitCount = hitCount + 1
            if hitCount == 5:
                #Bingo!  Add the boardNum to the winner's list.  If it's the last board, we'll return True.  Otherwise we'll pretend the game is still going
                winningBoards.append(boardNum)
                if len(winningBoards) < len(boards):
                    return False
                else:
                    return True
        else:
            # Miss! There's nothing left to do so return False
            return False

# Check the board to see if the number drawn gives us a bingo
def checkBoard(boardNum, draw, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if draw == cell:
                # We have a hit! Mark the board then check for a bingo!
                boards[boardNum][y][x] = 'X'
                hasWon = checkBingo(boardNum, x, y)
                if hasWon:
                    return "Bingo"
                
# Play bingo
def playBingo(draws, boards):
    # Iterate through our draws and pass the number to each bingo board
    for draw in draws:
        numSkips = 0
        for boardNum, board in enumerate(boards):
            # Check to see if the board has already won.  If it has, skip it
            if boardNum in winningBoards:
                numSkips = numSkips + 1
                continue
            loseFlag = checkBoard(boardNum, draw, board)
            if loseFlag == "Bingo":
                return draw, board
    # We shouldn't be able to reach this line
    return None, None

# Calculate the final answer
def calculateFinalAnswer(winningNumber, losingBoard):
    # First find the sum of all unmarked numbers
    sum = 0
    for row in losingBoard:
        for cell in row:
            if cell != "X":
                sum = sum + int(cell)

    # Now multiply the sum with the winning number
    return sum * int(winningNumber)
# Are we running against test or input?
runFlag = sys.argv[1]

getData(runFlag)

winningNumber, losingBoard = playBingo(draws, boards)
print("Winning number: " + winningNumber)
finalAnswer = calculateFinalAnswer(winningNumber, losingBoard)
print("Final answer: " + str(finalAnswer))
print("Done!")

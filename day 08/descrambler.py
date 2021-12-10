import sys
import pprint

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    # For each line we're going to split on the pipe to get the signal input vs. output
    # For now we're only interested in the output
    outputLines = []
    tenPanel = []
    for line in lines:
        outputLine = line.split("|")[1].strip().split(" ")
        outputLines.append(outputLine)
        panel = line.split("|")[0].strip().split(" ")
        tenPanel.append(panel)
    return tenPanel, outputLines

# Iterate through each number and add to the score for each segment
def calculateSegmentFrequencies(sevenSegmentFlags):
    # Start with a list of zeros length 7 to represent each segment
    sevenSegmentCounts = [0] * 7
    for digit in sevenSegmentFlags:
        for index, segment in enumerate(digit):
            if segment:
                sevenSegmentCounts[index] = sevenSegmentCounts[index] + 1
    return sevenSegmentCounts

# Calculate the frequency score for each digit
def calculateDigitScores(sevenSegmentFlags, sevenSegmentFreqs):
    digitScores = []
    # Iterate through each digit's segment flags
    for digit, sevenSegmentFlag in enumerate(sevenSegmentFlags):
        totalDigitScore = 0
        # For each digit's segment we'll add to its score based on the frequency score calculated earlier
        for index, flag in enumerate(sevenSegmentFlag):
            if flag:
                totalDigitScore = totalDigitScore + sevenSegmentFreqs[index]
        # Now we have this digit's unique fingerprint
        digitScores.append(totalDigitScore)
    return digitScores

# Calculate the input frequencies for later scoring
def calculateInputFrequencies(tenPanel):
    # We can just use a dictionary here since we don't actually care about what their 'real' position is
    sevenSegmentCounts = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0}
    for digit in tenPanel:
        for segment in digit:
            sevenSegmentCounts[segment] = sevenSegmentCounts[segment] + 1
    return sevenSegmentCounts

# Calculate the score for each scrambled digit
def calculateInputScores(tenPanel, inputFreqs, digitScores):
    # Construct a dictionary of each tenPanel's scrambled display along with its score
    # This will act as a fingerprint that we'll be able to use to link the final output to their integer values
    digitDict = {}
    for digit in tenPanel:
        digitScore = 0
        for segment in digit:
            digitScore = digitScore + inputFreqs[segment]
        digitDict[digitScore] = digitScores.index(digitScore)
    return digitDict

# Fingerprint each output signal, concatenate them into a final number
def fingerprintOutput(outputSignals, inputFingerprint, inputFreqs):
    outputString = ""
    for outputSignal in outputSignals:
        digitScore = 0
        for segment in outputSignal:
            digitScore = digitScore + inputFreqs[segment]
        digit = str(inputFingerprint[digitScore])
        outputString = outputString + digit
    return int(outputString)

# Are we running against test or input?
runFlag = sys.argv[1]

# Signal for displaying each number
sevenSegmentFlags = [[True, True, True, False, True, True, True], #0
                    [False, False, True, False, False, True, False], #1
                    [True, False, True, True, True, False, True], #2
                    [True, False, True, True, False, True, True], #3
                    [False, True, True, True, False, True, False], #4
                    [True, True, False, True, False, True, True], #5
                    [True, True, False, True, True, True, True], #6
                    [True, False, True, False, False, True, False], #7
                    [True, True, True, True, True, True, True], #8
                    [True, True, True, True, False, True, True]] #9
# Get the frequency of each segment
sevenSegmentFreqs = calculateSegmentFrequencies(sevenSegmentFlags)
# Now use the frequencies to calculate a score for each digit
digitScores = calculateDigitScores(sevenSegmentFlags, sevenSegmentFreqs)
# Get the data from the input file
tenPanels, outputSignals = getData(runFlag)
outputs = 0
# Loop over each input line to get the output number
for index, tenPanel in enumerate(tenPanels):
    # Since the tenPanel in the input and our previous calculation both present ten individual digits, they should get the same fingerprint despite being scrambled
    inputFreqs = calculateInputFrequencies(tenPanel)
    inputFingerprint = calculateInputScores(tenPanel, inputFreqs, digitScores)
    displayNum = fingerprintOutput(outputSignals[index], inputFingerprint, inputFreqs)
    outputs = outputs + displayNum
print(str(outputs))
print("Done!")

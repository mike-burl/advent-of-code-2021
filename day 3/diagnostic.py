# first we open the input file and extract all data

print('Opening input file...')

with open('input.txt') as file:
    lines = file.readlines()

# We'll use two lists initialized at zero to keep track of the counts
# We don't know how long the input lines will be beforehand, so use the length of the first line to set the list size
zeroCounts = [0] * (len(lines[0]) - 1)
oneCounts = [0] * (len(lines[0]) - 1)

# Loop through the lines and count the 1s and 0s that appear
for line in lines:
    # We need both the index position and the actual character, so pull both
    # End line chars can be returned by the enumerator, watch out for this
    for index, bit in enumerate(line):
        if bit == '1':
            oneCounts[index] = oneCounts[index] + 1
        elif bit == '0':
            zeroCounts[index] = zeroCounts[index] + 1

# Now calculate both the Gamme and Espilon rates
# The problem does not mention what happens if the zero and one values are equal,
# so for now we'll assume that won't happen
binaryGamma = []
binaryEpsilon = []
for index, zeroCount in enumerate(zeroCounts):
    if zeroCount > oneCounts[index]:
        binaryGamma.append(0)
        binaryEpsilon.append(1)
    elif zeroCount < oneCounts[index]:
        binaryGamma.append(1)
        binaryEpsilon.append(0)
    else:
        print(str(oneCounts))
        print(str(zeroCounts))
        raise Exception("I TOLD YOU THIS WOULD HAPPEN")

print("binaryGamma: " + str(binaryGamma))
print("binaryEpsilon: " + str(binaryEpsilon))

# Now convert the binary lists to actual numbers with bitwise operators and multiply them for our final answer
gamma = 0
for digit in binaryGamma:
    gamma = (gamma << 1) | digit

epsilon = 0
for digit in binaryEpsilon:
    epsilon = (epsilon << 1) | digit

print("Gamma: " + str(gamma))
print("Epsilon: " + str(epsilon))

powerConsumption = gamma * epsilon
print("Power consumption: " + str(powerConsumption))
print("Done!")

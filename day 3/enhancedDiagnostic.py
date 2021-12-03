# first we open the input file and extract all data

print('Opening input file...')

with open('input.txt') as file:
    lines = file.readlines()

# initialize our x and y vectors
horizontal = 0
depth = 0
aim = 0

# for each line, we'll modify either the aim or horizontal and depth vectors
for line in lines:
    # split each line into an array
    # index 0 is the command, index 1 is the command value
    vector = line.split()
    command = vector[0]
    value = int(vector[1])

    # execute instructions based on the command given
    if command == 'down':
        # increase the aim
        aim = aim + value
        print('aim increased to ' + str(aim))
    elif command == 'up':
        # decrease the aim
        aim = aim - value
        print('aim decreased to ' + str(aim))
    elif command == 'forward':
        # move the submarine based on the current aim and value provided
        horizontal = horizontal + value
        aimVector = aim * value
        depth = depth + aimVector
        # the submarine can't fly!
        if depth < 0:
            depth = 0
        print('aimVector: ' + str(aimVector) + ' submarine position: (' + str(horizontal) + ',' + str(depth) + ')')

finalAnswer = horizontal * depth
print(finalAnswer)
print("Done!")

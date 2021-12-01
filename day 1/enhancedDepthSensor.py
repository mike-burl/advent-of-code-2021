print('Opening input file...')

with open('input.txt') as file:
    lines = file.readlines()
    
# First set the first two indexes in the array
firstNum = int(lines[0])
secondNum = int(lines[1])
thirdNum = int(lines[2])

counter = 0

# Initialize our windows
slidingWindow = firstNum + secondNum + thirdNum
previousSlidingWindow = 0

# Now we loop over the remaining items in the array
for line in lines[3:]:
    firstNum = secondNum
    secondNum = thirdNum
    thirdNum = int(line)

    previousSlidingWindow = slidingWindow
    slidingWindow = firstNum + secondNum + thirdNum
    
    if slidingWindow > previousSlidingWindow:
        counter = counter + 1

print(counter)

file.close()

print('Done!')

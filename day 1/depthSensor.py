print('Opening input file...')

with open('input.txt') as file:
    lines = file.readlines()
    
# First set the first two indexes in the array
firstNum = lines[0]
secondNum = lines[1]

# Initialize our counter and check to see if secondNum > firstNum
counter = 0
if secondNum > firstNum:
    counter = counter + 1

hasPrinted = False
# Now we loop over the remaining items in the array
for line in lines[2:]:
    firstNum = secondNum
    secondNum = line
    
    if secondNum > firstNum:
        counter = counter + 1

print(counter)

file.close()

print('Done!')

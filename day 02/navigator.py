# first we open the input file and extract all data

print('Opening input file...')

with open('input.txt') as file:
    lines = file.readlines()

# initialize our x and y vectors
horizontal = 0
vertical = 0

# for each line, we'll modify either the horizontal or vertical vector
for line in lines:
    # split each line into an array
    # index 0 is the direction, index 1 is the distance
    vector = line.split()
    direction = vector[0]
    distance = int(vector[1])

    # apply distance to horizontal or vertical vector based on direction
    if direction == 'forward':
        # move the submarine forwards
        horizontal = horizontal + distance 
    elif direction == 'up':
        # move the submarine up.  be sure to make sure it doesn't fly away!
        vertical = vertical - distance
        if vertical < 0:
            vertical = 0
    elif direction == 'down':
        # move the submarine down
        vertical = vertical + distance     

finalAnswer = horizontal * vertical
print(finalAnswer)
print("Done!")

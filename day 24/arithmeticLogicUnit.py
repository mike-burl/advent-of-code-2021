import sys

registerDict = {'w':0, 'x':1, 'y':2, 'z':3}
class ALUCache:
    inp = 0
    registers = [0, 0, 0, 0]

    def __init__(self, newInp, newRegister):
        self.inp = newInp
        self.registers = newRegister

    # It's looking like we don't have enough entropy in our hashing.  Let's turn it up   
    def toTuple(self):
        return (self.registers[0], self.registers[1], self.registers[2], self.registers[3])
        
    def toString(self):
        stringInts = [str(num) for num in self.registers]
        returnString = ":".join(stringInts)
        return returnString

# Open the data file and extract our data
def getData(runFlag):
    with open(runFlag + '.txt') as file:
        lines = file.readlines()
    instructions = []
    for line in lines:
        line = line.rstrip()
        line = line.split(" ")
        inst = line[0]
        if inst == 'inp':
            instructions.append([inst, line[1]])
        else:
            instructions.append([inst, line[1], line[2]])

    return instructions

# Iterate through all caches and delete all duplicate register sets
# Final cache is determined by which has the highest inp value
def cleanCaches():
    registerSet = set({})
    for cache in reversed(caches):
        key = cache.toTuple()
        # This key hasn't been encountered yet, stash it and continue
        if key not in registerSet:
            registerSet.add(key)
            continue
        # This key has been encountered, delete it
        else:
            caches.remove(cache)

# For each remaining cache we want to expand it by 9, one for each digit
def expandCaches(reg):
    regInt = registerDict[reg]
    newCaches = []
    global caches
    if len(caches) > 0:
        for cache in caches:
            for i in range(1, 10):
                newInp = (cache.inp * 10) + i
                newRegisters = cache.registers.copy()
                newRegisters[regInt] = i
                newCaches.append(ALUCache(newInp, newRegisters))
    else:
        for i in range(1, 10):
                newInp = i
                newRegisters = [0,0,0,0]
                newRegisters[regInt] = i
                newCaches.append(ALUCache(newInp, newRegisters))
    caches = newCaches

# Add the value of a by the value of b, then store the result in variable a
def addCaches(a, b):
    aI = registerDict[a]
    # For efficiency sake we'll just use two branches based on whether b is a pointer or literal
    if b.isalpha():
        bI = registerDict[b]
        for cache in caches:
            cache.registers[aI] = cache.registers[aI] + cache.registers[bI]
    else:
        bI = int(b)
        for cache in caches:
            cache.registers[aI] = cache.registers[aI] + bI
            
# Multiply the value of a by the value of b, then store the result in variable a
def multiplyCaches(a, b):
    aI = registerDict[a]
    # For efficiency sake we'll just use two branches based on whether b is a pointer or literal
    if b.isalpha():
        bI = registerDict[b]
        for cache in caches:
            cache.registers[aI] = cache.registers[aI] * cache.registers[bI]
    else:
        bI = int(b)
        for cache in caches:
            cache.registers[aI] = cache.registers[aI] * bI

# Divide the value of a by the value of b, then store the result in variable a
def divideCaches(a, b):
    aI = registerDict[a]
    # For efficiency sake we'll just use two branches based on whether b is a pointer or literal
    if b.isalpha():
        bI = registerDict[b]
        for cache in caches:
            cache.registers[aI] = int(cache.registers[aI] / cache.registers[bI])
    else:
        bI = int(b)
        for cache in caches:
            cache.registers[aI] = int(cache.registers[aI] / bI)

# Modulo the value of a by the value of b, then store the result in variable a
def moduloCaches(a, b):
    aI = registerDict[a]
    # For efficiency sake we'll just use two branches based on whether b is a pointer or literal
    if b.isalpha():
        bI = registerDict[b]
        for cache in caches:
            cache.registers[aI] = cache.registers[aI] % cache.registers[bI]
    else:
        bI = int(b)
        for cache in caches:
            cache.registers[aI] = cache.registers[aI] % bI

# Check if the value of a is equal to the value of b, store 1 in a if equal, 0 if not
def equalCaches(a, b):
    aI = registerDict[a]
    # For efficiency sake we'll just use two branches based on whether b is a pointer or literal
    if b.isalpha():
        bI = registerDict[b]
        for cache in caches:
            if cache.registers[aI] == cache.registers[bI]:
                cache.registers[aI] = 1
            else:
                cache.registers[aI] = 0
    else:
        bI = int(b)
        for cache in caches:
            if cache.registers[aI] == bI:
                cache.registers[aI] = 1
            else:
                cache.registers[aI] = 0
                
inputFlag = sys.argv[1]
instructions = getData(inputFlag)
print(instructions)
caches = []
for inst in instructions:
    # on inp instructions we want to clean the cache, then expand it
    if inst[0] == 'inp':
        if len(caches) > 0:
            print("before clean: " + str(len(caches)))
            cleanCaches()
            print("after clean: " + str(len(caches)))
        expandCaches(inst[1])
    elif inst[0] == 'add':
        addCaches(inst[1], inst[2])
    elif inst[0] == 'mul':
        multiplyCaches(inst[1], inst[2])
    elif inst[0] == 'div':
        divideCaches(inst[1], inst[2])
    elif inst[0] == 'mod':
        moduloCaches(inst[1], inst[2])
    elif inst[0] == 'eql':
        equalCaches(inst[1], inst[2])

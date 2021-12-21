import math
class Scanner:
    def __init__(self, ident):
        self.points = []
        self.distances = []
        self.ident = ident
        self.offset = [0, 0, 0]
        self.axisSign = [1, 1, 1]
        self.axisMap = [0, 1, 2]

    def calculateDistances(self):
        self.distances = []
        # Create a matrix of distances
        for i in range(len(self.points)):
            p1 = self.points[i]
            distances = []

            for j in range(len(self.points)):
                if i == j:
                    continue
                p2 = self.points[j]
                dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)
                distances.append(dist)

            distances.sort()
            self.distances.append(distances)

    def findOverlapping(self, other: 'Scanner'):
        commonPoints = {}
        for i in range(len(self.distances)):
            for j in range(len(other.distances)):
                _c = 0
                if i in commonPoints:
                    break
                for k in range(12):
                    if self.distances[i][k] == other.distances[j][k]:
                        _c += 1
                if _c > 1:
                    # print(_c)
                    commonPoints[i] = j
        if len(commonPoints) < 1:
            # Apparently 12 points are always shared.
            return False

        # Determine axis switch. By default we assume complete alignment
        axisMap = [0, 1, 2]
        axisSign = [1, 1, 1]
        offset = [None, None, None]

        # For all possibilities of rotated and flipped axes, try to determine
        # the offset.
        for i in range(3):
            # i - axis rotation
            for j in [1, -1]:

                _offset_x = []
                _offset_y = []
                _offset_z = []

                for key in commonPoints:
                    p1 = self.points[key]
                    p2 = other.points[commonPoints[key]]
                    _offset_x.append(p1[0] - j * p2[i])
                    _offset_y.append(p1[1] - j * p2[i])
                    _offset_z.append(p1[2] - j * p2[i])

                # When applying axis mapping, do not do both switcheroos!
                # Other final mapping will be wrong.
                if len(set(_offset_x)) == 1:
                    axisMap[0] = i
                    axisSign[0] = j
                    offset[0] = _offset_x[0]
                if len(set(_offset_y)) == 1:
                    axisMap[1] = i
                    axisSign[1] = j
                    offset[1] = _offset_y[0]
                if len(set(_offset_z)) == 1:
                    axisMap[2] = i
                    axisSign[2] = j
                    offset[2] = _offset_z[0]
                # print(_offset_x, _offset_y, _offset_z)

        # If one of the axis is undetermined stop.
        if any([_ == None for _ in offset]):
            return False

        other.offset = offset
        other.axisMap = axisMap
        other.axisSign = axisSign
        other.alignPoints()
        return True

    def alignPoints(self):
        """Function that aligns the offset with the root scanner.
        """
        for i in range(len(self.points)):
            x, y, z = self.axisMap
            sx, sy, sz = self.axisSign

            new_x = self.offset[0] + sx * self.points[i][x]
            new_y = self.offset[1] + sy * self.points[i][y]
            new_z = self.offset[2] + sz * self.points[i][z]

            self.points[i][0] = new_x
            self.points[i][1] = new_y
            self.points[i][2] = new_z


scanners = []
file = "input.txt"
with open(file, 'r') as f:
    current = None
    _c = 0
    for line in f:
        if line.startswith('---'):
            if current:
                current.points = points
                current.calculateDistances()
            current = Scanner(_c)
            _c += 1
            scanners.append(current)
            points = []
            continue
        if not line.strip():
            continue

        points.append([int(_) for _ in line.split(',')])

    current.points = points
    current.calculateDistances()

toProcess = scanners[:]
processed = [scanners[0]]
toProcess.pop(0)

while toProcess:
    # pop the first one
    scanner = toProcess.pop(0)

    for i, aligned in enumerate(processed):
        ok = aligned.findOverlapping(scanner)
        if ok:
            # print(f'Aligned to {i}')
            break
    if ok:
        processed.append(scanner)
        # for aligned in processed:
        #     print(aligned.points)
    else:
        toProcess.append(scanner)

# Gather all the points and return the number of beacons
points = []
for scanner in processed:
    for point in scanner.points:
        if point in points:
            continue
        else:
            points.append(point)
print("Part 1. Number of beacons:", len(points))


max_distance_between_2scanners = 0
for i in range(len(processed)):
    for j in range(i, len(processed)):
        s1 = processed[i]
        s2 = processed[j]

        dist = abs(s1.offset[0] - s2.offset[0]) + abs(s1.offset[1] - s2.offset[1]) + abs(s1.offset[2] - s2.offset[2])

        if dist > max_distance_between_2scanners:
            max_distance_between_2scanners = dist
print("Part 2. Max manhattan distance between two scanners: ", max_distance_between_2scanners)

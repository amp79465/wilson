# generates a 3D maze schematic in a csv file.
# for use on command line.
# parameters are the x, y, and z dimensions of the maze and the filename.csv in that order

import sys, random, csv

# P - positive, N - negative
class Cell:
    def __init__(self):
        self.wallPX = True
        self.wallNX = True
        self.wallPY = True
        self.wallNY = True
        self.wallPZ = True
        self.wallNZ = True
        self.coordX = 0
        self.coordY = 0
        self.coordZ = 0
        self.neighbors = []

# The x, y, z should probably just reference the globals initX, etc    
def initSpace(x, y, z):
    mazeBlank = [[] for i in range(x)]
    for i in range(x):
        mazeBlank[i] = [[] for i in range(y)]
    for i in range(x):
        for j in range(y):
            mazeBlank[i][j] = [Cell() for k in range(z)]
    
    for a in range(x):
        for b in range(y):
            for c in range(z):
                mazeBlank[a][b][c].coordX = a
                mazeBlank[a][b][c].coordY = b
                mazeBlank[a][b][c].coordZ = c
    populateNeighbors(mazeBlank)
    return mazeBlank

def populateNeighbors(maze):
    for a in range(len(maze)):
        for b in range(len(maze[a])):
            for c in range(len(maze[a][b])):
                # rather than painstakingly work through the coordinate logic
                # using IndexError exceptions 
                try:
                    if maze[a+1][b][c] not in maze[a][b][c].neighbors:
                        maze[a][b][c].neighbors.append(maze[a+1][b][c])                                                
                except IndexError:
                    pass
                try:
                    if maze[a-1][b][c] not in maze[a][b][c].neighbors:
                        maze[a][b][c].neighbors.append(maze[a-1][b][c]) 
                except IndexError:
                    pass
                try:
                    if maze[a][b+1][c] not in maze[a][b][c].neighbors:
                        maze[a][b][c].neighbors.append(maze[a][b+1][c]) 
                except IndexError:
                    pass
                try:
                    if maze[a][b-1][c] not in maze[a][b][c].neighbors:
                        maze[a][b][c].neighbors.append(maze[a][b-1][c]) 
                except IndexError:
                    pass
                try:
                    if maze[a][b][c+1] not in maze[a][b][c].neighbors:
                        maze[a][b][c].neighbors.append(maze[a][b][c+1]) 
                except IndexError:
                    pass
                try:
                    if maze[a][b][c-1] not in maze[a][b][c].neighbors:
                        maze[a][b][c].neighbors.append(maze[a][b][c-1]) 
                except IndexError:
                    pass
                
    # ensure neighbor lists are unique            
    for a in range(len(maze)):
        for b in range(len(maze[a])):
            for c in range(len(maze[a][b])):
                for n in maze[a][b][c].neighbors:
                    if n.coordX > maze[a][b][c].coordX + 1:
                        del maze[a][b][c].neighbors[maze[a][b][c].neighbors.index(n)]
                    if n.coordX < maze[a][b][c].coordX - 1:
                        del maze[a][b][c].neighbors[maze[a][b][c].neighbors.index(n)]
                    if n.coordY > maze[a][b][c].coordY + 1:
                        del maze[a][b][c].neighbors[maze[a][b][c].neighbors.index(n)]
                    if n.coordY < maze[a][b][c].coordY - 1:
                        del maze[a][b][c].neighbors[maze[a][b][c].neighbors.index(n)]
                    if n.coordZ > maze[a][b][c].coordZ + 1:
                        del maze[a][b][c].neighbors[maze[a][b][c].neighbors.index(n)]
                    if n.coordZ < maze[a][b][c].coordZ - 1:
                        del maze[a][b][c].neighbors[maze[a][b][c].neighbors.index(n)]

# add all Cells to candidateList                        
def populateCandidates(maze):
    candidateList = []
    for a in range(len(maze)):
        for b in range(len(maze[a])):
            for c in range(len(maze[a][b])):
                candidateList.append(maze[a][b][c])
    return candidateList

def randomWalk():
    walkPath = []
    walkPath.append(mazeCandidates[random.randrange(len(mazeCandidates))])
    inMaze = False
    # pick a random neighbor and add it to walkpPath until we hit a member of the maze
    while not inMaze:
        nextChoice = random.randrange(len(walkPath[-1].neighbors))
        if walkPath[-1].neighbors[nextChoice] not in mazeCandidates:
            inMaze = True
        walkPath.append(walkPath[-1].neighbors[nextChoice])
        
    # erase the loops in walkPath
    for cell in walkPath:
        startingIndex = walkPath.index(cell)
        try:
            continueFlag = True
            while continueFlag:
                if cell in walkPath[startingIndex + 1:]:
                    del walkPath[startingIndex + 1:walkPath.index(cell, startingIndex + 1, len(walkPath)) + 1]
                else:
                    continueFlag = False
        except IndexError:
            pass
        
    eraseWalls(walkPath)

    # add all members of the loop-erased walkPath to mazeMembers
    for cell in walkPath[:-1]:
        mazeMembers.append(cell)
        del mazeCandidates[mazeCandidates.index(cell)]

    print("percentage in maze: ", (len(mazeMembers) / initCandidateCount) * 100)

# erasing walls in the masterMaze     
def eraseWalls (walkPath):
    for i in range(len(walkPath) - 1):
        if walkPath[i].coordX > walkPath[i+1].coordX:
            masterMaze[walkPath[i].coordX][walkPath[i].coordY][walkPath[i].coordZ].wallNX = False
            masterMaze[walkPath[i + 1].coordX][walkPath[i + 1].coordY][walkPath[i + 1].coordZ].wallPX = False
        elif walkPath[i].coordX < walkPath[i+1].coordX:
            masterMaze[walkPath[i].coordX][walkPath[i].coordY][walkPath[i].coordZ].wallPX = False
            masterMaze[walkPath[i + 1].coordX][walkPath[i + 1].coordY][walkPath[i + 1].coordZ].wallNX = False
        elif walkPath[i].coordY > walkPath[i+1].coordY:
            masterMaze[walkPath[i].coordX][walkPath[i].coordY][walkPath[i].coordZ].wallNY = False
            masterMaze[walkPath[i + 1].coordX][walkPath[i + 1].coordY][walkPath[i + 1].coordZ].wallPY = False
        elif walkPath[i].coordY < walkPath[i+1].coordY:
            masterMaze[walkPath[i].coordX][walkPath[i].coordY][walkPath[i].coordZ].wallPY = False
            masterMaze[walkPath[i + 1].coordX][walkPath[i + 1].coordY][walkPath[i + 1].coordZ].wallNY = False
        elif walkPath[i].coordZ > walkPath[i+1].coordZ:
            masterMaze[walkPath[i].coordX][walkPath[i].coordY][walkPath[i].coordZ].wallNZ = False
            masterMaze[walkPath[i + 1].coordX][walkPath[i + 1].coordY][walkPath[i + 1].coordZ].wallPZ = False
        elif walkPath[i].coordZ < walkPath[i+1].coordZ:
            masterMaze[walkPath[i].coordX][walkPath[i].coordY][walkPath[i].coordZ].wallPZ = False
            masterMaze[walkPath[i + 1].coordX][walkPath[i + 1].coordY][walkPath[i + 1].coordZ].wallNZ = False

# write to csv            
def outputMaze():
    with open(outFileName, 'w') as csvfile:
        outWriter = csv.writer(csvfile, delimiter=',')
        for y in range(initY):
            outWriter.writerow(["L", y])
            planeList = []

            # converting the mazeMaster object into x, z planes that represent each floor of the maze before writing.
            for x in range(initX):
                zListNX = []
                zList = []
                yListNX = []
                yList = []

                for z in range(initZ):
                    # populate zListNX with the wall values to the NZ, NX and NX of Cell
                    zListNX.append("X")
                    if masterMaze[x][y][z].wallNX:
                        zListNX.append("X")
                    else:
                        zListNX.append("O")
                    # populate zList with the NZ and coordinate of the cell
                    if masterMaze[x][y][z].wallNZ:
                        zList.append("X")
                    else:
                        zList.append("O")
                    zList.append("O")
                    # populate the yList and yListNX in the same way, establishing the paths through the ceiling
                    yList.append("X")
                    if masterMaze[x][y][z].wallPY:
                        yList.append("X")
                    else:
                        yList.append("O")
                    yListNX.append("X")
                    yListNX.append("X")
                # add walls at the end of each list
                zListNX.append("X")
                zList.append("X")
                yListNX.append("X")
                yList.append("X")
                planeList.append([])

                # make the planeList from the 4 row lists
                planeList[-1].append([i for i in zListNX])
                planeList[-1].append([i for i in zList])
                planeList[-1].append([i for i in yListNX])
                planeList[-1].append([i for i in yList])

            # write the floor
            for pz in range(len(planeList[0][0])):
                outList = []
                for px in range(len(planeList)):
                    outList.append(planeList[px][0][pz])
                    outList.append(planeList[px][1][pz])
                outList.append("X")
                outWriter.writerow(outList)
            outWriter.writerow([])
            outWriter.writerow(["C", y])

            # write the ceiling
            for pz in range(len(planeList[0][0])):
                outList = []
                for px in range(len(planeList)):
                    outList.append(planeList[px][2][pz])
                    outList.append(planeList[px][3][pz])
                outList.append("X")
                outWriter.writerow(outList)
            outWriter.writerow([])


random.seed()    
initX = int(sys.argv[1])
initY = int(sys.argv[2])
initZ = int(sys.argv[3])
outFileName = str(sys.argv[4])

print("initializing maze...")
masterMaze = initSpace(initX, initY, initZ)
print("populating maze...")
mazeMembers = []
mazeCandidates = populateCandidates(masterMaze)

initCandidateCount = len(mazeCandidates)
startingCell = random.randrange(len(mazeCandidates))
mazeMembers.append(mazeCandidates[startingCell])
del mazeCandidates[startingCell]

while len(mazeCandidates) > 0:
    randomWalk()

print("rendering maze...")
outputMaze()
print("done!")

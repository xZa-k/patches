from graphics import *
from pprint import pprint
from time import sleep
from random import randint

PATCHWORK_SIZE = 5

# colors = ["blue", "orange", "red"]
colors = []
VALID_COLORS = ["red", "green", "blue", "magenta", "orange", "cyan"]
VALID_SIZES = [5, 7, 9]



# Returns a triangle polygon at a specified position, along with a direction it points
def triangle(pos, direction):
    if direction == "down":
        return Polygon(pos, Point(pos.x + 20, pos.y), Point(pos.x + 10, pos.y + 10))
    elif direction == "right":
        return Polygon(pos, Point(pos.x, pos.y + 20), Point(pos.x + 10, pos.y + 10))

# Draws 2 triangles in a direction
def drawDoubleTriangle(win, pos, direction, color):

    secondPos = pos
    if direction == "down":
        secondPos = Point(pos.x, pos.y + 10)
    elif direction == "right":
        secondPos = Point(pos.x + 10, pos.y)

    tri = triangle(pos, direction)
    tri.setFill(color)
    tri.setOutline(color)
    tri.draw(win)

    tri2 = triangle(secondPos, direction)
    tri2.setFill(color)
    tri2.setOutline(color)
    tri2.draw(win)

    return (tri, tri2)

def drawCircle(win, pos, color):
    circle = Circle(Point(pos.x + 10, pos.y + 10), 10)
    circle.setFill(color)
    circle.setOutline(color)
    circle.draw(win)
    return circle


### Final patch ###
def finalPatch(pos, color):
    patchworkArray[int(pos.x//100)][int(pos.y//100)] = {
        "type": "final",
        "color": color,
        "objects": ""
    }


def drawFinalPatch(win, pos, color):
    size = int(100 + pos.x)
    squareSize = 10
    squareArray = []
    for x in range(int(pos.x), size , squareSize):
        y = abs(x - size + squareSize - pos.y)
        square = Rectangle(Point(x, y), Point(x+squareSize, y+squareSize))
        square.setFill(color)
        square.setOutline(color)
        square.draw(win)
        squareArray.append(square)

    return squareArray



### Penultimate patch ###
def penPatch(pos, color):
    patchworkArray[int(pos.x//100)][int(pos.y//100)] = {
        "type": "pen",
        "color": color,
        "objects": ""
    }


def drawPenPatch(win, pos, color):
    drawSize = 20
    objectArray = []

    for column in range(5):
        if column % 2 == 0:
            direction = "down"
            mod = 0
        else:
            direction = "right"
            mod = 1

        for row in range(5):
            if row % 2 == mod:
                doubleTriangle = drawDoubleTriangle(win, Point(pos.x + column * drawSize, pos.y + row * drawSize), direction, color)
                objectArray.extend(doubleTriangle)
            else:
                circle = drawCircle(win, Point(pos.x + column * drawSize, pos.y + row * drawSize), color)
                objectArray.append(circle)

    return objectArray




def setColor(row, column, color):
    patchworkArray[row][column]["color"] = color

def patchwork(win):

    # Set dotted border color
    for column in range(PATCHWORK_SIZE):
        for row in range(PATCHWORK_SIZE):

            # Set to pen patch
            patchData = patchworkArray[row][column]

            # Diagonal line replaces pen patch with final patch
            if row == column:
                finalPatch(Point(column * 100, row * 100), "red")

            # Set base color to color 1
            setColor(row, column, colors[1])

            if column > 0 and column < PATCHWORK_SIZE - 1:
                if row > 0 and row < PATCHWORK_SIZE - 1:
                    setColor(row, column, colors[2])
                    

            if row % 2 == 0 and (column == 0 or column == PATCHWORK_SIZE-1):
                setColor(row, column, colors[0])
            if (row == 0 or row == PATCHWORK_SIZE-1) and column % 2 == 0:
                setColor(row, column, colors[0])


def drawPatchwork(win):

    # patchWorkObjects = [[None for x in range(PATCHWORK_SIZE)] for y in range(PATCHWORK_SIZE)]



    for column in range(PATCHWORK_SIZE):
        for row in range(PATCHWORK_SIZE):
            patchData = patchworkArray[row][column]


            if patchData["type"] == "final":
                patchworkArray[row][column]["objects"] = drawFinalPatch(win, Point(column * 100, row * 100), patchData["color"])

            elif patchData["type"] == "pen":
                patchworkArray[row][column]["objects"] = drawPenPatch(win, Point(column * 100, row * 100), patchData["color"])

            elif patchData["type"] == "none":
                for obj in patchworkArray[row][column]["objects"]:
                    obj.undraw()


def deletePatch(row, column):
    patchworkArray[row][column]["type"] = "none"
    for obj in patchworkArray[row][column]["objects"]:
        obj.undraw()

def getNeighbors(row, column):
    neighbors = []

    possibleNeighbors = [[row - 1, column], [row + 1, column], [row, column - 1], [row, column + 1]]
    # Filter out invalid indices

    def validateCoord(coord):
        if coord[0] < 0 or coord[1] < 0:
            return False
        if coord[0] > PATCHWORK_SIZE-1 or coord[1] > PATCHWORK_SIZE-1:
            return False
        return True

    # for i in range(len(possibleNeighbors)):
    #     if possibleNeighbors[i][0] > 0 or possibleNeighbors[i][1] > 0:
    #         neighbors.append(possibleNeighbors[i])
    #     if possibleNeighbors[i][0] < PATCHWORK_SIZE-1 or possibleNeighbors[i][1] < PATCHWORK_SIZE-1:
    #         neighbors.append(possibleNeighbors[i])

    # Filters it to only valid coordinates
    result = list(filter(validateCoord, possibleNeighbors))

    return result


def swapTile(row, column, toRow, toColumn):

    # Swap the actual drawing objects
    for obj in patchworkArray[row][column]["objects"]:
        obj.move((toColumn - column) * 100, (toRow - row) * 100)

    for i in range(100):
        for obj in patchworkArray[toRow][toColumn]["objects"]:
            obj.move( (column - toColumn), (row - toRow))
        sleep(0.01)

    # Swap the data in the array
    patchworkArray[row][column], patchworkArray[toRow][toColumn] = patchworkArray[toRow][toColumn], patchworkArray[row][column]


def puzzleMode(win):
    cursor = {"x": PATCHWORK_SIZE-1, "y": PATCHWORK_SIZE-1}
    deletePatch(cursor["x"], cursor["y"])

    
    
    shuffleCount = int(input("Shuffle count: "))

    # Shuffle board
    for i in range(shuffleCount):
        neighbors = getNeighbors(cursor["x"], cursor["y"])
        neighbor = neighbors[randint(0, len(neighbors)-1)]
        swapTile(cursor["y"], cursor["x"], neighbor[1], neighbor[0])
        cursor = {"x": neighbor[0], "y": neighbor[1]}

    while True:
        mousePoint = win.getMouse()
        mouseX = int(mousePoint.x // 100)
        mouseY = int(mousePoint.y // 100)

        neighbors = getNeighbors(cursor["x"], cursor["y"])
        if [mouseX, mouseY] in neighbors:
            swapTile(cursor["y"], cursor["x"], mouseY, mouseX )
            print(cursor)
            cursor = {"x": mouseX, "y": mouseY}
            print(cursor)


    

validInput = False
while not validInput:
    print("Valid square sizes are 5, 7 and 9.")
    sizeInput = input("Patchwork size:")
    if sizeInput.isdigit():
        if int(sizeInput) in VALID_SIZES:
            validInput = True
            PATCHWORK_SIZE = int(sizeInput)
        else:
            print("Invalid size")
    else:
        print("Input is not a number")

validInput = False
while not validInput:
    print("Valid colors are (r)ed, (g)reen, (b)lue, (m)agenta, (o)range, (c)yan")
    print("Please type the first letter of the desired colours i.e. omb")
    colorInput = input("Colors:")
    if colorInput.isascii():

        if len(colorInput) == 3:
            letters = [color[0] for color in VALID_COLORS]
            for char in colorInput:
                for colorIndex in range(len(letters)):
                    if char == letters[colorIndex]:
                        colors.append(VALID_COLORS[colorIndex])
            if len(colors) == 3:
                validInput = True
            else:
                print("Invalid color character inputted")
                colors = []
            
        else:
            print("Only 3 colors characters must be inputted")
    else:

        print("Input must only be letters")




patchworkArray = [[{"type": "pen", "color": "red", "objects": []} for x in range(PATCHWORK_SIZE)] for y in range(PATCHWORK_SIZE)]


win = GraphWin(width=100*PATCHWORK_SIZE, height=100*PATCHWORK_SIZE)
patchwork(win)

drawPatchwork(win)

win.getMouse()

puzzleMode(win)

win.getMouse()

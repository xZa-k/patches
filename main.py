from graphics import *
from pprint import pprint
PATCHWORK_SIZE = 5
patchworkArray = [[{"type": "pen", "color": "red"} for x in range(PATCHWORK_SIZE)] for y in range(PATCHWORK_SIZE)]
colors = ["blue", "orange", "red"]


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

def drawCircle(win, pos, color):
    circle = Circle(Point(pos.x + 10, pos.y + 10), 10)
    circle.setFill(color)
    circle.setOutline(color)
    circle.draw(win)


### Final patch ###
def finalPatch(pos, color):
    patchworkArray[int(pos.x//100)][int(pos.y//100)] = {
        "type": "final",
        "color": color
    }


def drawFinalPatch(win, pos, color):
    size = int(100 + pos.x)
    squareSize = 10
    for x in range(int(pos.x), size , squareSize):
        y = abs(x - size + squareSize - pos.y)
        square = Rectangle(Point(x, y), Point(x+squareSize, y+squareSize))
        square.setFill(color)
        square.setOutline(color)
        square.draw(win)    


### Penultimate patch ###
def penPatch(pos, color):
    patchworkArray[int(pos.x//100)][int(pos.y//100)] = {
        "type": "pen",
        "color": color
    }
    

def drawPenPatch(win, pos, color):
    drawSize = 20

    for column in range(5):
        if column % 2 == 0:
            direction = "down"
            mod = 0
        else:
            direction = "right"
            mod = 1

        for row in range(5):
            if row % 2 == mod:
                drawDoubleTriangle(win, Point(pos.x + column * drawSize, pos.y + row * drawSize), direction, color)
            else:
                drawCircle(win, Point(pos.x + column * drawSize, pos.y + row * drawSize), color)

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
    
            

    



if __name__ == "__main__":

    
    win = GraphWin(width=100*PATCHWORK_SIZE, height=100*PATCHWORK_SIZE)
    # penPatch(win, Point(100, 0), "red")
    patchwork(win)

    for column in range(PATCHWORK_SIZE):
        for row in range(PATCHWORK_SIZE):
            patchData = patchworkArray[row][column]
            pprint(patchworkArray)
            
            try:
                if patchData["type"] == "final":
                    drawFinalPatch(win, Point(column * 100, row * 100), patchData["color"])

                else:
                    drawPenPatch(win, Point(column * 100, row * 100), patchData["color"])
            except:
                pass

    win.getMouse()



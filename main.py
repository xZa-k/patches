from graphics import *


def finalPatch(win, position, color):
    size = int(100 + position.x)
    squareSize = 10
    for x in range(int(position.x), size , squareSize):
        y = abs(x - size + squareSize - position.y)
        square = Rectangle(Point(x, y), Point(x+squareSize, y+squareSize))
        square.setFill(color)
        square.setOutline(color)
        square.draw(win)



if __name__ == "__main__":
    # for x in range(11):
    #     y = 10 - x
    #     print(f"{x},{y}")
    
    win = GraphWin()
    finalPatch(win, Point(100, 100), "red")
    win.getMouse()


0, 10
1, 9
2, 8
3, 7
4, 6
5, 5
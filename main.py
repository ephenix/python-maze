import tkinter
from maze import *


root = tkinter.Tk()
canvas = tkinter.Canvas(root, bg="grey23", height=800, width=800)
canvas.pack()

grid = MazeGrid(canvas, 50,50, scale=15)

for row in grid:
    for node in row:
        node.draw_walls()

canvas.delete(grid[0][0].walls["North"])
canvas.delete(grid[-1][-1].walls["South"])

def traverse():
    if grid[0][0].traverse():
        root.after(1,traverse)

traverse()
root.mainloop()
import tkinter
from maze import *


root = tkinter.Tk()
canvas = tkinter.Canvas(root, bg="grey23", height=800, width=800)
canvas.pack()

grid = MazeGrid(10,10)
grid[0][0].traverse()

def draw_point(canvas,x,y,size):
    point = canvas.create_oval(x,y,x+size,y+size,fill='DodgerBlue1',outline="")
    return point

def draw_line(canvas,x,y,direction,scale):
    if direction == "North":
        x2 = x
        y2 = y - scale
    if direction == "South":
        x2 = x
        y2 = y + scale
    if direction == "East":
        x2 = x + scale
        y2 = y
    if direction == "West":
        x2 = x - scale
        y2 = y
    line = canvas.create_line(x,y,x2,y2,width=5)
    return line

def draw_grid(canvas, grid, scale):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            draw_point(canvas,x*scale+50,y*scale+50,20)

def draw_connections(canvas, grid, scale):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            for connection in grid[y][x].connections.keys():
                draw_line(canvas,x*scale+60,y*scale+60,connection,scale)


draw_grid(canvas, grid, 50)
draw_connections(canvas, grid, 50)

root.mainloop()
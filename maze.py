import random
from tkinter import Tk

class MazeNode():

    connected_nodes = []
    active_nodes = []

    def __init__(self, canvas, x, y, scale) -> None:
        self.canvas         = canvas
        self.weights        = {}
        self.neighbors      = {}
        self.connected_from = None
        self.connection_a   = None
        self.connection_b   = None
        self.x              = x
        self.y              = y
        self.scale          = scale
        self.center_x       = ( x * scale ) + scale
        self.center_y       = ( y * scale ) + scale
        self.walls          = {}

    def set_neighbor(self, neighbor, key, weight) -> None:
        self.neighbors[key] = neighbor
        self.weights[key] = weight
       
    def best_connection(self):
        best_node = None
        best_weight = 1.0
        best_key = None
        for parent in self.active_nodes:
            for key,node in parent.neighbors.items():
                if node not in self.connected_nodes:
                    if parent.weights[key] < best_weight:
                        best_node = parent
                        best_key = key
                        best_weight = parent.weights[key]
        return {
            "node": best_node,
            "key": best_key
        }

    def connect(self,key):
        if key == "North":
            inverse_key = "South"
        if key == "South":
            inverse_key = "North"
        if key == "East":
            inverse_key = "West"
        if key == "West":
            inverse_key = "East"
        self.canvas.delete(self.walls[key])
        self.canvas.delete(self.neighbors[key].walls[inverse_key])
        self.connected_nodes.append(self.neighbors[key])
        self.neighbors[key].connected_from = inverse_key
        self.active_nodes.append(self.neighbors[key])
        if self.connection_a == None:
            self.connection_a = self.neighbors[key]
        else:
            self.connection_b = self.neighbors[key]
            self.active_nodes.remove(self)
        
    def traverse(self):
        if self not in self.connected_nodes:
            self.connected_nodes.append(self)
            self.active_nodes.append(self)
        connection = self.best_connection()
        if connection["node"]:
            connection["node"].connect(connection["key"])
            return True
        else:
            return False

    def draw(self):
        self.canvas.create_oval(
            self.center_x - 5,
            self.center_y - 5,
            self.center_x + 5,
            self.center_y + 5,
            fill='DodgerBlue1',outline="")

    def draw_connections(self):
        if self.connection_a:
            self.canvas.create_line(
                self.center_x,
                self.center_y,
                self.connection_a.center_x,
                self.connection_a.center_y,
                width=3,fill="sea green")
        if self.connection_b:
            self.canvas.create_line(
                self.center_x,
                self.center_y,
                self.connection_b.center_x,
                self.connection_b.center_y,
                width=3,fill="medium sea green")
    
    def draw_neighbor_weights(self):
        for key,neighbor in self.neighbors.items():
            if key in ["East", "South"]:
                xa = self.center_x
                ya = self.center_y
                xb = neighbor.center_x
                yb = neighbor.center_y
                xc = (xa+xb)/2
                yc = (ya+yb)/2
                self.canvas.create_line(xa,ya,xb,yb)
                self.canvas.create_text(xc,yc,text="%.2f" % self.weights[key],fill="azure")
    
    def draw_walls(self):
        walls = ["North","South","East","West"]
        for key,neighbor in self.neighbors.items():
            if self.connection_a == neighbor:
                walls.remove(key)
            if self.connection_b == neighbor:
                walls.remove(key)
        if self.connected_from in walls:
            walls.remove(self.connected_from)
        for key in walls:
            self.draw_wall(key)

    def draw_wall(self,key):
        if key == "North":
            xa = self.center_x - self.scale/2
            ya = self.center_y - self.scale/2
            xb = self.center_x + self.scale/2
            yb = self.center_y - self.scale/2
        if key == "South":
            xa = self.center_x - self.scale/2
            ya = self.center_y + self.scale/2
            xb = self.center_x + self.scale/2
            yb = self.center_y + self.scale/2
        if key == "East":
            xa = self.center_x + self.scale/2
            ya = self.center_y - self.scale/2
            xb = self.center_x + self.scale/2
            yb = self.center_y + self.scale/2
        if key == "West":
            xa = self.center_x - self.scale/2
            ya = self.center_y - self.scale/2
            xb = self.center_x - self.scale/2
            yb = self.center_y + self.scale/2
        
        wall = self.canvas.create_line(xa,ya,xb,yb,width="4",fill='green yellow')
        self.walls[key]=wall

def MazeGrid(canvas, size_x, size_y, scale):
    grid = [ [MazeNode(canvas,x,y,scale) for x in range(size_x)] for y in range(size_y)]
    for y in range(size_y):
        for x in range(size_x):
            wx = random.random()
            wy = random.random()
            if x > 0:
                grid[y][x].set_neighbor(grid[y][x-1],"West",wx)
            if x < (size_x-1):
                grid[y][x].set_neighbor(grid[y][x+1],"East",wx)
            if y > 0:
                grid[y][x].set_neighbor(grid[y-1][x],"North",wy)
            if y < (size_y-1):
                grid[y][x].set_neighbor(grid[y+1][x],"South",wy)
    return grid

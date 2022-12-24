import random

class MazeNode():

    connected_nodes = []

    def __init__(self, x, y) -> None:
        self.weights     = {}
        self.neighbors   = {}
        self.connections = {}
        self.x = x
        self.y = y

    def inverse_key(key):
        if key == "North":
            return "South"
        if key == "South":
            return "North"
        if key == "East":
            return "West"
        if key == "West":
            return "East"

    def set_neighbor(self, neighbor, key, weight, inverse=True) -> None:
        self.neighbors[key] = neighbor
        self.weights[key] = weight
        if inverse:
            neighbor.set_neighbor(self, MazeNode.inverse_key(key), weight, inverse=False)

    def connect(self, key,inverse=True):
        if self not in self.connected_nodes:
            self.connected_nodes.append(self)
        self.weights.pop(key)
        self.connections[key] = self.neighbors.pop(key)
        if inverse:
            self.connections[key].connect(MazeNode.inverse_key(key),inverse=False)

    def lowest_weight_key(self):
        if len(self.neighbors) > 1 and len(self.connections):
            try:
                key = min(self.weights, key=self.weights.get)
            except ValueError:
                return None
            return key
        else:
            return None

    def get_expansion_node(self):
        lowest_weight_node=None
        lowest_weight = 1.0
        for node in self.connected_nodes:
            key = node.lowest_weight_key()
            if key:
                weight = node.weights[key]
                if weight < lowest_weight:
                    lowest_weight = weight
                    lowest_weight_node = node
        return lowest_weight_node        
    
    def autoconnect(self):
        key = self.lowest_weight_key()
        self.connect(key)

    def traverse(self):
        self.connected_nodes.append(self)
        while(True):
            node = self.get_expansion_node()
            if node:
                node.autoconnect()
            else:
                break

def MazeGrid(size_x, size_y):
    grid = [ [MazeNode(x,y) for x in range(size_x)] for y in range(size_y)]
    for y in range(size_y):
        for x in range(size_x):
            if x < (size_x-1):
                grid[y][x].set_neighbor(grid[y][x+1],"East",random.random())
            if y < (size_y-1):
                grid[y][x].set_neighbor(grid[y+1][x],"South",random.random())
    return grid

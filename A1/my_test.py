import random
INF = 99999

class Node:
    def __init__(self, current_depth=0, search_depth=0, coordinates):
        self.position = coordinates
        self.depth = current_depth

    def isLeaf():
        if self.depth == search_depth:
            return eval(self.position)

    def isMax():
        return True if self.depth % 2 == 0 else False

    def isMin():
        return True if self.depth % 2 != 0 else False

# search-evaluate architecture

def generate_move(depth=0):
    if depth != 0:
        for i in range(depth):
            for 
    else:
        while 

def eval(coordinates):
    return random.random()

def alphabeta(n, a, b):
    if n.isLeaf == True:
        return  eval(n.position)
    elif n.isMax == True:  
        g = -INF
        for 

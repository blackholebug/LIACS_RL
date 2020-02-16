import random
from hex_skeleton import HexBoard

import typing

INF = 99999

class Node:
    # Dict or Obj?
    def __init__(self, coordinates, current_depth=0, search_depth=99990):
        self.children = list()
        self.position = coordinates
        self.cdepth = current_depth
        self.sdepth = search

    def isLeaf(self):
        return True if self.cdepth == self.sdepth else False

    def isMax(self):
        return True if self.cdepth % 2 == 0 else False

    def isMin(self):
        return True if self.cdepth % 2 != 0 else False


# search-evaluate architecture

def gen_move(hexboard: HexBoard, current_depth=0, search_depth: int=999999):
    """
    start randomly with RED, traverse the board
    """
    init_step = (random.randint(0, hexboard.size), random.randint(0, hexboard.size))
    hexboard.place(init_step, hexboard.RED) 
    root_node = Node(init_step, current_depth, search_depth)
    move(hexboard, current_depth, search_depth, root_node)

def move(hexboard: HexBoard, node: Node, current_depth=0, search_depth: int=999999):
    """
    search the board recursively
    """
    while not hexboard.is_game_over() and search_depth != current_depth:
        current_depth += 1
        for k, v in hexboard.board.items():
            if v == hexboard.EMPTY:
                current_step = k
                break
        current_color = hexboard.RED if current_depth % 2 == 0 else hexboard.BLUE
        hexboard.place(current_step, current_color)
        new_node = Node(current_step, current_depth, search_depth)
        node.children.append(new_node)
        move(hexboard, current_depth, search_depth, new_node)

def eval(coordinates):
    return random.random()

def alphabeta(node: Node, a: int, b: int, current_depth: int):
    if current_depth <= 0 or node.isLeaf == True:
        return eval(node.position)
    elif node.isMax == True:  
        g = -INF
        for c in node.children:
            g = max(g, alphabeta(c, a, b, current_depth-1))
            a = max(a, g)
            if g >= b:
                break
    elif node.isMin == True:
        g = INF
        for c in node.children:
            g = min(g, alphabeta(c, a, b, current_depth-1))
            b = min(b, g)
            if a >= g:
                break
    return g

def search():
    return 0
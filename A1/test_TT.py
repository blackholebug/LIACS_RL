import numpy as np
import networkx as nx

from board import HexBoard
from move import possible_moves
from search_with_TT import lower_upper_search, MAX, MIN
import time


def test_tt(size: int, max_depth: int):
    np.random.seed(4)
    board = HexBoard(size)
    tt = {"is_use": 1}
    while(True):
        """
        To see all these hits and updates, please remove the comments of line 60 & line 71 in
        search_with_TT.py.

        When max_depth = 3 and board size = 2: should hit 12 times at leafs + update 29 times 
        including root when the board is blank. Here shows all the hit(H) and updates(U)

                               O  
                _____________  U  _____________
               /         |           |         \
              /          |           |          \
             x           x           x           x     
             U           U           U           U 
          /  |  \     /  |  \     /  |  \     /  |  \      
         o   o   o   o   o   o   o   o   o   o   o   o
         U   U   U   U   U   U   U   U   U   U   U   U
        / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \
        x x x x x x x x x x x x x x x x x x x x x x x x
        U U U U U U U U H U H U H U H U H H H H H H H H
        """
        best_move = lower_upper_search(board, max_depth, memory=tt)
        board.place(best_move, MAX)

        if board.game_over:
            break

        moves = possible_moves(board)
        random_move = moves[np.random.randint(0, len(moves))]
        board.place(random_move, MIN)

        if board.game_over:
            break


def test_without_tt(size: int, max_depth: int):
    np.random.seed(4)
    board = HexBoard(size)

    while(True):
        best_move = lower_upper_search(board, max_depth)
        board.place(best_move, MAX)

        if board.game_over:
            break

        moves = possible_moves(board)
        random_move = moves[np.random.randint(0, len(moves))]
        board.place(random_move, MIN)

        if board.game_over:
            break


if __name__ == "__main__":
    time_start = time.process_time()

    for i in range(1):
        test_tt(6, 4)
    time1 = time.process_time() - time_start

    for i in range(1):
        test_without_tt(6, 4)
    time2 = time.process_time() - time_start

    print(f"run time of search with TT: {time1}")
    print(f"run time of search without TT: {time2}")

import numpy as np

from board import HexBoard
from move import possible_moves
from search import lower_upper_search, iterative_deeping, MAX, MIN
from evaluate import player_direction

# Trigger the print by delete the comment on line 33 & 34 of search.py.
# Test will return best move from every depth.


def test_iterative_deepening():
    np.random.seed(4)
    board = HexBoard(5)

    moves = possible_moves(board)
    random_move = moves[np.random.randint(0, len(moves))]
    board.place(random_move, MIN)
    board.print()

    best_move = iterative_deeping(board)
    board.place(best_move, MAX)
    board.print()


if __name__ == "__main__":
    test_iterative_deepening()

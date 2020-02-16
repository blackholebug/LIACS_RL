import numpy as np

from board import HexBoard
from move import possible_moves
from search import lower_upper_search, MAX, MIN


def test_search_vs_deterministic():
    np.random.seed(0)  # make random gen determinstic

    board = HexBoard(4)
    while not board.game_over:
        moves = possible_moves(board)
        random_move = moves[np.random.randint(0, len(moves))]
        board.place(random_move, MIN)

        best_move = lower_upper_search(board)
        board.place(best_move, MAX)

    assert board.game_over
    assert board.check_win(MAX)

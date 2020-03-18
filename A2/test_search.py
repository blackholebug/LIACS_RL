import numpy as np

from board import HexBoard
from move import get_possible_moves
from search import lower_upper_search
from evaluate import player_direction
from utils import player_color, MAX, MIN

# note random player on small board is quite hard?
# looses for seed 0 wins for other seeds on board size 3


def test_search_vs_deterministic():
    np.random.seed(4)  # make random gen determinstic
    board = HexBoard(2)
    while True:
        best_move = lower_upper_search(board)
        print(f"Best move: {best_move}")
        board.place(best_move, MAX)
        board.print()

        if board.game_over:
            break

        moves = get_possible_moves(board)
        random_move = moves[np.random.randint(0, len(moves))]
        board.place(random_move, MIN)
        board.print()

        if board.game_over:
            break

    print(f"max color: {player_color(MAX)}")
    print(f"max dir: {player_direction(MAX)}")
    print("final board:")
    board.print()
    assert board.check_win(MAX)


# note random player on small board is quite hard?
# looses for seed 0 wins for other seeds on board size 3
def test_win_ratio_full_tree_search():
    np.random.seed(0)  # make random gen determinstic
    for i in range(0, 10):
        board = HexBoard(3)
        while True:
            best_move = lower_upper_search(board)
            board.place(best_move, MAX)

            if board.game_over:
                break

            moves = get_possible_moves(board)
            random_move = moves[np.random.randint(0, len(moves))]
            board.place(random_move, MIN)

            assert not board.game_over


# note max_depth smaller then 2 will cause the AI to lose some games
# improvements to search might fix this
def test_win_ratio_fixed_depth():
    np.random.seed(0)  # make random gen determinstic
    for i in range(0, 10):
        board = HexBoard(4)
        while True:
            print(f"i: {i}")
            best_move = lower_upper_search(board, max_depth=3)
            board.place(best_move, MAX)

            if board.game_over:
                print("win")
                break

            moves = get_possible_moves(board)
            random_move = moves[np.random.randint(0, len(moves))]
            board.place(random_move, MIN)

            assert not board.game_over


# code below only runs if this file is called directly by python
# it does nothing when this module is imported we use it for
# debugging tests and investigating unexpected behaviour
if __name__ == "__main__":

    test_win_ratio_fixed_depth()

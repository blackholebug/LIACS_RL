import numpy as np

from board import HexBoard
from move import get_possible_moves
from MCTS_search import MCTS
from search_with_TT import lower_upper_search
from utils import MAX, MIN, player_color, player_direction

def test_MCTS_vs_non_deterministic():
    np.random.seed(4)  # make random gen determinstic
    board = HexBoard(6)
    while True:
        best_move = MCTS(board, 500)
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

def test_MCTS_vs_minmax():
    np.random.seed(4)  # make random gen determinstic
    board = HexBoard(6)
    tt = {"is_use": 1}
    while True:
        best_move = MCTS(board, 7000)
        print(f"MAX Best move: {best_move}")
        board.place(best_move, MAX)
        board.print()

        if board.game_over:
            break
        
        best_move = lower_upper_search(board, max_depth=4, memory=tt)
        print(f"MIN Best move: {best_move}")
        board.place(best_move, MIN)
        board.print()

        if board.game_over:
            break

    print(f"max color: {player_color(MAX)}")
    print(f"max dir: {player_direction(MAX)}")
    print("final board:")
    board.print()
    # assert board.check_win(MAX)


def test_minmax_vs_MCTS():
    np.random.seed(4)  # make random gen determinstic
    board = HexBoard(6)
    tt = {"is_use": 1}
    while True:
        best_move = lower_upper_search(board, max_depth=4, memory=tt)
        print(f"MAX Best move: {best_move}")
        board.place(best_move, MAX)
        board.print()

        if board.game_over:
            break
        
        best_move = MCTS(board, 7000)
        print(f"MIN Best move: {best_move}")
        board.place(best_move, MIN)
        board.print()

        if board.game_over:
            break

    print(f"max color: {player_color(MAX)}")
    print(f"max dir: {player_direction(MAX)}")
    print("final board:")
    board.print()
    # assert board.check_win(MAX)

if __name__ == "__main__":
    # test_MCTS_vs_non_deterministic()
    test_MCTS_vs_minmax()
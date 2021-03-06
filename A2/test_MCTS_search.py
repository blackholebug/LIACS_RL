import numpy as np

from board import HexBoard
from move import get_possible_moves
from search_mcts import mcts_search
from search_with_TT import lower_upper_search
from utils import MAX, MIN, player_color, player_direction

def test_MCTS_on_endgame_1():
    lose = 0
    for i in range(1000):
        np.random.seed()  # make random gen determinstic
        board = HexBoard(4)
        board.place((0, 1), MAX)
        board.place((1, 1), MAX)
        board.place((2, 2), MAX)
        board.place((3, 2), MAX)
        """
        a b c d 
        -----------------------
        0 |- - - - |
        1 | b b - - |
        2 |  - - b b |
        3 |   - - - - |
        -----------------------
        """
        best_move = mcts_search(board, 500)
        board.place(best_move, MAX)

        if not board.check_win(MAX):
            lose += 1
            print(f"max color: {player_color(MAX)}")
            print(f"max dir: {player_direction(MAX)}")
            print(f"Best move: {best_move}")
            print("final board:")
            board.print()

    print(f"lose {lose} times in 1000 tries")


def test_MCTS_on_endgame_2():
    count_1 = 0
    count_2 = 0
    for i in range(1000):
        np.random.seed()  # make random gen determinstic
        board = HexBoard(5)
        board.place((1, 2), MAX)
        board.place((2, 2), MAX)
        board.place((2, 3), MAX)
        board.place((2, 4), MAX)
        board.place((0, 0), MIN)
        board.place((0, 2), MIN)
        board.place((0, 3), MIN)
        board.place((0, 4), MIN)
        """
        a b c d e
        -----------------------
        0 |r - - - - |
        1 | - - - - - |
        2 |  r b b b b |
        3 |   r - - - - |
        4 |    r - - - - |
        -----------------------
        """
        best_move = mcts_search(board, 1000)
        if best_move == (0, 1):
            count_1 += 1
        if best_move == (1, 1):
            count_2 += 1

    print(f"{count_1} times find the best place, {count_2} times find a fair place")    


def test_MCTS_vs_minmax():
    np.random.seed(4)  # make random gen determinstic
    board = HexBoard(6)
    tt = {"is_use": 1}
    while True:
        best_move = mcts_search(board, 7000)
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
        
        best_move = mcts_search(board, 7000)
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
    # test_minmax_vs_MCTS()
    test_MCTS_on_endgame_1()
    test_MCTS_on_endgame_2()
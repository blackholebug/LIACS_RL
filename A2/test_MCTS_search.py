import numpy as np

from board import HexBoard
from move import get_possible_moves
from MCTS_search import MCTS
from utils import MAX, MIN, player_color, player_direction

def test_MCTS_vs_deterministic():
    np.random.seed(4)  # make random gen determinstic
    board = HexBoard(2)
    while True:
        best_move = MCTS(board, 5)
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

if __name__ == "__main__":
    test_MCTS_vs_deterministic()
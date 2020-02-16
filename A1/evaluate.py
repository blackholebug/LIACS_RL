from board import HexBoard
import numpy as np
from itertools import product


# evaluation function
def score(board: HexBoard, player: int) -> int:
    adj_matrix = to_graph(board)
    adj_matrix = add_edge_points(adj_matrix)
    score = hash(adj_matrix) # TODO use the Dijkstra
    return score

def to_graph(board: HexBoard) -> np.ndarray:
    s = board.size
    adj_matrix = np.full((s*s, s*s), np.inf)
    for x, y in product(range(s), range(s)):
        neighbors = board.get_neighbors((x,y))
        for (i, j) in neighbors:
            # TODO probably reduce extra check
            if board.board[x, y] != HexBoard.EMPTY and \
                board.board[x, y] == board.board[i, j]:
                adj_matrix[x*s+y, i*s+j] = 0
            elif board.board[x, y] * board.board[i, j] == HexBoard.RED * HexBoard.BLUE:
                continue
            else:
                adj_matrix[x*s+y, i*s+j] = 1
    return adj_matrix

def add_edge_points(adj_matrix: np.ndarray) -> np.ndarray:
    """
    now only consider adding top and bottom points
    """
    mat_size = adj_matrix.shape[0]
    board_size = int(mat_size ** 0.5)
    new_mat = np.full((mat_size+2, mat_size+2), np.inf)
    new_mat[:mat_size, :mat_size] = adj_matrix
    new_mat[-2, :board_size] = np.zeros(board_size)
    new_mat[-1, -2-board_size:-2] = np.zeros(board_size)
    new_mat[:mat_size, -2:] = new_mat[-2:, :mat_size].T
    return new_mat

def test_score():
    for i in range(0, 2):
        winner = HexBoard.RED if i == 0 else HexBoard.BLUE
        loser = HexBoard.BLUE if i == 0 else HexBoard.RED
        board = HexBoard(3)
        board.place((0, 2), winner)
        board.place((1, 1), loser)
        board.place((1, 0), winner)
        board.place((2, 1), loser)
        board.place((0, 1), winner)

        print("The Adjacency Matrix is")
        print(to_graph(board))
        board.print()

        board.place((2, 2), loser)
        board.place((2, 0), winner)
        board.place((1, 2), loser)

        print("The Adjacency Matrix is")
        print(to_graph(board))
        board.print()

        assert board.check_win(winner)
        assert not board.check_win(loser)
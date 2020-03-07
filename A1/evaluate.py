from board import HexBoard

import numpy as np
import networkx as nx
from typing import Tuple, List
from utils import INF, player_direction

# evaluation function amplify own strength while diminishing enemy's


def score_with_rivalry(board: HexBoard, friend: int) -> int:
    C = 2  # adjust this parameter to change the importance ratio of friend's winning and enemy's lose
    size = board.size
    enemy = board.get_opposite_color(friend)
    adj_matrix_friend = create_adj_matrix_scored(board, friend)
    adj_matrix_enemy = create_adj_matrix_scored(board, enemy)
    graph_friend = nx.Graph(adj_matrix_friend)
    graph_enemy = nx.Graph(adj_matrix_enemy)
    source = size * size
    target = size * size + 1
    try:
        eval_score_friend = nx.dijkstra_path_length(
            graph_friend, source, target)
    except nx.exception.NetworkXNoPath:
        eval_score_friend = INF  # NOTE: Change
    try:
        eval_score_enemy = nx.dijkstra_path_length(graph_enemy, source, target)
    except nx.exception.NetworkXNoPath:
        eval_score_enemy = INF  # NOTE: Change

    eval_score = C * eval_score_friend - eval_score_enemy  # NOTE: Change

    return eval_score


# evaluation function
def score(board: HexBoard, player: int) -> int:
    size = board.size
    adj_matrix = create_adj_matrix_scored(board, player)
    G = nx.Graph(adj_matrix)
    source = size * size
    target = size * size + 1
    try:
        score = - nx.dijkstra_path_length(G, source, target)
    except nx.exception.NetworkXNoPath:
        score = - INF

    return score


def index(coordinate: tuple, size: int) -> int:
    return coordinate[0] + coordinate[1] * size


# Blue
def get_boarder_left_right(board: HexBoard) -> Tuple[List[int], List[int]]:
    size = board.size
    left_border = [index((0, y), size) for y in range(size)]
    right_border = [index((size - 1, y), size) for y in range(size)]

    return left_border, right_border


# Red
def get_boarder_top_down(board: HexBoard) -> Tuple[List[int], List[int]]:
    size = board.size
    top_border = [index((x, 0), size) for x in range(size)]
    down_border = [index((x, size - 1), size) for x in range(size)]

    return top_border, down_border


def create_adj_matrix_scored(board: HexBoard, friend: int) -> np.ndarray:
    """
    computer's color is friend.
    size * size is to walk through the whole board.
    friend <-> friend: 1
    friend <-> empty, empty <-> empty: size*size
    enemy leaving unconnected : 0
    """
    size = board.size
    path_len_board = size * size
    adj_matrix = np.zeros(
        (size * size + 2, size * size + 2)
    )  # initial as all not connected
    for point in board.board:
        if board.board[point] == friend:
            # neighbor is coordinate tuple
            for neighbor in board.get_neighbors(point):
                if board.board[neighbor] == friend:
                    adj_matrix[index(point, size)][index(neighbor, size)] = 1
                    adj_matrix[index(neighbor, size)][index(point, size)] = 1
                elif board.board[neighbor] == board.EMPTY:
                    adj_matrix[index(point, size)][
                        index(neighbor, size)
                    ] = path_len_board
                    adj_matrix[index(neighbor, size)][
                        index(point, size)
                    ] = path_len_board
        if board.board[point] == board.EMPTY:
            for neighbor in board.get_neighbors(point):
                if (
                    board.board[neighbor] == board.EMPTY
                    or board.board[neighbor] == friend
                ):
                    adj_matrix[index(point, size)][
                        index(neighbor, size)
                    ] = path_len_board
                    adj_matrix[index(neighbor, size)][
                        index(point, size)
                    ] = path_len_board

    # connect the external starting and ending point
    if friend == HexBoard.BLUE:
        a_boarder, b_boarder = get_boarder_left_right(board)
    else:
        a_boarder, b_boarder = get_boarder_top_down(board)
    for i in a_boarder:
        adj_matrix[size * size][i] = 1
        adj_matrix[i][size * size] = 1
    for i in b_boarder:
        adj_matrix[size * size + 1][i] = 1
        adj_matrix[i][size * size + 1] = 1

    return adj_matrix

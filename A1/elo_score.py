from board import HexBoard
from move import possible_moves
from search import lower_upper_search
# from search_with_TT import lower_upper_search, iterative_deeping_with_TT

import trueskill as ts
import numpy as np
from typing import Tuple


def update_trueskill(rating1: ts.Rating, rating2: ts.Rating, is_first_win: bool) -> Tuple[ts.Rating]:
    if is_first_win:
        rating1, rating2 = ts.rate_1vs1(rating1, rating2)
        # print(f"1: {rating1} 2: {rating2}")
    else:
        rating2, rating1 = ts.rate_1vs1(rating2, rating1)
        # print(f"1: {rating1} 2: {rating2}")
    return rating1, rating2


def get_moves(board: HexBoard, flag: str) -> tuple:
    if flag == "random":
        pos_moves = possible_moves(board)
        move = pos_moves[np.random.randint(0, len(pos_moves))]
    elif flag == "depth3":
        move = lower_upper_search(board, max_depth=3)
    elif flag == "depth4":
        move = lower_upper_search(board, max_depth=4)
    return move


def calculate_trueskill(rating: ts.Rating) -> float:
    score = rating.mu - 3 * rating.sigma
    return score

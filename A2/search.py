# see https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#cite_note-RN03-12
# and Russel and Norvig Artificial inteligence p. 170
import time
from typing import Optional

from move import Move, get_possible_moves
from board import HexBoard
from evaluate import score, score_with_rivalry
from utils import MAX, MIN, INF, player_color


class Timer:
    started: float = 0.0  # in seconds
    maxduration: float = 0.0  # in seconds

    def __init__(self, maxduration: float):
        self.started = time.time()
        self.maxduration = maxduration

    def time_is_up(self) -> bool:
        now = time.time()
        if now - self.started > self.maxduration:
            return True
        return False


def iterative_deeping(board: HexBoard) -> Optional[Move]:
    depth = 1
    timer = Timer(10.0)

    while not timer.time_is_up():
        best_move = lower_upper_search(board, max_depth=depth)
        print(f"finish on depth: {depth}")
        print(f"current best move: {best_move}")
        depth += 1
    return best_move


# the alpha beta algorithm or as we prefer to call
# it lower upper almost a copy of max value but
# returns the move with the highest score, currently
# only the MAX player can use lower_upper
def lower_upper_search(board: HexBoard, max_depth: int = INF) -> Optional[Move]:
    lower = -INF
    upper = INF
    depth = 0

    best_overal_score = -INF
    best_overal_move = None
    for move in get_possible_moves(board):
        move.do(board, MAX)
        subtree_score = min_value(board, lower, upper, max_depth, depth)
        move.undo(board)

        # replaces max(best, subtree_score)
        if subtree_score >= best_overal_score:
            best_overal_score = subtree_score
            best_overal_move = move

        # should not do alpha beta here. as alpha beta should not
        # cut off since there is not any higher branche

    return best_overal_move


def max_value(
    board: HexBoard, lower: int, upper: int, max_depth: int, depth: int
) -> int:
    best = -INF
    depth += 1

    # if leaf aka if game over
    if board.is_game_over():
        return -INF  # min player wins
    if depth > max_depth:
        # return score_with_rivalry(board, MAX)
        return score(board, MAX)

    moves = get_possible_moves(board)
    for move in moves:
        move.do(board, MAX)
        best = max(best, min_value(board, lower, upper, max_depth, depth))
        move.undo(board)

        lower = max(lower, best)  # update lower bound alpha
        if lower >= upper:
            return best  # beta cutoff, a>=b

    return best


def min_value(
    board: HexBoard, lower: int, upper: int, max_depth: int, depth: int
) -> int:
    best = INF
    depth += 1

    # if leaf aka if game over
    if board.is_game_over():
        return INF  # max has won
    if depth > max_depth:
        # return score_with_rivalry(board, MIN)
        return score(board, MIN)

    moves = get_possible_moves(board)
    for move in moves:
        move.do(board, MIN)
        best = min(best, max_value(board, lower, upper, max_depth, depth))
        move.undo(board)

        upper = min(upper, best)
        if lower >= upper:
            return best  # alpha cutoff, a>=b

    return best

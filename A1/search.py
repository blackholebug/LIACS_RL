# see https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#cite_note-RN03-12
# and Russel and Norvig Artificial inteligence p. 170
import time
from typing import Optional

from move import Move, possible_moves
from board import HexBoard
from evaluate import score

MIN = HexBoard.RED
MAX = HexBoard.BLUE
INF: int = 99999


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
    timer = Timer(5.0)

    while not timer.time_is_up():
        best_move = lower_upper_search(board, max_depth=depth)
        depth += 1

    return best_move


# the alpha beta algorithm or as we prefer to call
# it lower upper almost a copy of max value but
# returns the move with the highest score, currently
# only the MAX player can use lower_upper
def lower_upper_search(board: HexBoard, max_depth: int = INF) -> Optional[Move]:
    best = -INF
    lower = INF
    upper = -INF
    depth = 0

    best_move_score = -INF
    best_move_action = None
    for move in possible_moves(board):
        move.do(board, MAX)
        best = max(best, max_value(board, lower, upper, max_depth, depth))
        if best >= best_move_score:
            best_move_score = best
            best_move_action = move
        move.undo(board)
        lower = max(lower, best)  # update lower bound
        if best >= upper:
            break  # beta cutoff, a>=b

    return best_move_action


def max_value(
    board: HexBoard, lower: int, upper: int, max_depth: int, depth: int
) -> int:
    best = -INF
    depth += 1
    if depth > max_depth:
        return score(board, MAX)
    for move in possible_moves(board):
        move.do(board, MAX)
        best = max(best, min_value(board, lower, upper, max_depth, depth))
        move.undo(board)
        lower = max(lower, best)  # update lower bound alpha
        if best >= upper:
            return best  # beta cutoff, a>=b
    return best


def min_value(
    board: HexBoard, lower: int, upper: int, max_depth: int, depth: int
) -> int:
    best = INF
    depth += 1
    if depth > max_depth:
        return score(board, MIN)
    for move in possible_moves(board):
        move.do(board, MIN)
        best = min(best, max_value(board, lower, upper, max_depth, depth))
        move.undo(board)
        if lower >= best:
            return best  # alpha cutoff, a>=b
        upper = min(upper, best)
    return best

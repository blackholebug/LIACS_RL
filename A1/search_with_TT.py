# see https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#cite_note-RN03-12
# and Russel and Norvig Artificial inteligence p. 170
import numpy as np
import time
from typing import Optional

from move import Move, possible_moves
from board import HexBoard
import evaluate
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

def get_empty(board: HexBoard) -> int:
    count = 0
    for move in board.board:
        if board.board[move] == HexBoard.EMPTY:
            count += 1
    return count

def iterative_deeping_with_TT(board: HexBoard) -> Optional[Move]:
    depth = 1
    timer = Timer(5.0)
    # add this to trigger transposition table
    ttable = {"is_use": 1}

    while not timer.time_is_up() and depth <= get_empty(board):
        best_move = lower_upper_search(
            board, max_depth=depth, memory=ttable)
        depth += 1
    return best_move


def update_transposition_table(board: HexBoard, memory: dict, remaining_depth: int, score: int,
                               best_move: tuple, is_score: bool = False, is_bound: bool = False):
    current_board = list()
    current_status = {
        "score": score,
        "remaining_depth": remaining_depth,
        "best_move": best_move,
    }

    for k, v in board.board.items():
        current_board.append((k, v))
    key = (*current_board,)
    memory[key] = current_status
    # print("updated")


def query_transposition_table(board: HexBoard, memory: dict, current_remaining_depth: int) -> Optional[dict]:
    record = None
    current_board = list()
    for k, v in board.board.items():
        current_board.append((k, v))
    key = (*current_board,)
    if key in memory:
        record = memory[key]
        # print("hit")
    return record


# the alpha beta algorithm or as we prefer to call
# it lower upper almost a copy of max value but
# returns the move with the highest score, currently
# only the MAX player can use lower_upper
def lower_upper_search(board: HexBoard, max_depth: int = INF, memory: dict = None) -> Optional[Move]:

    lower = -INF
    upper = INF
    depth = 0

    best_overal_score = -INF
    best_overal_move = None
    empty_pos = possible_moves(board)
    # Query transposition table
    if memory:
        record = query_transposition_table(board, memory, max_depth)
        if record:
            # search best move first
            best_move = record['best_move']
            if best_move and not empty_pos and empty_pos[0] != best_move:
                empty_pos.remove(best_move)
                empty_pos.insert(0, best_move)

    for move in empty_pos:
        move.do(board, MAX)
        subtree_score = min_value(
            board, lower, upper, max_depth, depth, memory)
        move.undo(board)
        if subtree_score >= best_overal_score:
            best_overal_score = subtree_score
            best_overal_move = move
            if memory:
                update_transposition_table(
                    board, memory, max_depth, best_overal_score, best_overal_move)

    return best_overal_move


def max_value(board: HexBoard, lower: int, upper: int, max_depth: int, depth: int, memory: dict = None) -> int:
    best = -INF
    depth += 1
    remaining_depth = max_depth - depth
    empty_pos = possible_moves(board)

    # if leaf aka if game over
    if board.is_game_over():
        return -INF  # min player wins

    # Query transposition table
    if memory:
        record = query_transposition_table(board, memory, remaining_depth)
        if record:
            if record['remaining_depth'] >= remaining_depth:
                best = record["score"]
                return best
            else:
                # search best move first
                best_move = record['best_move']
                if best_move and not empty_pos and empty_pos[0] != best_move:
                    empty_pos.remove(best_move)
                    empty_pos.insert(0, best_move)

    if depth >= max_depth:
        eval_score = evaluate.score(board, MAX)
        if memory:
            update_transposition_table(
                board, memory, remaining_depth, eval_score, None)
        return eval_score

    for move in empty_pos:
        move.do(board, MAX)
        current = min_value(board, lower, upper, max_depth, depth, memory)
        move.undo(board)
        if current > best:
            best = current
            if memory:
                update_transposition_table(
                    board, memory, remaining_depth, best, move)

        lower = max(lower, best)  # update lower bound alpha
        if lower >= upper:  # NOTE: change best to lower
            return best  # beta cutoff, a>=b

    return best


def min_value(board: HexBoard, lower: int, upper: int, max_depth: int, depth: int, memory: dict = None) -> int:
    best = INF
    depth += 1
    remaining_depth = max_depth - depth
    empty_pos = possible_moves(board)

    # if leaf aka if game over
    if board.is_game_over():
        return -INF  # min player wins

    # Query transposition table
    if memory:
        record = query_transposition_table(board, memory, remaining_depth)
        if record:
            if record['remaining_depth'] >= remaining_depth:
                best = record["score"]
                return best
            else:
                # search best move first
                best_move = record['best_move']
                if best_move and not empty_pos and empty_pos[0] != best_move:
                    empty_pos.remove(best_move)
                    empty_pos.insert(0, best_move)

    if depth >= max_depth:
        eval_score = evaluate.score(board, MIN)
        if memory:
            update_transposition_table(
                board, memory, remaining_depth, eval_score, None)
        return eval_score

    for move in possible_moves(board):
        move.do(board, MIN)
        current = max_value(board, lower, upper, max_depth, depth, memory)
        move.undo(board)
        if current < best:
            best = current
            if memory:
                update_transposition_table(
                    board, memory, remaining_depth, best, move)

        upper = min(upper, best)  # update upper bound beta
        if lower >= upper:  # NOTE: change best to upper
            return best  # alpha cutoff, a>=b

    return best

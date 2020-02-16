import operator
from board import HexBoard
from typing import List


class Move(tuple):
    def __new__(self, x, y):
        self.x = property(operator.itemgetter(0))
        self.y = property(operator.itemgetter(1))
        return tuple.__new__(Move, (x, y))

    def do(self, board: HexBoard, color: int):
        board.board[self] = color
        if board.check_win(color):
            board.game_over = True

    def undo(self, board: HexBoard):
        board.board[self] = HexBoard.EMPTY
        board.game_over = False


def possible_moves(board: HexBoard) -> List[Move]:
    moves = []
    for y in range(board.size):
        for x in range(board.size):
            if board.board[x, y] == HexBoard.EMPTY:
                moves.append(Move(x, y))

    return moves

# simple expl: https://www.youtube.com/watch?v=2MNalT1g3m8

from board import HexBoard
from move import get_possible_moves

from search import MIN

if __name__ == "__main__":
    # replace by interactive menu/input
    # and tests moved to test_.py
    board = HexBoard(4)
    move = get_possible_moves(board)[0]
    board.place((move.x, move.y), MIN)

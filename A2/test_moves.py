import numpy as np
from board import HexBoard
from evaluate import player_direction
from move import Move, get_possible_moves

# sanity check that playing using get_possible_moves list will end at some point


def test_random():
    endable_board = HexBoard(4)
    while not endable_board.game_over:
        moves = get_possible_moves(endable_board)
        move = moves[np.random.randint(0, len(moves))]
        endable_board.place(move, HexBoard.RED)

    assert endable_board.game_over
    assert endable_board.check_win(HexBoard.RED)
    assert not endable_board.check_win(HexBoard.BLUE)


# sanity check that possible moves decrease if a piece is placed
# and it has the right length during that time
def test_len():
    board = HexBoard(4)
    moves = get_possible_moves(board)
    assert len(moves) == 16

    n_placed = 0
    for x in range(0, 4):
        for y in range(0, 4):
            moves = get_possible_moves(board)
            board.place(moves[0], HexBoard.RED)
            # set game over to false to prevent place from
            # no longer working when a line has completed
            board.game_over = False
            assert len(moves) == 16 - n_placed
            n_placed += 1

    moves = get_possible_moves(board)
    assert len(moves) == 0


# test that do and undo work by testing if game_over is detected
def test_do():
    board = HexBoard(4)
    Move(0, 2).do(board, HexBoard.BLUE)
    Move(1, 2).do(board, HexBoard.BLUE)
    Move(2, 2).do(board, HexBoard.BLUE)
    Move(3, 2).do(board, HexBoard.BLUE)
    board.print()
    assert board.game_over

    Move(3, 2).undo(board)
    Move(2, 2).undo(board)
    assert not board.game_over

    Move(3, 2).do(board, HexBoard.BLUE)
    assert not board.game_over

    Move(2, 2).do(board, HexBoard.RED)
    assert not board.game_over

    # do does no no check if position was
    # taken thus this is possible
    Move(2, 2).do(board, HexBoard.BLUE)
    assert board.game_over
    assert player_direction(HexBoard.BLUE) == "left right"
    assert board.check_win(HexBoard.BLUE)


if __name__ == "__main__":
    test_do()

# file must by named "test_" as pytest will run all files of the form
# test_*.py or *_test.py in its current directory
import numpy as np
from board import HexBoard

# sanity check that wins are detected
def test_wins():
    for i in range(0, 2):
        winner = HexBoard.RED if i == 0 else HexBoard.BLUE
        loser = HexBoard.BLUE if i == 0 else HexBoard.RED
        board = HexBoard(3)
        board.place((1, 1), loser)
        board.place((2, 1), loser)
        board.place((1, 2), loser)
        board.place((2, 2), loser)
        board.place((0, 0), winner)
        board.place((1, 0), winner)
        board.place((2, 0), winner)
        board.place((0, 1), winner)
        board.place((0, 2), winner)
        assert board.check_win(winner)
        assert not board.check_win(loser)
        board.print()


# sanity check that random play will at some point end the game
def test_random():
    endable_board = HexBoard(4)
    while not endable_board.game_over:
        endable_board.place(
            (np.random.randint(0, 4), np.random.randint(0, 4)), HexBoard.RED
        )
    assert endable_board.game_over
    assert endable_board.check_win(HexBoard.RED)
    assert not endable_board.check_win(HexBoard.BLUE)
    print("Randomly filled board")
    endable_board.print()


# test if get_neighbors works
def test_neighbor():
    neighbor_check = HexBoard(5)
    assert neighbor_check.get_neighbors((0, 0)) == [(1, 0), (0, 1)]
    assert neighbor_check.get_neighbors((0, 1)) == [(1, 1), (1, 0), (0, 2), (0, 0)]
    assert neighbor_check.get_neighbors((1, 1)) == [
        (0, 1),
        (2, 1),
        (0, 2),
        (2, 0),
        (1, 2),
        (1, 0),
    ]
    assert neighbor_check.get_neighbors((3, 4)) == [(2, 4), (4, 4), (4, 3), (3, 3)]
    assert neighbor_check.get_neighbors((4, 3)) == [(3, 3), (3, 4), (4, 4), (4, 2)]
    assert neighbor_check.get_neighbors((4, 4)) == [(3, 4), (4, 3)]
    neighbor_check_11 = HexBoard(5)
    assert neighbor_check_11.get_neighbors((4, 4)) == [(3, 4), (4, 3)]

    neighbor_check_small = HexBoard(2)
    assert neighbor_check_small.get_neighbors((0, 0)) == [(1, 0), (0, 1)]
    assert neighbor_check_small.get_neighbors((1, 0)) == [(0, 0), (0, 1), (1, 1)]
    assert neighbor_check_small.get_neighbors((0, 1)) == [(1, 1), (1, 0), (0, 0)]
    assert neighbor_check_small.get_neighbors((1, 1)) == [(0, 1), (1, 0)]

    neighbor_check_sanity = HexBoard(11)
    for x in range(0, 11):
        for y in range(0, 11):
            neighbors = neighbor_check_sanity.get_neighbors((x, y))
            for neighbor in neighbors:
                neighbors_neighbors = neighbor_check_sanity.get_neighbors(neighbor)
                index_of_self = neighbors_neighbors.index((x, y))
                assert index_of_self != -1

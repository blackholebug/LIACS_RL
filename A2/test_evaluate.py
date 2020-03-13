import evaluate
from board import HexBoard


def creat_board_blue_uncon(winner: int, loser: int) -> HexBoard:
    board = HexBoard(3)
    board.place((0, 2), winner)
    board.place((1, 1), loser)
    board.place((1, 0), winner)
    board.place((2, 1), loser)
    board.place((0, 1), winner)
    board.place((2, 2), loser)
    board.place((2, 0), winner)
    board.place((1, 2), loser)
    return board


def creat_board_252(winner: int, loser: int) -> HexBoard:
    board = HexBoard(6)
    board.place((1, 1), winner)
    board.place((0, 2), loser)
    board.place((5, 0), winner)
    board.place((2, 1), loser)
    board.place((0, 3), winner)
    board.place((2, 2), loser)
    board.place((4, 0), winner)
    board.place((1, 2), loser)
    return board


def creat_board_20(winner: int, loser: int) -> HexBoard:
    board = HexBoard(3)
    board.place((1, 1), winner)
    board.place((0, 2), loser)

    return board


def test_score():
    winner = HexBoard.RED
    loser = HexBoard.BLUE

    board = creat_board_blue_uncon(winner, loser)
    assert evaluate.score_with_rivalry(
        board, winner) == -99991  # -99991 = 4*2 -99999

    board = creat_board_20(winner, loser)
    assert evaluate.score_with_rivalry(board, winner) == 20  # 20 = 20*2-20

    board = creat_board_252(winner, loser)
    assert evaluate.score_with_rivalry(board, winner) == 252  # 252 = 182*2-112


def test_direction():
    blue_dir = evaluate.player_direction(HexBoard.BLUE)
    red_dir = evaluate.player_direction(HexBoard.RED)

    assert blue_dir == "left right"
    assert red_dir == "top bottem"


if __name__ == "__main__":
    winner = HexBoard.RED  # 2
    loser = HexBoard.BLUE  # 1
    board = creat_board_20(winner, loser)
    board.print()
    print(evaluate.score_with_rivalry(board, winner))

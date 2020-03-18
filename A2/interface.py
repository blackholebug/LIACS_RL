from board import HexBoard
import re
from itertools import product
import search_with_TT as st


def to_move(c):
    column, row = int(c[:-1]), ord(c[-1]) - ord('a')
    return (row, column)


def player_human(board: HexBoard) -> tuple:
    # query the user until receving a (pseudo) legal move.
    move = None
    while True:
        match = re.match('([0-9][0-9]*[a-z])',
                         input('Your move (e.g. 2b): \n >>> '))
        if match:
            move = to_move(match.group(0))
            if move in product(range(board.size), range(board.size)) and board.board[move] == HexBoard.EMPTY:
                return move
            else:
                print("Input error: please enter a correct coordinate again")
        else:
            print("Input error: please enter a move like 2b")
    return move


def player_machine(board: HexBoard, memory: dict) -> tuple:
    # search the board for the next move
    move = st.lower_upper_search(board, max_depth=4, memory=memory)
    # move = st.iterative_deeping_with_TT(board)
    return move


def main():
    test_board = HexBoard(int(input("Enter the size of board as a number: ")))
    print("""Please select a game mode: \n
             \t Mode 1 ...... human vs human \n
             \t Mode 2 ...... human vs machine(alpha-beta) \n
             \t Mode 3 ...... machine(random) vs machine(alpha-beta) \n
          """)
    mode = input(
        "Wich mode do you want to play? Please enter a number: \n >>> ")
    assert mode == '1' or mode == '2' or mode == '3'
    test_board.print()

    is_first_player = True
    tt = {"is_use": 1}

    while True:
        # first player use BLUE, second player use RED
        player = HexBoard.BLUE if is_first_player else HexBoard.RED
        player_name = "1" if is_first_player else "2"
        # game play
        print(f"Player {player_name} move")
        if mode == '1':
            if is_first_player:
                print("(Your direction: left-right)")
            else:
                print("(Your direction: top-bottom)")
            move = player_human(test_board)
            test_board.place(move, player)
            test_board.print()
        elif mode == '2':
            # NOTE: human plays first by default
            if is_first_player:
                print("(Your direction: left-right)")
            else:
                print("(Your direction: top-bottom)")
            move = player_human(test_board) if is_first_player else player_machine(test_board, tt)
            test_board.place(move, player)
            test_board.print()
        elif mode == '3':
            move = player_machine(test_board)
            test_board.place(move, player)
            test_board.print()
        # Check win
        if test_board.is_game_over():
            print(f"Player {player_name} win!")
            break
        else:
            # change player if not win
            is_first_player = False if is_first_player else True


if __name__ == '__main__':
    main()

import random
from hex_skeleton import HexBoard
import re
import typing
from itertools import product

def to_move(c):
    row, column = int(c[:-1]), ord(c[-1]) - ord('a')
    return (row, column)

def player_human(board: HexBoard) -> tuple:
    # query the user until receving a (pseudo) legal move.
    move = None
    while True:
        match = re.match('([0-9][0-9]*[a-z])', input('Your move: '))
        if match:
            move = to_move(match.group(0))
            if move in product(range(board.size), range(board.size))\
                and board.board[move] == HexBoard.EMPTY:
                return move
            else:
                print("Please enter a correct coordinate again")
        else:
            print("Please enter a move like 2b")

    return move

def player_machine(board: HexBoard) -> tuple:
    # search the board for the next move
    move = None
    return move

def main():
    test_board = HexBoard(int(input("Enter the size of board as a number: ")))
    print("""Please select a game mode: \n
             \t Mode 1 ...... human vs human \n
             \t Mode 2 ...... human vs machine(alpha-beta) \n
             \t Mode 3 ...... machine(random) vs machine(alpha-beta) \n
          """)
    mode = input("Wich mode do you want to play? Please enter a number: ")
    test_board.print()

    is_fristplayer = True
    while True:
        # first player use BLUE, second player use RED
        player = HexBoard.BLUE if is_fristplayer else HexBoard.RED
        # game play
        print(f"Player {1+int(not is_fristplayer)} move:")
        if mode == '1':
            move = player_human(test_board)
            test_board.place(move, player)
            test_board.print()
        elif mode == '2':
            # NOTE: human plays first by default
            move = player_human(test_board) if is_fristplayer else player_machine(test_board)
            test_board.place(move, player)
            test_board.print()
        elif mode == '3':
            move = player_machine(test_board)
            test_board.place(move, player)
            test_board.print()
        # Check win
        if test_board.is_game_over() == True:
            print(f"Player {1+int(not is_fristplayer)} win!")
            break
        else:
            # change player if not win
            is_fristplayer = False if is_fristplayer == True else True

if __name__ == '__main__':
    main()


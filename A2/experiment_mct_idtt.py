from board import HexBoard
from search import MAX, MIN
import matplotlib.pyplot as plt
import trueskill as ts
import numpy as np
from elo_score_mcts import update_trueskill, calculate_trueskill
from A2.search_with_TT import lower_upper_search
from MCTS_search import MCTS as mcts_func
import os
# import time


def player1_vs_player2(size: int, player1_name: str, player2_name: str,
                       ab_memory=False, matches=12, mcts_max_iter=3):
    np.random.seed(666)
    init = 25
    player1 = ts.Rating(init)
    player2 = ts.Rating(init)

    if ab_memory:
        tt = {"is_use": 1}
        is_tt = 'ab_with_tt'
    else:
        tt = None
        is_tt = 'ab_without_tt'

    player1_scores = [0]
    player2_scores = [0]
    for i in range(matches):
        board = HexBoard(size)
        while True:
            if player1_name == 'MCTS':
                first_move = mcts_func(board, mcts_max_iter)
            elif player1_name == 'depth3':
                first_move = lower_upper_search(board, 3, memory=tt)
            elif player1_name == 'depth4':
                first_move = lower_upper_search(board, 4, memory=tt)

            board.place(first_move, MAX)
            if board.game_over:
                player1, player2 = update_trueskill(player1, player2, True)
                player1_scores.append(calculate_trueskill(player1))
                player2_scores.append(calculate_trueskill(player2))
                print(f"{player1_name} win!")
                break

            if player2_name == 'MCTS':
                second_move = mcts_func(board, mcts_max_iter)
            elif player2_name == 'depth3':
                second_move = lower_upper_search(board, 3)
            elif player2_name == 'depth4':
                second_move = lower_upper_search(board, 4)

            board.place(second_move, MIN)
            if board.game_over:
                player1, player2 = update_trueskill(player1, player2, False)
                player1_scores.append(calculate_trueskill(player1))
                player2_scores.append(calculate_trueskill(player2))
                print(f"{player2_name} win!")
                break

    plt.plot(range(matches + 1), player1_scores, label=player1_name)
    plt.plot(range(matches + 1), player2_scores, label=player2_name)
    plt.legend(loc='upper right')
    plt.xlabel('matches')
    plt.ylabel('score')
    plt.title('Trueskill score')

    plt.savefig(f'{dir_name}/{player1_name}-{player2_name}-{is_tt}-{matches}.png')
    plt.show()
    print(f"{player1_name} score: {player1_scores} \n {player2_name} score: {player2_scores}")


if __name__ == "__main__":

    # Vary the experiment settings here. from line 77-80
    num_matches = 20  # NOTE: in Trueskill original package 12 is suggested
    is_ab_memory = True
    num_mcts_iter = 10000
    board_size = 6

    mct_iter = f'mct_{num_mcts_iter}'

    if is_ab_memory:
        is_tt = 'ab_with_idtt'
    else:
        is_tt = 'ab_no_idtt'

    dir_name = f'Elo-result/board{board_size}-{num_matches}s-{is_tt}-{mct_iter}'
    os.mkdir(dir_name)

    depth3 = "depth3"
    depth4 = "depth4"
    MCTS = 'MCTS'

    # MCTS to play against alpha-beta depth3 and depth4
    player1_vs_player2(board_size, MCTS, depth3,
                       ab_memory=is_ab_memory, matches=num_matches, mcts_max_iter=num_mcts_iter)
    player1_vs_player2(board_size, depth3, MCTS,
                       ab_memory=is_ab_memory, matches=num_matches, mcts_max_iter=num_mcts_iter)
    player1_vs_player2(board_size, MCTS, depth4,
                       ab_memory=is_ab_memory, matches=num_matches, mcts_max_iter=num_mcts_iter)
    player1_vs_player2(board_size, depth4, MCTS,
                       ab_memory=is_ab_memory, matches=num_matches, mcts_max_iter=num_mcts_iter)


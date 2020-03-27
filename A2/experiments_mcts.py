from board import HexBoard
# from search_with_TT import MAX, MIN
from search import MAX, MIN
import matplotlib.pyplot as plt
import trueskill as ts
import numpy as np
# import time
from elo_score_mcts import update_trueskill, calculate_trueskill, get_moves

def player1_vs_player2(size: int, player1_name: str, player2_name: str):
    np.random.seed(666)
    init = 25
    player1 = ts.Rating(init)  # 创建ts中的类对象
    player2 = ts.Rating(init)

    matches = 20  # NOTE: 12 is suggested

    player1_scores = [0]
    player2_scores = [0]
    for i in range(matches):
        board = HexBoard(size)
        while True:

            first_move = get_moves(board, player1_name)
            board.place(first_move, MAX)
            if board.game_over:  # 每次判断，如果游戏结束就：更新双方得分 + break（不再继续下棋）
                player1, player2 = update_trueskill(player1, player2, True)
                player1_scores.append(calculate_trueskill(player1))
                player2_scores.append(calculate_trueskill(player2))
                print(f"{player1_name} win!")
                break

            second_move = get_moves(board, player2_name)
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
    plt.savefig(f'../../A2/tt_13/{player1_name}-{player2_name}.png')
    plt.show()
    print(f"{player1_name} score: {player1_scores} \n {player2_name} score: {player2_scores}")

if __name__ == "__main__":

    depth3 = "depth3"
    depth4 = "depth4"
    MCTS = 'MCTS'

    tt = {"is_use": 1}

    player1_vs_player2(3, depth3, MCTS)
    player1_vs_player2(3, MCTS, depth3)
    player1_vs_player2(3, depth4, MCTS)
    player1_vs_player2(3, MCTS, depth4)

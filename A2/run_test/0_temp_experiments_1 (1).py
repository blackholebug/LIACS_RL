# -*- coding: utf-8 -*-
"""RL_A2_N_Cp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1poWqnGxWB_nC01aZClxgRunEAUYzEvwe
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import math
import copy

from board import HexBoard
from move import get_possible_moves
from utils import MAX, MIN, INF, player_color, player_direction
from MCTS import Node
from search_mcts import expand, random_play

ntrials = 60     # number of MCST-vs-Random_Player trials for each (N, Cp)
N_vec = [5000]    # all N (max iterations) values to be investigated
SIZE = 9          # board size
k_intervals = 20
Cp_vec = [0.5]  # all Cp values to be investigated

def UCT_select(node, Cp):
    # initialize variables to be updated
    best_score = -INF
    best_sub_node = None
    # traverse every child of the node
    for sub_node in node.get_children():
        # compute UCT Score for this candidate child
        left = sub_node.get_quality_value() / sub_node.get_visit_times()
        right = math.log(node.get_visit_times()) / sub_node.get_visit_times()
        score = left + Cp * math.sqrt(right)
        # update
        if score > best_score:
            best_sub_node = sub_node
            best_score = score
    return best_sub_node

def MCTS_N_Cp(board, N, Cp):

    root_node = Node()
    root_node.set_state(board)

    for i in range(N):
        current_node = root_node
        # select
        while not current_node.get_state().is_game_over():
            if current_node.is_all_expand():
                current_node = UCT_select(current_node, Cp)
            else:
                current_node = expand(current_node)
                break
        # play out
        current_state = current_node.get_state()
        play_board = copy.deepcopy(current_state)
        play_color = current_node.get_move_color()
        while not play_board.is_game_over():
            play_color = MIN if play_color==MAX else MAX
            random_play(play_board, play_color)
        reward = 1 if play_board.check_win(MAX) else 0
        # back propagation
        while current_node != None:
            current_node.visit_times_add_one()
            current_node.quality_value_add_n(reward)
            current_node = current_node.parent
    
    # get best move after iteration
    selected_node = UCT_select(root_node, Cp)
    next_move = selected_node.get_last_move()
    
    return next_move

def Sim_MCTS_Random(size, N, Cp):

    board = HexBoard(size)

    while True:
        # MCST moves
        best_move = MCTS_N_Cp(board, N, Cp)
        board.place(best_move, MAX)
        # game over or not
        if board.game_over:
            break
        # Random Player moves
        moves = get_possible_moves(board)
        random_move = moves[np.random.randint(0, len(moves))]
        board.place(random_move, MIN)
        # game over or not
        if board.game_over:
            break

    # return 1 if MCST wins and return 0 if loses
    if board.check_win(MAX):
        return 1
    else:
        return 0

# store in a dictionary the experiment results
D_vsRandom = {"Cp":Cp_vec} 

for N in N_vec:
    win_rate = list()
    for Cp in Cp_vec:
        win_count = 0
        for t in range(ntrials):
            win_count += Sim_MCTS_Random(SIZE, N, Cp)
        win_rate.append(win_count/ntrials)
    # add a new column to the dataframe for each new N

win_rate_array = np.array(win_rate)
np.savetxt('res_1.csv', win_rate_array, delimiter=',')


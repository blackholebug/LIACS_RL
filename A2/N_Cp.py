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
from time import process_time

from board import HexBoard
from move import get_possible_moves
from utils import MAX, MIN, INF, player_color, player_direction
from MCTS import Node
from search_mcts import expand, random_play


####################################################################
#Define Functions
####################################################################


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
            current_node.add_visit_times()
            current_node.add_quality_value(reward)
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

    
##########################################################################
#Preliminary Trials
##########################################################################


# explore the convergence of win rate for (N=500, Cp=1) on a 5-by-5 board
win_rate = list()
win_count = 0
for t in range(100):
    win_count += Sim_MCTS_Random(5, 500, 1)
    win_rate.append(win_count/(t+1))
# plot the dynamic win rate as the number of simulations increases
plt.figure()
plt.plot([t+1 for t in range(100)], win_rate)
plt.title("Asymptotic Property of Win Rate")
plt.xlabel("Number of Simulations")
plt.ylabel("Win Rate of MCTS")
plt.ylim(0.8,1.05)
plt.vlines(x=60, ymin=0.8, ymax=1, colors="r", linestyles=":")
plt.hlines(y=win_rate[60], xmin=1, xmax=100, colors="y", linestyles=":")
plt.savefig("Win_Rate_Convergence.eps")
plt.show()


# explore the computational cost of doing experiments
# estimate the average time for a play-out against random player with respect to N and board size

size_vec = [5, 6, 7, 8, 9]
N_vec = [500, 1000, 3000, 5000]
TIME = {"Board Size":size_vec}

for N in N_vec:
    time = list()
    for size in size_vec:
        t1 = process_time()
        for i in range(10):                  # simulate 10 play-outs and output the average time
            Sim_MCTS_Random(size, N, 1)
        t2 = process_time()
        delta = round((t2-t1)/10, 2)
        time.append(str(delta)+" seconds")
    TIME["N="+str(int(N))] = time

DF = pd.DataFrame(TIME)
print(DF)
print(DF.to_latex(column_format="lc"+"r"*len(N_vec)))
DF.to_csv("Preliminary_Time.csv", encoding='utf-8')



########################################################
# Parameters
########################################################


ntrials = 60     # number of MCST-vs-Random_Player trials for each (N, Cp)
SIZE = 6          # board size
k_intervals = 20  
Cp_vec = np.linspace(0.5, 1.5, 1+k_intervals)  # all Cp values to be investigated


#########################################################
# Experiments
#########################################################


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
    D_vsRandom["N="+str(int(N))] = win_rate

    
DF = pd.DataFrame(D_vsRandom)
# print out the experiment results in LaTex format
print(DF.to_latex(column_format="lc"+"r"*len(N_vec)))
# save the experiment results as a dataframe
DF.to_csv("N_Cp_9.csv", encoding='utf-8')

    
# plot the experiment results: MCTS vs Randam Player
fig, axs = plt.subplots(2, 2, figsize=(10,10))
fig.suptitle('MCTS vs Random Player: '+str(int(SIZE))+"-by-"+str(int(SIZE))+" Board")
for i in range(2):
    for j in range(2):
        N = int(N_vec[2*i+j])
        axs[i,j].plot(Cp_vec, D["N="+str(N)])
        axs[i,j].set_title("N = "+str(N))
        axs[i,j].set_xlabel('Cp')
        axs[i,j].set_ylabel('Win Rate')
        axs[i,j].set_ylim(0.85, 1.01)
        plt.savefig("vsRandom.eps")


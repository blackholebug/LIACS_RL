import copy
import random
import math

from board import HexBoard
from MCTS import Node

from utils import MAX, MIN, INF, player_color
from move import get_possible_moves


def select(node, is_exploration):
    """select operation
    
    Arguments:
        node {Node} -- a node object as root node
        is_exploration {bool} -- judge if iterations are completed or not
    
    Returns:
        best_sub_node {Node} -- the selected sub node
    """    
    best_score = -INF
    best_sub_node = None

    # Travel all sub nodes to find the best one
    for sub_node in node.get_children():

        # UCT Selection formular
        if is_exploration:
            C = 1 / math.sqrt(2.0)
            to_sqrt = 2.0 * math.log(node.get_visit_times()) / sub_node.get_visit_times()
            # UCT score
            score = sub_node.get_quality_value() / sub_node.get_visit_times() + C * math.sqrt(to_sqrt)

        # Choose the most frequently visited nodes
        else:
            score = sub_node.get_visit_times()

        if score > best_score:
            best_sub_node = sub_node
            best_score = score

    return best_sub_node


def expand(node):
    """expand operation
    
    Arguments:
        node {Node} -- a node object to expand
    
    Returns:
        sub_node {Node} -- a node object as the expanded subnode
    """    
    tried_sub_node_moves = [
        sub_node.get_last_move() for sub_node in node.get_children()
    ]

    possible_moves = get_possible_moves(node.get_state())
    new_move = random.choice(possible_moves)

    # Make sure new move has not been tried before
    while new_move in tried_sub_node_moves:
        new_move = random.choice(possible_moves)

    sub_node = Node()
    # Create a deepcopy of board from parent
    new_state = copy.deepcopy(node.get_state())
    # Update the move color of new status
    if node.get_move_color() == None:
        move_color = MAX
    else:
        move_color = MAX if node.get_move_color() == MIN else MIN
    sub_node.set_move_color(move_color)
    # Do move on new status
    new_state.place(new_move, move_color)
    # Update last move of new status
    sub_node.set_last_move(new_move)  # TODO: make a sub class of HexBoard; integrate set_last_move()
    # attach the new status to sub node
    sub_node.set_state(new_state)
    # add child to parent
    node.add_child(sub_node)

    return sub_node


def random_play(board, color):
    """randomly play on a temperary board
    
    Arguments:
        board {HexBoard} -- A provided board
        color {int} -- color of last move
    """    
    possible_moves = get_possible_moves(board)
    new_move = random.choice(possible_moves)
    board.place(new_move, color)


def mcts_search(board, max_iter):
    """mcts search function
    
    Arguments:
        board {HexBoard} -- a HexBoard object as the original state
        max_iter {int} -- number of max iteration 
    
    Returns:
        next_move {tuple} -- the coordinate of predicted best move
    """    
    root_node = Node()
    root_node.set_state(board)

    for i in range(max_iter):
        current_node = root_node

        # Select
        while not current_node.get_state().is_game_over():
            # Go deep in the search tree when all subnodes are expanded
            if current_node.is_all_expand():
                current_node = select(current_node, True)
            # Expand
            else:
                # Update the current node to a new sub node when finding a node not fully expanded
                current_node = expand(current_node)
                break

        # Play-out
        current_state = current_node.get_state()
        play_board = copy.deepcopy(current_state)
        play_color = current_node.get_move_color()
        # Play randomly until the game over
        while not play_board.is_game_over():
            # Change the piece color
            play_color = MIN if play_color == MAX else MAX
            random_play(play_board, play_color)
        reward = 1 if play_board.check_win(MAX) else 0

        # Back propagation
        while current_node != None:
            # Update the visit times
            current_node.add_visit_times()
            # Update the quality value
            current_node.add_quality_value(reward)
            # Change the node to the parent node
            current_node = current_node.parent

    # After the iteration, get best move
    selected_node = select(root_node, False)
    next_move = selected_node.get_last_move()
    return next_move
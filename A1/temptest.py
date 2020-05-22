import numpy as np

from board import HexBoard
from move import possible_moves
from search_with_TT import lower_upper_search, player_color, MAX, MIN
from evaluate import player_direction

board = HexBoard(4)

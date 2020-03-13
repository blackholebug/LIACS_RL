from utils import MAX, MIN, INF, player_color
import move

class Node(object):
    def __init__(self):
        self.parent = None
        self.children = []

        self.visit_times = 0
        self.quality_value = 0.0

        self.state = None
        self.last_move = None
        self.move_color = MAX

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_last_move(self, last_move):
        self.last_move = last_move

    def get_last_move(self):
        return self.last_move

    def set_move_color(self, move_color):
        self.move_color = move_color

    def get_move_color(self):
        return self.move_color

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def get_visit_times(self):
        return self.visit_times

    def set_visit_times(self, times):
        self.visit_times = times

    def visit_times_add_one(self):
        self.visit_times += 1

    def get_quality_value(self):
        return self.quality_value

    def set_quality_value(self, value):
        self.quality_value = value

    def quality_value_add_n(self, n):
        self.quality_value += n

    def is_all_expand(self):
        return len(self.children) == len(move.get_possible_moves(self.state))

    def add_child(self, sub_node):
        sub_node.set_parent(self)
        self.children.append(sub_node)

    def __repr__(self):
        return "Node: {}, Q/N: {}/{}, state: {}".format(
            hash(self), self.quality_value, self.visit_times, self.state)
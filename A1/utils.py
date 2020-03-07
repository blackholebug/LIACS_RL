from board import HexBoard

MIN = HexBoard.RED
MAX = HexBoard.BLUE
INF: int = 99999


def player_color(player: int) -> str:
    if player == HexBoard.BLUE:
        return "BLUE"
    else:
        return "RED"


def player_direction(player: int) -> str:
    if player == HexBoard.BLUE:
        return "left right"
    else:
        return "top bottem"

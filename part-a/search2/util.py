from search2.Constants import *
from search2.Board import *

from copy import deepcopy


"""
This module contains some helper functions for printing actions and boards.
Feel free to use and/or modify them to help you develop your program.
"""

def print_move(n, x_a, y_a, x_b, y_b, **kwargs):
    """
    Output a move action of n pieces from square (x_a, y_a)
    to square (x_b, y_b), according to the format instructions.
    """
    print("MOVE {} from {} to {}.".format(n, (x_a, y_a), (x_b, y_b)), **kwargs)


def print_boom(x, y, **kwargs):
    """
    Output a boom action initiated at square (x, y) according to
    the format instructions.
    """
    print("BOOM at {}.".format((x, y)), **kwargs)


def print_board(board_dict, message="", unicode=False, compact=True, **kwargs):
    """
    For help with visualisation and debugging: output a board diagram with
    any information you like (tokens, heuristic values, distances, etc.).

    Arguments:
    board_dict -- A dictionary with (x, y) tuples as keys (x, y in range(8))
        and printable objects (e.g. strings, numbers) as values. This function
        will arrange these printable values on the grid and output the result.
        Note: At most the first 3 characters will be printed from the string
        representation of each value.
    message -- A printable object (e.g. string, number) that will be placed
        above the board in the visualisation. Default is "" (no message).
    unicode -- True if you want to use non-ASCII symbols in the board
        visualisation (see below), False to use only ASCII symbols.
        Default is False, since the unicode symbols may not agree with some
        terminal emulators.
    compact -- True if you want to use a compact board visualisation, with
        coordinates along the edges of the board, False to use a bigger one
        with coordinates alongside the printable information in each square.
        Default True (small board).

    Any other keyword arguments are passed through to the print function.
    """
    if unicode:
        if compact:
            template = """# {}
#    ┌───┬───┬───┬───┬───┬───┬───┬───┐
#  7 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  6 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  5 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  4 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  3 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  2 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  1 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  0 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    └───┴───┴───┴───┴───┴───┴───┴───┘
# y/x  0   1   2   3   4   5   6   7"""
        else:
            template = """# {}
# ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,7 │ 1,7 │ 2,7 │ 3,7 │ 4,7 │ 5,7 │ 6,7 │ 7,7 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,6 │ 1,6 │ 2,6 │ 3,6 │ 4,6 │ 5,6 │ 6,6 │ 7,6 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,5 │ 1,5 │ 2,5 │ 3,5 │ 4,5 │ 5,5 │ 6,5 │ 7,5 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,4 │ 1,4 │ 2,4 │ 3,4 │ 4,4 │ 5,4 │ 6,4 │ 7,4 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,3 │ 1,3 │ 2,3 │ 3,3 │ 4,3 │ 5,3 │ 6,3 │ 7,3 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,2 │ 1,2 │ 2,2 │ 3,2 │ 4,2 │ 5,2 │ 6,2 │ 7,2 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,1 │ 1,1 │ 2,1 │ 3,1 │ 4,1 │ 5,1 │ 6,1 │ 7,1 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,0 │ 1,0 │ 2,0 │ 3,0 │ 4,0 │ 5,0 │ 6,0 │ 7,0 │
# └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘"""
    else:
        if compact:
            template = """# {}
#    +---+---+---+---+---+---+---+---+
#  7 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  6 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  5 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  4 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  3 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  2 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  1 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  0 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
# y/x  0   1   2   3   4   5   6   7"""
        else:
            template = """# {}
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,7 | 1,7 | 2,7 | 3,7 | 4,7 | 5,7 | 6,7 | 7,7 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,6 | 1,6 | 2,6 | 3,6 | 4,6 | 5,6 | 6,6 | 7,6 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,5 | 1,5 | 2,5 | 3,5 | 4,5 | 5,5 | 6,5 | 7,5 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,4 | 1,4 | 2,4 | 3,4 | 4,4 | 5,4 | 6,4 | 7,4 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,3 | 1,3 | 2,3 | 3,3 | 4,3 | 5,3 | 6,3 | 7,3 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,2 | 1,2 | 2,2 | 3,2 | 4,2 | 5,2 | 6,2 | 7,2 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,1 | 1,1 | 2,1 | 3,1 | 4,1 | 5,1 | 6,1 | 7,1 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,0 | 1,0 | 2,0 | 3,0 | 4,0 | 5,0 | 6,0 | 7,0 |
# +-----+-----+-----+-----+-----+-----+-----+-----+"""
    # board the board string
    coords = [(x,BOARD_SIDE_LENGTH-1-y) for y in range(BOARD_SIDE_LENGTH) for x in range(BOARD_SIDE_LENGTH)]
    cells = []
    whites = []
    blacks = []
    for white in board_dict["white"]:
        whites.append((white[1], white[2]))
    for black in board_dict["black"]:
        blacks.append((black[1], black[2]))
    w = b = 0
    for xy in coords:
        if xy not in whites and xy not in blacks:
            cells.append("   ")
        elif xy in whites:
            cells.append("{}w ".format(board_dict["white"][w][0])) #str(board_dict[xy])[:3].center(3))
            w +=  1
        elif xy in blacks:
            cells.append("{}b ".format(board_dict["black"][b][0])) #str(board_dict[xy])[:3].center(3))
            b +=1
    # print it
    print(template.format(message, *cells), **kwargs)


# ---------------------------------------------------------------------------- #
#                                                                              #
#                           General Utility Functions                          #
#                                                                              #
# ---------------------------------------------------------------------------- #
def list_neighbor_locations(board, loc):
    """
    List the coordinates surrounding a given location of a 2x2 grid
    """
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_loc = (loc[0]+i, loc[1]+j)
            if board.is_valid(new_loc) and new_loc != loc:
                neighbors.append(new_loc)
    return neighbors


def are_neighbors(loc1, loc2):
    """
    Check if the two locations are within space of eachother
    """
    # Same locaiton is are not neighbors
    if loc1 == loc2: return False

    return abs(loc1[0]-loc2[0]) <= 1 and abs(loc1[1]-loc2[1]) <= 1


def calculate_manhattan_distance(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + \
           abs(loc1[1] - loc2[1])


# ---------------------------------------------------------------------------- #
#                                                                              #
#                           Game Specific Utility Functions                    #
#                                                                              #
# ---------------------------------------------------------------------------- #
def get_piece_location(piece):
    """
    Given a piece tuple (n, x, y) return just the location (x, y)
    """
    return (piece[1], piece[2])


def calculate_heuristic_value(board, loc):
    """
    Our heuristic function.
    """
    return count_eliminated_blacks(board, loc, [])


def count_eliminated_blacks(board, loc, already_exploded):
    """
    Counts the net gain/loss of an explosion at a given location.
        - +1 for every black tile exploded
    """
    total = 0

    for black in board.get_blacks():
        black_loc = (black[1], black[2])
        if are_neighbors(black_loc, loc):
            if black_loc not in already_exploded:
                already_exploded.append(black_loc)
                total += black[0] + count_eliminated_blacks(board, black_loc, already_exploded)

    return total


def list_unique_black_neighbors(board):
    """
    List all the unique neighbors of every black piece on the board
    """
    all_neighbors = set([])
    for black in board.get_blacks():
        black_loc = (black[1], black[2])
        neighbors = list_neighbor_locations(board, black_loc)
        for neighbor in neighbors:
            if not board.is_occupied_by_black(neighbor):
                all_neighbors.add(neighbor)

    return all_neighbors


def list_target_locations(board):
    """
    Return a sorted list of the target locations with the
    """
    scored_targets = []
    unique_neighbors = list_unique_black_neighbors(board)
    for loc in unique_neighbors:
        scored_targets.append((calculate_heuristic_value(board, loc), loc))

    scored_targets.sort(reverse=True)
    return scored_targets


def valid_move(board, loc, visited):
    """
    Check if the new location is valid.
    Must:
        - be on the board
        - not have been visited in the current path (visited)
    """
    return board.is_valid(loc) and loc not in visited # and not board.is_occupied_by_white(loc)


def list_pieces_by_distance(pieces, target):
    """
    lists the white pieces in order by closest to furthest to the target
    """
    lst = []
    for piece in pieces:
        loc = (piece[1], piece[2])
        lst.append((calculate_manhattan_distance(loc, target), piece))

    lst.sort()
    return lst

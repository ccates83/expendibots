from search.DescendingPriorityQueue import *

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
    coords = [(x,7-y) for y in range(8) for x in range(8)]
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


#
# Added utility functions
#
def did_lose(board_state):
    """
    Check the board state. If there are blacks and no white pieces left we lose.
    """
    return board_state["black"] and not board_state["white"]

def did_win(board_state):
    """
    Check board state. If there are no blacks left we win.
    """
    return not board_state["black"]


def are_neighbors(location1, location2):
    """
    Check if the two locations neighbor eachother
    """
    if location1 == location2: return False
    return  abs(location1[0]-location2[0]) <= 1 and \
            abs(location1[1]-location2[1]) <= 1


def is_occupied_by_black(location, board_data):
    for black in board_data["black"]:
        if location == (black[1], black[2]):
            return True
    return False


def is_occupied_by_white(location, board_data):
    for white in board_data["white"]:
        if location == (white[1], white[2]):
            return True
    return False


def is_occupied(location, board_data):
    return  is_occupied_by_black(location, board_data) or \
            is_occupied_by_white(location, board_data)


def list_neighboring_pieces(board_state, location):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            loc = (location[0]+i, location[1]+j)
            if (is_occupied(loc, board_state)):
                neighbors.append(loc)
    return neighbors


def remove_piece(board_state, location):
    """
    Removes a piece from the given location on the board state
    """
    # Check the black locations
    for black in board_state["black"]:
        if (location == (black[1], black[2])):
            board_state["black"].remove(black)
    # Check the whites
    for white in board_state["white"]:
        if (location == (white[1], white[2])):
            board_state["white"].remove(white)

def place_piece(board_state, stack_size, location):
    """
    Places a white piece with stack size given
    """
    board_state["white"].append((stack_size, location[0], location[1]))


def explode(board_state, location, actions):
    """
    Explodes the node and recursively calls explode on any neighbors.
    Returns the new board state after the explosion.
    """
    # If we call explode on an empty tile, we are done
    if (not is_occupied(location, board_state)):
        return board_state

    # Append the explosion to the actions
    actions.append(("explode", location))


    remove_piece(board_state, location)
    for neighbor in list_neighboring_pieces(board_state, location):
        explode(board_state, neighbor, actions)
    return board_state


def list_black_neighbor_tiles(board_data):
    """
    Lists all neighboringn locations to black tiles. These are the locations we
    want our white pieces to potentially be.
    """
    neighbors = []
    for black in board_data["black"]:
        for i in range(-1, 2):
            for j in range(-1, 2):
                loc = (black[1] + i, black[2] + j)
                if( not is_occupied_by_black(loc, board_data)):
                    neighbors.append(loc)
    return neighbors


# The next two functions take two tuple coordinates and finds the distances
#
def horizontal_distance(start, end):
    return abs(start[0] - end[0])
def vertical_distance(start, end):
    return abs(start[1] - start[1])

def calculate_number_moves(start_loc, target_loc, step=1):
    """
    Calculates the number of moves it would take the node to reach the distination
    coordinates. Works with stacks.
    Should not have to worry about pieces in the way.
    """
    # distance / number of spaces the stack can move
    return  horizontal_distance(start_loc, target_loc) / step + \
            vertical_distance(start_loc, target_loc) / step

def is_occupied_by_black(location, board_data):
    for black in board_data["black"]:
        if location == (black[1], black[2]):
            return True
    return False


def is_occupied_by_white(location, board_data):
    for white in board_data["white"]:
        if location == (white[1], white[2]):
            return True
    return False


def is_occupied(location, board_data):
    return  is_occupied_by_black(location, board_data) or \
            is_occupied_by_white(location, board_data)


def list_neighboring_empty_tiles(node, board_data):
    """
    Lists the locations surrounding the node.
    """
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i != 0 or j != 0) and \
                not is_occupied_by_black((node[1] + i, node[2]  + j), board_data):
                neighbors.append((node[1] + i, node[2]  + j))
    return neighbors


def count_occurances(list):
    elements = {}

    for elem in list:
        if elem in elements:
            elements[elem] += 1
        else:
            elements[elem] = 1
    return elements


def count_eliminated_tiles(explosion_location, board_data, already_exploded = []):
    """
    Calculates the number of tiles that would blow up from a given location
    ADDS: black tiles eliminated
    SUBTRACTS: white tiles eliminated
    """
    net_total = -1
    for black in board_data["black"]:
        if are_neighbors((black[1], black[2]), (explosion_location[0], explosion_location[1])):
            if black not in already_exploded:
                already_exploded.append(black)
                net_total += 1 + count_eliminated_tiles((black[1], black[2]), board_data, already_exploded)
    for white in board_data["white"]:
        if are_neighbors((white[1], white[2]), (explosion_location[0], explosion_location[1])):
            if white not in already_exploded:
                already_exploded.append(white)
                net_total -= 1 + count_eliminated_tiles((black[1], black[2]), board_data, already_exploded)

    return net_total

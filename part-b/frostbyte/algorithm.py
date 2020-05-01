# Algorithm.py
#
# Functions for implementing our game playing algorithm

def calculate_next_move(colour, board):
    """
    Calculate the next best move for the given player (colour) with the given
    state of the board
    """
    list_all_possible_actions(colour, board)


def list_all_possible_actions(colour, board):
    """
    list all possible moves available for a player
    """
    all_actions = []
    for stack in board.state[colour]:
        all_actions += list_possible_actions(colour, board, stack)

    for action in all_actions:
        print(action)


def list_possible_actions(colour, board, stack):
    """
    List all possible actions for a given stack on the board
    """
    loc = stack[1]
    n = stack[0]
    actions = []

    # find all the possible move actions
    for step in range(1, n+1):
        for num_moving in range(1, n+1):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 or j == 0:
                        new_loc = (loc[0]+i*step, loc[1]+j*step)
                        if (i, j) == (0, 0):
                            actions.append(("BOOM", loc))
                        elif in_bounds(new_loc):
                            if (colour == "white" and not board.is_occupied_by_black(new_loc)) or \
                                colour == "black" and not board.is_occupied_by_white(new_loc):
                                actions.append((("MOVE"), num_moving, loc, new_loc))

    return actions


#
#   Helpers
#
def in_bounds(loc):
    """
    Check if the given location is within the boards of an expendibots board
    """
    return loc[0] > -1 and loc[0] < 8 and loc[1] > -1 and loc[1] < 8

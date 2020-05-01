from copy import deepcopy
# Algorithm.py
#
# Functions for implementing our game playing algorithm

def calculate_next_move(colour, board):
    """
    Calculate the next best move for the given player (colour) with the given
    state of the board
    """
    print("Calculating next move...")
    actions = list_all_possible_actions(colour, board)
    for action in actions:
        print(action)

    print("---")
    filtered_actions = []

    for action in actions:
        print("Current action: ", action)

        # If the action is a boom, try out the boom.
        #     - If we win, do it
        #     - if it improves the ratio ours/their pieces, do it
        #     - else, remove it from the list of actions
        if action[0] == "BOOM":
            test_state = test_boom(board, action[1])

            # If we win with this explosion, immediately return it
            if did_win(colour, test_state):
                print("We win!")
                return action

            # If the boom gives us a better ratio of our pieces to theirs than we have right now, do it
            if get_ratio(colour, board) < get_ratio(colour, test_state):
                print("Ratio {} -> {}".format(get_ratio(colour, board), get_ratio(colour, test_state)))
                filtered_actions.append(action)

        else:
            filtered_actions.append(action)

    # We have gone through the explosions and decided if they are worth it, now investigate moves
    print("Filtered list:")
    for action in filtered_actions:
        print(action)



def list_all_possible_actions(colour, board):
    """
    list all possible moves available for a player
    """
    all_actions = []
    for stack in board.state[colour]:
        all_actions += list_possible_actions(colour, board, stack)

    # Puts 'BOOM's to the front of the list
    all_actions.sort()
    return all_actions


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


def test_boom(board, loc):
    new_board = deepcopy(board)
    new_board.perform_boom(loc)
    return new_board


#
#   Helpers
#
def in_bounds(loc):
    """
    Check if the given location is within the boards of an expendibots board
    """
    return loc[0] > -1 and loc[0] < 8 and loc[1] > -1 and loc[1] < 8


def did_win(colour, board):
    if colour == "white":
        opp = "black"
    else:
        opp = "white"

    return board.state[colour] and not board.state[opp]


def get_ratio(colour, board):
    """
    Assuming the passed colour is the current players color, calculate the get_ratio
    of player/opponent pieces left
    """
    players_count = 0
    for stack in board.state[colour]:
        players_count += stack[0]

    if colour == "white":
        opp = "black"
    else:
        opp = "white"

    opponent_count = 0
    for stack in board.state[opp]:
        opponent_count += stack[0]

    return players_count / opponent_count

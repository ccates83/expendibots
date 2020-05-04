from copy import deepcopy

"""

Utility class for helper functions for Expendibots part b

"""
def get_opp_colour(colour):
    """
    Returns a string of your opponents colour
    """
    if colour == "white":
        return "black"

    return "white"


def list_all_possible_moves(colour, board):
    """
    Lists every possible move a player can take. Excludes explosions that cause the
    player to immediately lose
    """
    actions = []
    for stack in board.state[colour]:

        # Explode, if we dont lose add it to the list
        # if we win, make that the only item in the list
        temp_board = deepcopy(board)
        temp_board.explode(stack[1])
        if temp_board.state[colour]:
            actions.append(('BOOM', stack[1]))
            if not temp_board.state[get_opp_colour(colour)]:
                return [('BOOM', stack[1])]

        for step in range(1, stack[0]+1):
            for n in range(1, stack[0]+1):
                # Up, down, left, right
                action = ('MOVE', n, stack[1], (stack[1][0], stack[1][1]+step))
                if board.is_valid_action(colour, action):
                    actions.append(action)

                action = ('MOVE', n, stack[1], (stack[1][0], stack[1][1]-step))
                if board.is_valid_action(colour, action):
                    actions.append(action)

                action = ('MOVE', n, stack[1], (stack[1][0]+step, stack[1][1]))
                if board.is_valid_action(colour, action):
                    actions.append(action)

                action = ('MOVE', n, stack[1], (stack[1][0]-step, stack[1][1]))
                if board.is_valid_action(colour, action):
                    actions.append(action)

    for action in actions:
        if not board.is_valid_action(colour, action):
            actions.remove(action)

    return actions

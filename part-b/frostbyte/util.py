from copy import deepcopy

"""

Utility class for helper functions for Expendibots part b

"""
# These books were calculated by running a random choice bot algorithm 10000 times
# adding or subtracting n from the location (n being the turn number). Adding if they won,
# subtracting if they lost
# This was done iteratively, the first iteration with random, then the new values used against random
# to create more informed values each iteration.
WHITE_VALUES = [
    [244,   290,    164,    92,     29,     61,     0,      0   ],
    [277,   258,    582,    257,    79,     114,    101,    106 ],
    [4012,  3951,   2761,   1793,   1072,   607,    581,    322 ],
    [8539,  9066,   6609,   4389,   2922,   1504,   1044,   827,],
    [12750, 14922,  11889,  7483,   5472,   3001,   1880,   1298],
    [17714, 20364,  17059,  14111,  11621,  5781,   2755,   2593],
    [20802, 24905,  24096,  21534,  17396,  11114,  5262,   3465],
    [15849, 21504,  21337,  19418,  15513,  10880,  6004,   3492]
]
BLACK_VALUES = reversed(WHITE_VALUES) # Use the white values, but the rows have to be reversed to account for the other side of the board


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


def point_actions(colour, actions):
    """
    Assign a point value to moves based on the book we created
    """
    pointed = []
    for action in actions:
        if action[0] == 'BOOM':
            pointed.append((0, action))
        else:
            grid = WHITE_VALUES
            if colour == "black":
                grid = BLACK_VALUES

            # print("Action:", action)
            # y = action[3][1]
            # x = action[3][0]
            # print(x, y)
            # row = grid[y]
            # print(row)
            # val = row[7]
            # print(val)
            # print("Value:", grid[action[3][1]][action[3][0]])
            pointed.append((grid[action[3][1]][action[3][0]], action))

    return pointed


def get_booms(list_of_actions):
    """
    return a list of the booms we would want to do. Priority in the algorithm is
    given to booms that would cause a win or ones that provide the best ratio
    """
    booms = []

    for action in list_of_actions:
        if action[0] == 'BOOM':
            booms.append(action)

    return booms


def test_boom(board, colour, action):
    """
    Give a new board state that would be the result of the action
    """
    temp = deepcopy(board)
    temp.perform_action(colour,action)
    return temp


def get_ratio(colour, board):
    """
    Return the ratio of colour pieces to opponent pieces
    """
    return len(board.state[colour]) / len(board.state[get_opp_colour(colour)])


def did_win(colour, board):
    """
    Check if the given colour won the game
    """
    return board.state[colour] and not board.state[get_opp_colour(colour)]

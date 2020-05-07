from copy import deepcopy

"""

Utility class for helper functions for Expendibots part b

"""
# These books were calculated by running a random choice bot algorithm 10000 times
# adding or subtracting n from the location (n being the turn number). Adding if they won,
# subtracting if they lost
# This was done iteratively, the first iteration with random, then the new values used against random
# to create more informed values each iteration.


EXPONENTIAL_WEIGHTS = [
    [0,         0,          16384,      8192,       7168,       81920,      2097152,    155648   ],
    [1040,      0,          1024,       0,          0,          4096,       159744,     1572864  ],
    [1049344,   256,        757968,     8508224,    4196608,    17458240,   276773840,  145003088],
    [192,       10487936,   7028848,    6326648,    5014472,    8471216,    14229900,   290867968],
    [20972164,  2812,       4665200,    2503448,    37471064,   10498652,   39297164,   44084612 ],
    [6704,      42733890,   1338384,    69622546,   312117424,  56156116,   84912710,   6143110  ],
    [11524,     3098,       40376,      681089932,  11344370,   134768662,  6982534,    37670632 ],
    [3286,      9464,       179602,     27312510,   223325632,  16262538,   3838178,    4368054  ]
]

LINEAR_WEIGHTS = [
    [244,   290,    164,    92,     29,     61,     0,      0   ],
    [277,   258,    582,    257,    79,     114,    101,    106 ],
    [4012,  3951,   2761,   1793,   1072,   607,    581,    322 ],
    [8539,  9066,   6609,   4389,   2922,   1504,   1044,   827,],
    [12750, 14922,  11889,  7483,   5472,   3001,   1880,   1298],
    [17714, 20364,  17059,  14111,  11621,  5781,   2755,   2593],
    [20802, 24905,  24096,  21534,  17396,  11114,  5262,   3465],
    [15849, 21504,  21337,  19418,  15513,  10880,  6004,   3492]
]

WHITE_VALUES = LINEAR_WEIGHTS
BLACK_VALUES = LINEAR_WEIGHTS[::-1] # the rows have to be reversed to account for the other side of the board


def calculate_next_action(colour, board):
    """
    Given a player (colour) and the state of the board, returns the next best move for the player
    """
    actions = list_all_possible_moves(colour, board)

    # Evaluate boom actions. If we win immediately do it, if it betters our ratio
    # of our pieces to opponents pieces, do the one that gives the best new ratio
    current_ratio = get_ratio(colour, board)
    best = current_ratio
    boom_to_execute = None
    for boom in get_booms(actions):
        test = test_boom(board, colour, boom)
        if did_win(colour, test):
            return boom

        new_ratio = get_ratio(colour, test)
        if new_ratio > best:
            best = new_ratio
            boom_to_execute = boom

    if boom_to_execute:
        return boom_to_execute
    # If none of the boom actions are in our favor, take the best move
    pointed = point_actions(colour, actions)

    pointed.sort(reverse=True)
    return pointed[0]


def create_action_queue(colour, board):
    """
    Return a list of actions in order of priority for a given board state and player,
    each action is preceded in a tuple by the value we give it
    """
    actions = list_all_possible_moves(colour, board)

    # Evaluate boom actions. If we win immediately do it, if it betters our ratio
    # of our pieces to opponents pieces, do the one that gives the best new ratio
    current_ratio = get_ratio(colour, board)
    best = current_ratio
    boom_to_execute = None
    for boom in get_booms(actions):
        test = test_boom(board, colour, boom)
        if did_win(colour, test):
            return [boom]

        new_ratio = get_ratio(colour, test)
        if new_ratio > best:
            best = new_ratio
            boom_to_execute = boom

    if boom_to_execute:
        return [boom_to_execute]

    # If none of the boom actions are in our favor, take the best move
    pointed = point_actions(colour, actions)
    pointed.sort(reverse=True)

    return pointed


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


def test_action(board, colour, action):
    """
    Return a new board state that represents the result of this action
    """
    temp = deepcopy(board)
    temp.perform_action(colour,action)
    return temp


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

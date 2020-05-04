from copy import deepcopy

"""

Utility class for helper functions for Expendibots part b

"""
# These books were calculated by running a random choice bot algorithm 1000 times
# and adding +1 for any moves in a game that resulted in a win, -1 for any moves
# in a game resulting in a loss
WHITE_VALUES = [
    [-7, 4, 17, 11, 33, -3, 6, -19],
    [-28, -18, -33, 20, 18, -1, 17, -2],
    [-23, -48, -61, -23, 17, 4, 2, 9],
    [-12, -10, -22, -9, -7, -7, 9, 11],
    [-19, 0, -2, 4, 5, -14, 8, -5],
    [-16, 8, -6, 2, 1, -15, -4, -16],
    [2  -9  -19  -12  -17  -14  -38  -24],
    [-18, -23, -10, -28, 8, -14, -28, -55]
]
BLACK_VALUES = [
    [-5, -9, 21, -12, 28, 9, -15, -30],
    [11, 37, 7, 14, 21, 21, -1, -9],
    [21, 26, 20, 13, 32, 11, 7, -5],
    [11, 10, 8, 3, -6, -22, 1, -28],
    [9, -1, -1, 2, -8, -16, 13, 0],
    [17, 1, 9, -7, -20, 3, 15, 10],
    [25, -7, 11, 21, 16, 22, 29, 41],
    [6, 6, 33, 11, 12, 14, 29, 20]
]


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

import sys
import json

from search.util import print_move, print_boom, print_board
from search.node import Node

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    print("#", data)
    print()

    solve(data)


def solve(board_data):
    """
    Overarching function that outputs the moves needed to win the game.
    """
    if (len(board_data["black"]) == 0):
        print("# SOLVED")
        return

    path = get_closest_nodes(board_data)
    execute_path(path[0], path[1], board_data)

    solve(board_data)

def horizontal_distance(node1, node2):
    return abs(node1[1] - node2[1])


def vertical_distance(node1, node2):
    return abs(node1[2] - node2[2])

# Update this to check number of moves to being a NEIGHBOR not ontop
def calculate_number_moves(node, target_node):
    """
    Calculates the number of moves it would take the node to reach the distination
    coordinates. Works with stacks.
    Should not have to worry about pieces in the way.
    """
    # distance / number of spaces the stack can move
    return  horizontal_distance(node, target_node) / node[0] + \
            vertical_distance(node, target_node) / node[0]


def get_closest_nodes(board_data):
    """
    Looks through the white pieces and finds closest nodes from a white stack
    to a black stack.
    Returns: Tuple of start and end node for the closest path.
    """
    fewest_moves = -1
    start_node = 0
    end_node = 0

    for white_piece in board_data["white"]:
        for black_piece in board_data["black"]:
            moves = calculate_number_moves(white_piece, black_piece)
            if fewest_moves == -1 or moves < fewest_moves:
                start_node = white_piece
                end_node = black_piece
                fewest_moves = moves

    return (start_node, end_node)


def are_neighbors(node1, node2):
    return  horizontal_distance(node1, node2) == 1 and \
            vertical_distance(node1, node2) == 1


def explode(node, board_data):
    print_boom(node[1], node[2])
    if node in board_data["white"]:
        board_data["white"].remove(node)
    else:
        board_data["black"].remove(node)

    #explode any white piece neighbors
    for white in board_data["white"]:
        if (are_neighbors(node, white)):
            explode(white, board_data)
    for black in board_data["black"]:
        if (are_neighbors(node, black)):
            explode(black, board_data)

    print("#", board_data)


def copy_node(node):
    return [node[0], node[1], node[2]]


def execute_path(start_node, end_node, board_data):
    """
    Prints the moves for the path from the start_node to the end. Uses the stack
    size to move the furthest distance at a time. For now, move just one element
    of the stack. Removes the node blown up from the list.

    Recursively prints the path taken between the two closest nodes.
    """
    horiz_dist = horizontal_distance(start_node, end_node)
    vert_dist = vertical_distance(start_node, end_node)

    if are_neighbors(start_node, end_node):
        explode(start_node, board_data)
        return

    # Moves horizontally first
    if (horiz_dist < vert_dist or vert_dist == 1):
        print("# Move horiz 1")
        #Get the direction
        dir = 1
        if (start_node[1] > end_node[1]):
            dir = -1

        #Get the distance we can move
        if horiz_dist > start_node[0]:
            num_spaces = start_node[0]
        else:
            num_spaces = horiz_dist

        old_location = copy_node(start_node)
        start_node[1] = start_node[1] + dir * num_spaces

        #Print the move and print the rest of the path
        print_move(old_location[0], old_location[1], old_location[2], start_node[1], start_node[2])
        execute_path(start_node, end_node, board_data)


    # Moves vertically
    else:
        print("# Move vert 1")
        #Get the direction
        dir = 1
        if (start_node[2] > end_node[2]):
            dir = -1

        #Get the distance we can move
        if vert_dist > start_node[0]:
            num_spaces = start_node[0]
        else:
            num_spaces = vert_dist

        old_location = copy_node(start_node)
        start_node[2] = start_node[2] + dir * num_spaces

        #Print the move and print the rest of the path
        print_move(1, old_location[1], old_location[2], start_node[1], start_node[2])
        execute_path(start_node, end_node, board_data)


if __name__ == '__main__':
    main()

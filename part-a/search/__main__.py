import sys
import json

from search.util import print_move, print_boom, print_board
from search.node import Node

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    print(data)
    print()

    path = get_closest_nodes(data)
    print_path(path[0], path[1])


def solve():
    """
    Overarching function that outputs the moves needed to win the game.
    """


def calculate_number_moves(node, target_node):
    """
    Calculates the number of moves it would take the node to reach the distination
    coordinates. Works with stacks.

    Should not have to worry about pieces in the way.
    """
    horizontal_distance = abs(node[1] - target_node[1])
    vertical_distance = abs(node[2] - target_node[2])

    # distance / number of spaces the stack can move
    return min(horizontal_distance / node[0], vertical_distance / node[0])


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
                print(fewest_moves)

    return (start_node, end_node)


def print_path(start_node, end_node):
    """
    Prints the moves for the path from the start_node to the end. Uses the stack
    size to move the furthest distance at a time. For now, move just one element
    of the stack.
    """
    


if __name__ == '__main__':
    main()

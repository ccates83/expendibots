from search.DescendingPriorityQueue import *


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
    return  horizontal_distance(node1, node2) <= 1 and \
            vertical_distance(node1, node2) <= 1


def tiles_are_neighbors(coord1, coord2):
    return abs(coord1[0] - coord2[0]) <= 1 and \
            abs(coord1[1] - coord2[1]) <= 1


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

from search.DescendingPriorityQueue import *

def solve(board_data, visited_locations = [], current_path = ""):
    """
    Overarching solve function. Win if white pieces are not empty and black
    pieces are empty in the board data.
    PARAMS:
        - board_data = current state of the board
        - visited_locations = the tuple locations the current path has been to
        - current_path = string to print of all the moves of this current soln
    """

    # If there are not more black pieces in the current game board, this is solved
    if( not board_data["black"] ):
        print("# Solved!")
        print(current_path)
        return True # Solved

    # Copy all the data so recursive calls do not mess with other branches
    board_state = dict(board_data)
    visited = visited_locations.copy()
    curr_path = current_path

    # OUTLINE:
    #  - find the location we want a white piece to move
    #  - try each path, checking for repeated visits to locations
    #  - recursively go through each option and if we run out of white pieces then
    #         we kill that branch

    # Find all neighboring tiles to blacks
    target_locations = list_black_neighbor_tiles(board_state)

    # For every white piece, try every target location and eventually explode
    # this would be a good place to sort the paths from whites to these target_locations
    # based on our heuristic - some combination of number of moves, number of blacks
    # exploded, number of white pieces lost, etc...
    potential_paths = DescendingPriorityQueue()
    for white in board_state["white"]:
        for loc in target_locations:
            potential_paths.put((calculate_total_path_cost(board_data, white, loc), loc))

    while(not potential_paths.empty()):
        next = potential_paths.get()
        print(next)




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


def calculate_total_path_cost(board_data, start_node, target_location):
    """
    Assigns a value to this path - higher the betterself.
    FACTORS:
        + Number of black pieces we would explode in that location
        + 14 - manhattan distance (14 is the furthest it can be, corner to corner of the board)
        - Number of white pieces we would lose exploding there
    """
    start = (start_node[1], start_node[2]) #start_node.coord ## maybe store its current location too
    step = 1 # start_node.stack_size ## I am not positive where you store this yet
    return  14 - calculate_number_moves(start, target_location, step) + \
            count_eliminated_tiles(target_location, board_data)



#
#   Keep from here to ##### for sure
#

# The next two functions take two tuple coordinates and finds the distances
#
def horizontal_distance(start, end):
    return abs(start[0] - end[0])
def vertical_distance(start, end):
    return abs(start[1] - start[1])

def calculate_number_moves(start_loc, target_loc, step):
    """
    Calculates the number of moves it would take the node to reach the distination
    coordinates. Works with stacks.
    Should not have to worry about pieces in the way.
    """
    # distance / number of spaces the stack can move
    return  horizontal_distance(start_loc, target_loc) / step + \
            vertical_distance(start_loc, target_loc) / step

#####


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
    RETURN:
        - eliminated[0] is the white tiles lost
        - eliminated[1] is the black tiles exploded
    """
    total = 0
    for black in board_data["black"]:
        if are_neighbors(black, (1, explosion_location[0], explosion_location[1])):
            if black not in already_exploded:
                already_exploded.append(black)
                total += 1 + count_eliminated_tiles((black[1], black[2]), board_data, already_exploded)
    return total


def find_optimal_locations(board_data):
    """
    Find overlaps between as many neighbors of black as possible. This will blow
    up the most black pieces per turn.
    """
    all_neighbors = []
    for black in board_data["black"]:
        for loc in list_neighboring_empty_tiles(black, board_data):
            if loc not in all_neighbors:
                all_neighbors.append(loc)

    # Creates a list of the locations that will explode themost blackpieces
    optimal_locations = []
    most_explosions = 0
    for loc in all_neighbors:
        num_explosions = count_eliminated_tiles(loc, board_data, [])
        if num_explosions > most_explosions:
            most_explosions = num_explosions
            optimal_locations = []
            optimal_locations.append(loc)
        elif num_explosions == most_explosions:
            optimal_locations.append(loc)

    return optimal_locations


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

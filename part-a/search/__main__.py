import sys
import json

from search.util import *
from search.node import Node
from search.solver import *

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    white = data["white"]
    black = data["black"]
    print("White nodes: ", data["white"])
    print("Black nodes: ", data["black"])


    # TODO: find and print winning action sequence
    print("ORIGINAL STATE:")
    print(data)
    print_board(data)


    print("Solving...")

    i = 0
    for white in data["white"]:
        root_node = Node(state=data, stack_size=white[0], location=(white[1], white[2]),piece_number=0,parent=None,action=None,depth=0,path_cost=0,heuristic_cost=0)
        print(root_node.state)
        if (root_node.search()):
            print("SOLVED")
            break

    # # Find all neighboring tiles to blacks
    # target_locations = list_black_neighbor_tiles(data)
    #
    # # For every white piece, try every target location and eventually explode
    # # this would be a good place to sort the paths from whites to these target_locations
    # # based on our heuristic - some combination of number of moves, number of blacks
    # # exploded, number of white pieces lost, etc...
    # potential_paths = DescendingPriorityQueue()
    # for white in data["white"]:
    #     for loc in target_locations:
    #         potential_paths.put((heuristic_value(data, white, loc), loc))
    #
    # # Printing the queue for testing
    # print("# Target locations: ")
    # while(not potential_paths.empty()):
    #     next = potential_paths.get()
    #     print("# ", next)

if __name__ == '__main__':
    main()

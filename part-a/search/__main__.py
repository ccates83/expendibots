import sys
import json

from search.util import *
from search.node import Node

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    white = data["white"]
    print(white)
    print(data["white"][0])
    black = data["black"]

    # TODO: find and print winning action sequence
    print("ORIGINAL STATE:")
    print(data)
    print_board(data)


    print("Solving...")


    root_node = Node(state=data, piece_number=0, parent=None,action=None,depth=0,path_cost=0,heuristic_cost=0)
    print(root_node.state)
    root_node.search()

if __name__ == '__main__':
    main()

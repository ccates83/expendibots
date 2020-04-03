import sys
import json

#from search.util import *
from search.node import Node
from search.solver import *

from search.MyNode import MyNode
from search.board  import Board
from search.my_util import *

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    white = data["white"]
    black = data["black"]
    print("# White nodes: ", data["white"])
    print("# Black nodes: ", data["black"])


    # TODO: find and print winning action sequence
    print("# ORIGINAL STATE:")
    print_board(data)


    print("#\n#\n# Solving...\n#")

    i = 0
    for white in data["white"]:
        # root_node = Node(state=data, stack_size=white[0], location=(white[1], white[2]),piece_number=0,parent=None,action=None,depth=0,path_cost=0,heuristic_cost=0)
        root_node = MyNode(board=Board(data), location=(white[1], white[2]), stack_size=white[0])
        if (root_node.h_search()):
            print("#\n# ----- SOLVED ----- #")
            break


if __name__ == '__main__':
    main()

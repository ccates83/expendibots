import sys
import json

from search2.Board import *
from search2.Solver import *

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    board = ExpBoard(data, BOARD_SIDE_LENGTH)

    # TODO: find and print winning action sequence
    print("# ORIGINAL STATE:")
    board.print()

    print("#\n#\n#")
    print("#\n#\n#")
    print("#\n#\n#")
    print("#\n#\n#")


    #
    solver = Solver(board)
    solver.print()
    solver.solve()

    # print("\n\n")
    # solver.print()


    #
    #   TESTING BOARD CLASS
    #
    # print("Board Testing")
    # board.print()
    # print("Stack the pieces")
    # board.move_pieces((4, 3), (3, 5), 1)
    # board.print()
    # print("Move both one to the right")
    # board.move_pieces((3, 5), (4, 5), 2)
    # board.print()
    # print("Unstack, move one 2 spaces left")
    # board.move_pieces((4, 5), (2, 5), 1)
    # board.print()

    #
    #   TESTING NODE CLASS
    #
    # node = Node(board=board, location=(board.get_whites()[0][1], board.get_whites()[0][2]), \
    #             stack_size= board.get_whites()[0][0], target_location=(0, 0))
    # print(node)
    # print(node.board.data)
    # print("Node's board:")
    # node.board.print()
    # node.move_to((1, 0), node.stack_size)
    # node.print_board()

    # print("Copying to a new node")
    # node2 = node.copy()
    # print(node2)
    # node2.board.print()
    # print()
    # print("Editing the new node")
    # node2.move_to((7,2), 1)
    # print("original:", node)
    # node.board.print()
    # print("new node:", node2)
    # node2.board.print()
    # print("\n Test Exploding")
    # node2.explode()
    # print(node2)
    # node2.board.print()



if __name__ == '__main__':
    main()

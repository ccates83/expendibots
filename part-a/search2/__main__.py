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

    solver = Solver(board)
    print(solver.solve())
    # solver.print_actions()


if __name__ == '__main__':
    main()

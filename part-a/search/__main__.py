import sys
import json

from search.board import *
from search.solver import *

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    board = ExpBoard(data, BOARD_SIDE_LENGTH)

    solver = Solver(board)
    solver.print()
    solver.solve()


if __name__ == '__main__':
    main()

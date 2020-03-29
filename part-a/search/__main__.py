import sys
import json

from search.util import print_move, print_boom, print_board

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    print_board(data, 'I am the board message!')

if __name__ == '__main__':
    main()

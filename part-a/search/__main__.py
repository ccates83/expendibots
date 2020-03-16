import sys
import json

# Originally had search.util but that was not valid as the util file
# is in the same directory. With just 'from util...' the program
# will run.

#from search.util import print_move, print_boom, print_board
from util import print_move, print_boom, print_board


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    print(data)
    print_board(data)

if __name__ == '__main__':
    main()

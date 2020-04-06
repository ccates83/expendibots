from search2.util import *
import sys

class ExpBoard():
    """
    Object to represent the board and key functionality from the board data
    """
    def __init__(self, data, size):
        self.data = data
        self.whites = data["white"]
        self.blacks = data["black"]
        self.board_size = size


    def print(self):
        print_board(self.data)


    def get_state(self):
        return self.data


    def get_whites(self):
        return self.whites


    def get_blacks(self):
        return self.blacks


    def is_valid(self, loc):
        return loc[0] < self.board_size and loc[0] > -1 and \
               loc[1] < self.board_size and loc[1] > -1



    def is_occupied_by_black(self, loc):
        for black in self.blacks:
            if loc == (black[1], black[2]):
                return True
        return False


    def is_occupied_by_white(self, loc):
        for white in self.whites:
            if loc == (white[1], white[2]):
                return True
        return False


    def is_occupied(self, loc):
        return self.is_occupied_by_black(loc) or self.is_occupied_by_white(loc)


    def place_pieces(self, loc, num_pieces):
        """
        Places the number of pieces specified to the location on the board
        Return:
            - Number of pieces in the location
        """
        # First check if we need to stack
        for white in self.whites:
            if loc == (white[1], white[2]):
                white[0] += num_pieces
                print(white[0])
                return white[0]

        # if no stack, add the piece to the board
        self.whites.append((num_pieces, loc[0], loc[1]))
        return num_pieces


    def remove_pieces(self, loc, num_pieces):
        """
        Removes the number of pieces from the given location
        """
        for white in self.whites:
            if loc == (white[1], white[2]):
                # If we dont need to unstack, just remove that piece from the board
                if num_pieces == white[0]:
                    self.whites.remove(white)
                # else we do unstack, update the current locations stack size
                else:
                    new_white = (white[0]-num_pieces, white[1], white[2])
                    self.whites.remove(white)
                    self.whites.append(new_white)
                    # sys.exit(1)


    def remove_all_pieces(self, loc):
        """
        Removes all pieces from a given location
        """
        for white in self.whites:
            if loc == (white[1], white[2]):
                self.whites.remove(white)
        for black in self.blacks:
            if loc == (black[1], black[2]):
                self.blacks.remove(black)


    def move_pieces(self, old_loc, new_loc, num_pieces):
        """
        Move the number of pieces specified from the old location to the new location
        updating the board data accordingly

        Return:
            - Number of pieces in the new location
        """
        # find the piece we are moving
        for white in self.whites:
            if old_loc == (white[1], white[2]):
                n = white[0]
                self.remove_pieces(old_loc, num_pieces)
                if n != num_pieces:
                    self.place_pieces(old_loc, n-num_pieces)
                new_stack_size = self.place_pieces(new_loc, num_pieces)
                print(new_stack_size)
                return new_stack_size


    def update_board(self, new_data):
        """
        Updates the boards data from a new dictionary
        """
        self.data = new_data

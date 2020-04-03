from copy import deepcopy
from search.util import *

class Board():
    """
    Class to represent the board data and perform actions on the board
    """
    def __init__(self, data):
        """
        Init: takes in a dictionary of players pieces
        """
        self.dict = data


    def print(self):
        print_board(self.dict)


    def place_piece(self, n, loc):
        """
        Places n pieces at the given location
        """
        self.dict["white"].append((n, loc[0], loc[1]))


    def remove_piece(self, loc):
        """
        Removes a piece from the given location
        """
        # Check the black locations
        for black in self.dict["black"]:
            if (loc == (black[1], black[2])):
                self.dict["black"].remove(black)
        # Check the whites
        for white in self.dict["white"]:
            if (loc == (white[1], white[2])):
                self.dict["white"].remove(white)


    def get_stack_size(self, location):
        """
        Gives the stack size at a given location
        """
        for white in self.dict["white"]:
            if location == (white[1], white[2]):
                return white[0]
        for black in self.dict["black"]:
            if location == (black[1], black[2]):
                return black[0]
        return 0


    def are_neighbors(self, location1, location2):
        """
        Check if the two locations neighbor eachother
        """
        if location1 == location2: return False
        return  abs(location1[0]-location2[0]) <= 1 and \
                abs(location1[1]-location2[1]) <= 1


    def is_occupied_by_black(self, location):
        for black in self.dict["black"]:
            if location == (black[1], black[2]):
                return True
        return False


    def is_occupied_by_white(self, location):
        for white in self.dict["white"]:
            if location == (white[1], white[2]):
                return True
        return False


    def is_occupied(self, location):
        return  self.is_occupied_by_black(location) or \
                self.is_occupied_by_white(location)


    def get_whites(self):
        return self.dict["white"]


    def get_blacks(self):
        return self.dict["black"]

    def copy(self):
        return Board(deepcopy(self.dict))


    def list_neighboring_pieces(self, location):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                loc = (location[0]+i, location[1]+j)
                if (self.is_occupied(loc)):
                    neighbors.append(loc)
        return neighbors

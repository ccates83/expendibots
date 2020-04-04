from search2.util import *

class Action():
    """
    Object to represent an action done by a piece on the board
    """
    def __init__(self, type, loc1, loc2=None, num_pieces=None):
        self.type = type # string to tell either move or boom
        self.loc1 = loc1 # start location of the move or location of the boom
        self.loc2 = loc2 # OPTIONAL - end location of the move
        self.num_pieces = num_pieces # OPTIONAL - number of pieces to move


    def print(self):
        if self.type == "move":
            print_move(self.num_pieces, self.loc1[0], self.loc1[1], self.loc2[0], self.loc2[1])
        else:
            print_boom(self.loc1[0], self.loc1[1])

from search2.util import *
from search2.Action import *
from search2.Node import *

class Solver():
    """
    Class object to perform all actions of finding the winning solution to the
    game.
    """
    def __init__(self, board):
        """
        Init
        """
        self.board = board
        self.actions = []


    def solve(self):
        """
        Finds the solution and stores every move of the successful path in self.actions
        to be printed later
        """
        # Step 1: Find the target locations in order of priority
        print("# Step 1: find target locs")
        target_locations = list_target_locations(self.board)
        print("# Targets:", target_locations)
        print("#\n#\n#")

        # Step 2: Try to move each white to each target and see if we win
        for white in self.board.get_whites():
            print("# Trying white piece:", white)


    def print_actions(self):
        """
        Prints the actions taken by the solver to the solution of the board
        """
        print("#\n# Solution #")
        for action in self.actions:
            action.print()

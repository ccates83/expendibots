from search2.Constants import *
from search2.Action import *

class Node():
    """
    Class to represent a user piece and attempt to win the game.
    """
    def __init__(self, board, location, stack_size, target_location, actions=[], depth=0):
        """
        Init function
        """
        self.board = board
        self.location = location
        self.stack_size = stack_size
        self.target_location = target_location
        self.heuristic = None
        self.update_heuristic()
        self.actions = actions

        self.depth_limit = 100000 #BOARD_SIDE_LENGTH * BOARD_SIDE_LENGTH / 2
        self.depth = depth

    def __str__(self):
        """
        toString for debugging
        """
        return "Node at {} with stack {} with h(n) = {}".format(self.location, self.stack_size, self.heuristic)


    def manhattan_distance(self):
        """
        Calculate the manhattan distance from node's current location to the
        target location
        """
        return calculate_manhattan_distance(self.location, self.target_location)


    def move_to(self, new_loc, num_pieces):
        """
        Moves the self to the new location
        """
        self.stack_size = self.board.move_pieces(self.location, new_loc, num_pieces)
        self.actions.append(Action("move", self.location, new_loc, num_pieces))
        self.location = new_loc
        self.update_heuristic()


    def update_heuristic(self):
        """
        Calculates the heuristic value based off the location
        """
        self.heuristic = self.manhattan_distance()


    def explode(self):
        """
        Explode the node and update the board accordingly
        """
        self.explode_helper(self.location)


    def explode_helper(self, location):
        """
        Explode the node and update the board accordingly
        """
        # If we call explode on an empty tile, we are done
        if (not self.board.is_occupied(location)):
            return


        print_boom(location[0], location[1])

        # Append the explosion to the actions
        self.actions.append(Action("explode", location))

        self.board.remove_all_pieces(location)
        for neighbor in list_neighbor_locations(self.board, location):
            self.explode_helper(neighbor)

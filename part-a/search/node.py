from search.Constants import *
from search.util import *

class Node():
    """
    Class to represent a user piece and attempt to win the game.
    """
    def __init__(self, board, location, stack_size, target_location, depth=0, path=[]):
        """
        Init function
        """
        self.board = board
        self.location = location
        self.stack_size = stack_size
        self.target_location = target_location
        self.heuristic = None
        self.update_heuristic() # Set the heuristic value

        self.path = path

        self.depth_limit = 100000 #BOARD_SIDE_LENGTH * BOARD_SIDE_LENGTH / 2
        self.depth = depth


    def __str__(self):
        """
        toString for debugging
        """
        return "Node at {} with stack {} with h(n) = {}".format(self.location, self.stack_size, self.heuristic)


    def copy(self):
        """
        Copies self to a new node object
        """
        return Node(deepcopy(self.board), self.location, self.stack_size, self.target_location, path=deepcopy(self.path))


    def manhattan_distance(self):
        """
        Calculate the manhattan distance from node's current location to the
        target location
        """
        return calculate_manhattan_distance(self.location, self.target_location)


    def at_depth_limit(self):
        """
        Check if the node has reached the depth limit of the search
        """
        return self.depth > self.depth_limit


    def at_target(self):
        """
        Check if the node is at its target location
        """
        return self.location == self.target_location


    def move_to(self, new_loc, num_pieces):
        """
        Moves the self to the new location
        """
        self.board.move_pieces(self.location, new_loc, num_pieces)
        self.path.append((num_pieces, self.location, new_loc))
        self.location = new_loc
        self.update_stack_size()
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
        self.stack_size = 0


    def explode_helper(self, location):
        """
        Explode the node and update the board accordingly
        """
        # If we call explode on an empty tile, we are done
        if (not self.board.is_occupied(location)):
            return

        self.board.remove_all_pieces(location)
        for neighbor in list_neighbor_locations(self.board, location):
            self.explode_helper(neighbor)


    def print_board(self):
        """
        Print the nodes board
        """
        self.board.print()


    def update_stack_size(self):
        """
        Sets the nodes stack size to what is stored in the boards data at the noeds location
        """
        for white in self.board.get_whites():
            if (white[1], white[2]) == self.location:
                self.stack_size = white[0]

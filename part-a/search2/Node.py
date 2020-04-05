class Node():
    """
    Class to represent a user piece and attempt to win the game.
    """
    def __init__(self, board, location, stack_size, target_location):
        """
        Init function
        """
        self.board = board
        self.location = location
        self.stack_size = stack_size
        self.target_location = target_location
        self.heuristic = None
        self.update_heuristic()

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
        return abs(self.location[0] - self.target_location[0]) + \
               abs(self.location[1] - self.target_location[1])


    def move_to(self, new_loc, num_pieces):
        """
        Moves the self to the new location
        """
        self.update_heuristic()
        self.stack_size = self.board.move_pieces(self.location, new_loc, num_pieces)
        self.location = new_loc


    def update_heuristic(self):
        """
        Calculates the heuristic value based off the location
        """
        self.heuristic = self.manhattan_distance()

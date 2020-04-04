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


    def manhattan_distance(self):
        """
        Calculate the manhattan distance from node's current location to the
        target location
        """
        return abs(self.location[0] - target_location[0]) + \
               abs(self.location[1] - target_location[1])


    def move_to(self, new_loc):
        """
        Moves the self to the new location
        """
        self.location = new_loc

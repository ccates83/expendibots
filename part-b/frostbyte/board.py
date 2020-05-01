#
#   Representation of the board for the solver to store
#

class Board():
    def __init__(self):
        """
        Init function
        """

        # The initial state of the board is always the same for each game
        self.state = {
            "white": [(1, (0, 0)), (1, (0, 1)), (1, (1, 0)), (1, (1, 1)),
                      (1, (3, 0)), (1, (3, 1)), (1, (4, 0)), (1, (4, 1)),
                      (1, (6, 0)), (1, (6, 1)), (1, (7, 0)), (1, (7, 1))],
            "black": [(1, (0, 6)), (1, (0, 7)), (1, (1, 6)), (1, (1, 7)),
                      (1, (3, 6)), (1, (3, 7)), (1, (4, 6)), (1, (4, 7)),
                      (1, (6, 6)), (1, (6, 7)), (1, (7, 6)), (1, (7, 7))]
        }


    def update(self, action):
        """
        Update the state of the board with the given action - no checks for validity
        """
        print("UPDATING INTERNAL BOARD STATE")
        if action[0] == "BOOM":
            print("explode")
            self.perform_boom(action[1])
        else:
            print("move")

        print(self.state["white"])


    def perform_boom(self, loc):
        if not self.is_occupied(loc):
            return

        self.clear_tile(loc)

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    self.perform_boom((loc[0]+i, loc[1]+j))


    def is_occupied(self, loc):
        return self.is_occupied_by_black(loc) or self.is_occupied_by_white(loc)


    def is_occupied_by_white(self, loc):
        for white in self.state["white"]:
            if loc == white[1]: return True
        return False

    def is_occupied_by_black(self, loc):
        for black in self.state["black"]:
            if loc == black[1]: return True

        return False


    def clear_tile(self, loc):
        """
        Remove all tokens from a tile
        """
        for white in self.state["white"]:
            if loc == white[1]:
                self.state["white"].remove(white)
        for black in self.state["black"]:
            if loc == black[1]:
                self.state["black"].remove(black)


    def print(self):
        # DEBUG: For debugging purposes only
        whites = []
        for elem in self.state["white"]:
            whites.append(elem[1])
        blacks = []
        for elem in self.state["black"]:
            blacks.append(elem[1])

        for i in reversed(range(0, 8)):
            row = "|"
            for j in range(0, 8):
                if (j, i) in whites:
                    row += " w |"
                elif (j, i) in blacks:
                    row += " b |"
                else:
                    row += " . |"
            print(row)

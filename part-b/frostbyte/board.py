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


    def print(self):
        """
        Debug print statement for our internal testing
        """
        whites = []
        for elem in self.state["white"]:
            whites.append(elem[1])
        blacks = []
        for elem in self.state["black"]:
            blacks.append(elem[1])

        for i in reversed(range(0, 8)):
            row = "|"
            for j in range(0, 8):
                n = 0
                t = "_"
                for white in self.state["white"]:
                    if (j, i) == white[1]:
                        n = white[0]
                        t = "w"
                for black in self.state["black"]:
                    if (j, i) == black[1]:
                        n = black[0]
                        t = "b"

                if n == 0:
                    row += "____|"
                else:
                    row += " {}{} |".format(n, t)

            print(row)


    def update(self, colour, action):
        """
        Wrapper to be called when a player makes a move
        """
        self.perform_action(colour, action)


    def perform_action(self, colour, action):
        """
        Execute an action from the project spec
        """
        if action[0] == "MOVE":
            self.move(colour, action[1], action[2], action[3])
        elif action[0] == "BOOM":
            self.explode(action[1])
        else:
            print("INVALID ACTION")


    def move(self, colour, n, loc1, loc2):
        """
        Apply a move for the board. Assumes valid. Validates in apply_action()
        """
        for piece in self.state[colour]:
            # Find the piece
            if piece[1] == loc1:
                #Decide whether to unstack or move them all
                if piece[0] == n:
                    # Move all pieces
                    self.clear_location(loc1)
                else:
                    # Unstack
                    new_piece = (piece[0]-n, loc1)
                    self.clear_location(loc1)
                    self.state[colour].append(new_piece)
                self.place_pieces(colour, n, loc2)
                return



    def explode(self, loc, already_exploded=[]):
        """
        Execute an explosion on the board
        """
        if not self.is_occupied(loc):
            return

        self.clear_location(loc)
        already_exploded.append(loc)

        for i in range(-1, 2):
            for j in range(-1, 2):
                next_loc = (loc[0]+i, loc[1]+j)
                self.explode(next_loc, already_exploded)



    def clear_location(self, loc):
        """
        Clear a location of all pieces
        """
        for white in self.state["white"]:
            if white[1] == loc:
                self.state["white"].remove(white)
                return
        for black in self.state["black"]:
            if black[1] == loc:
                self.state["black"].remove(black)
                return


    def place_pieces(self, colour, n, loc):
        """
        Place n pieces for the given player (colour) at loc
        """
        # Check if we need to stack
        for piece in self.state[colour]:
            if piece[1] == loc:
                new_piece = (piece[0]+n, loc)
                self.state[colour].remove(piece)
                self.state[colour].append(new_piece)
                return

        # if we dont stack, just add the piece
        self.state[colour].append((n, loc))



    #
    # Helpers
    #
    def is_occupied_by_black(self, loc):
        """
        Check if a given location is occupied by black
        """
        for black in self.state["black"]:
            if loc == black[1]:
                return True
        return False


    def is_occupied_by_white(self, loc):
        """
        Check if a given location is occupied by white
        """
        for white in self.state["white"]:
            if loc == white[1]:
                return True
        return False


    def is_occupied(self, loc):
        """
        Check if a given location is occupied
        """
        return self.is_occupied_by_black(loc) or self.is_occupied_by_white(loc)


    def in_bounds(self, loc):
        """
        Check if a location is on the board
        """
        return loc[0] > -1 and loc[0] < 8 and loc[1] > -1 and loc[1] < 8


    def is_valid_action(self, colour, action):
        """
        Check if an action is valid for this board and the given player
        """
        if action[0] == 'BOOM':
            in_bounds = self.in_bounds(action[1])
            if colour == "white":
                correct_piece = self.is_occupied_by_white(action[1])
            else:
                correct_piece = self.is_occupied_by_black(action[1])
            return in_bounds and correct_piece

        dest_in_bounds = self.in_bounds(action[3])
        selected_in_bounds = self.in_bounds(action[2])
        if colour == "white":
            correct_piece = self.is_occupied_by_white(action[2])
            good_target = not self.is_occupied(action[3]) or self.is_occupied_by_white(action[3])
        else:
            correct_piece = self.is_occupied_by_black(action[2])
            good_target = not self.is_occupied(action[3]) or self.is_occupied_by_black(action[3])


        return dest_in_bounds and selected_in_bounds and correct_piece and good_target

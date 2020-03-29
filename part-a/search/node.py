BOARD_SIZE_MIN = 0
BOARD_SIZE_MAX = 7

class Node():
    def __init__(self, piece_number, state, parent):
        self.state = state
        self.piece_number = piece_number
        self.parent = parent # parent node
        #self.action = action # move up, left, down, right
        #self.depth = depth # depth of the node in the tree
        #self.step_cost = step_cost # g(n), the cost to take the step
        #self.path_cost = path_cost # accumulated g(n), the cost to reach the current node

        self.piece = self.state["white"][self.piece_number] # identify white piece to operate on
        self.new_state = self.state.copy()

        # children node
        self.move_up = None
        self.move_left = None
        self.move_down = None
        self.move_right = None

    # check if chosen white piece move lands on black piece
    def lands_on_black_check(self, new_x, new_y):
        for i in self.state["black"]:
            if new_x == i[1] and new_y == i[2]:
                return True

    # check if chosen white piece move lands on white piece
    def lands_on_white_check(self, new_x, new_y, pieces_to_move):
        for i in self.state["white"]:
            if new_x == i[1] and new_y == i[2]:
                i[0]+= pieces_to_move # add moved pieces to newly formed white stack
                if pieces_to_move == self.piece[0]: # if moving all pieces delete the original white piece
                    del self.new_state["white"][self.piece_number]
                else: # else decrease the number of pieces in the original stack
                    self.piece[0] -= pieces_to_move
                return True

    def try_move_up(self, move_distance, pieces_to_move):
        new_x = self.piece[1] # x stays the same
        new_y = self.piece[2] + move_distance # y moves up by n
        # check if move by n is valid
        if new_y > BOARD_SIZE_MAX:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white_check(new_x, new_y, pieces_to_move):
            return self.new_state
        else:
            if pieces_to_move == self.piece[0]: # if moving all pieces in stack just change the y variable
                self.new_state["white"][self.piece_number][2] = new_y
            else: # else decrease number of pieces in original stack and add new piece location to white list
                self.new_state["white"][self.piece_number][0] -= pieces_to_move
                self.new_state["white"].append([pieces_to_move,new_x,new_y])
            return self.new_state

    def try_move_down(self, move_distance, pieces_to_move):
        new_x = self.piece[1] # x stays the same
        new_y = self.piece[2] - move_distance # y moves down by n
        # check if move by n is valid
        if new_y < BOARD_SIZE_MIN:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white_check(new_x, new_y, pieces_to_move):
            return self.new_state
        else:
            if pieces_to_move == self.piece[0]:
                self.new_state["white"][self.piece_number][2] = new_y
            else:
                self.new_state["white"][self.piece_number][0] -= pieces_to_move
                self.new_state["white"].append([pieces_to_move,new_x,new_y])
            return self.new_state

    def try_move_right(self, move_distance, pieces_to_move):
        new_x = self.piece[1] + move_distance # x moves right by n
        new_y = self.piece[2] # y stays the same
        # check if move by n is valid
        if new_x > BOARD_SIZE_MAX:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white_check(new_x, new_y, pieces_to_move):
            return self.new_state
        else:
            if pieces_to_move == self.piece[0]:
                self.new_state["white"][self.piece_number][1] = new_x
            else:
                self.new_state["white"][self.piece_number][0] -= pieces_to_move
                self.new_state["white"].append([pieces_to_move,new_x,new_y])
            return self.new_state


    def try_move_left(self, move_distance, pieces_to_move):
        new_x = self.piece[1] - move_distance # x moves left by n
        new_y = self.piece[2] # y stays the same
        # check if move by n is allowable
        if new_x < BOARD_SIZE_MIN:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white_check(new_x, new_y, pieces_to_move):
            return self.new_state
        else:
            if pieces_to_move == self.piece[0]:
                self.new_state["white"][self.piece_number][1] = new_x
            else:
                self.new_state["white"][self.piece_number][0] -= pieces_to_move
                self.new_state["white"].append([pieces_to_move,new_x,new_y])
            return self.new_state

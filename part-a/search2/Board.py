class ExpBoard():
    """
    Object to represent the board and key functionality from the board data
    """
    def __init__(self, data, size):
        self.data = data
        self.whites = data["white"]
        self.blacks = data["black"]
        self.board_size = size


    def get_state(self):
        return self.data


    def get_whites(self):
        return self.whites


    def get_blacks(self):
        return self.blacks


    def is_valid(self, loc):
        return loc[0] < self.board_size and loc[0] > -1 and \
               loc[1] < self.board_size and loc[1] > -1


    def is_occupied_by_black(self, loc):
        for black in self.blacks:
            if loc == (black[1], black[2]):
                return True
        return False

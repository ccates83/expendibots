from frostbyte.board import *

class UserPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation.
        self.state = Board()


    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        self.state.print()
        return self.choose_action()


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        # TODO: Update state representation in response to action.
        print("UPDATING")
        self.state.update(action, colour)

    def is_valid_move(self, old_coord, new_coord, num_pieces):
        if not self.state.is_occupied(old_coord): return False
        return True

    def get_coordinates(self):
        """
        Gets the coordinates of a piece from the user.
        """
        print("x coord of piece:")
        x = int(input())
        print("y coord of piece:")
        y = int(input())

        return (x, y)

    def choose_action(self):
        """
        Takes user input in order to perform an action to take.
        """

        print("Please enter the coordinates of the piece you wish to take an action with")
        old_coord = self.get_coordinates()

        print("Move or explode? type 'move' or 'boom'")
        action = input()

        if action == "boom":
            print("you chose to explode at ({}, {})".format(old_coord[0], old_coord[1]))
            return ("BOOM", old_coord)
        elif action == "move":
            print("You chose to move, where would you like to move to?")
            new_loc = self.get_coordinates()
            print("How many pieces would you like to move?")
            n = int(input())

            if self.is_valid_move(old_coord, new_loc, n):
                print("You chose to move {} piece from {} to {}.".format(n, old_coord, new_loc))
                return ("MOVE", n, old_coord, new_loc)
            else:
                print("That is not a valid move, please try again.")
                return self.choose_action()

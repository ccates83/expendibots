from frostbyte.board import *
from frostbyte.util import *
import random


class RandPlayer:


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
        # Representation of the board for the player class
        self.state = Board()
        self.colour = colour
        self.actions = []


    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """

        all_actions = list_all_possible_moves(self.colour, self.state)
        action = all_actions[random.randint(0, len(all_actions)-1)]
        self.state.print()

        f = open("records.txt", "a")
        f.write("{}".format(action))
        f.close()

        return action


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
        self.state.update(colour, action)
        self.actions.append(action)


    #
    #   HELPERS
    #



    # Game State functions
    def did_win(self):
        """
        Check if the current player won
        """
        if self.colour == "white":
            return self.state.state["white"] and not self.state.state["black"]
        else:
            return not self.state.state["white"] and self.state.state["black"]

    def did_lose(self):
        """
        Check if the current player lost
        """
        if self.colour == "white":
            return not self.state.state["white"]
        else:
            return not self.state.state["black"]


    # Algorithmic functions
    def two_ply(self, root_node):
        """
        Search two moves ahead
        """
        current_best = -100000 # Init to a crazy low value that will never be the best, first option will take over

        for child in root_node.children:
            print(child.colour, ":", child)
            # for grandchild in child.children:
            #     print("\tTheir move score:", grandchild.value)

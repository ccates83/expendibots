from frostbyte.board import *
from frostbyte.util import *


class ExamplePlayer:


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


    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        # self.state.print()
        actions = list_all_possible_moves(self.colour, self.state)

        # Evaluate boom actions. If we win immediately do it, if it betters our ratio
        # of our pieces to opponents pieces, do the one that gives the best new ratio
        current_ratio = get_ratio(self.colour, self.state)
        best = current_ratio
        boom_to_execute = None
        for boom in get_booms(actions):
            test = test_boom(self.state, self.colour, boom)
            if did_win(self.colour, test):
                return boom

            new_ratio = get_ratio(self.colour, test)
            if new_ratio > best:
                best = new_ratio
                boom_to_execute = boom

        if boom_to_execute:
            return boom_to_execute

        # If none of the boom actions are in our favor, take the best move
        pointed = point_actions(self.colour, actions)
        pointed.sort(reverse=True)
        return pointed[0][1]


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

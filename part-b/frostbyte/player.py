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
        #
        #   ALGORITHM:
        #       Use the calculated book learned values to judge which move the opp would
        #       take and our move, get the best difference so that overall our move is better.
        #
        #   POTENTIAL IMPROVEMENT:
        #       - Incorporate the optimal stopping problem - look through 37% of the paths then take
        #           the next move that is better than ones we have seen.
        #
        #       - Another way of pruning...?
        #

        our_queue = create_action_queue(self.colour, self.state)
        our_queue_len = len(our_queue)
        current_best_difference = None
        best_move = None

        # If our queue only is 1 element to begin, we chose a boom
        if our_queue_len == 1:
            return our_queue[0]

        i = 0
        while our_queue:
            tup = our_queue.pop(0)
            our_action = tup[1]
            our_action_value = tup[0]

            # Calculate their likely move off of ours
            temp = test_action(self.state, self.colour, our_action)
            tup = calculate_next_action(get_opp_colour(self.colour), temp)
            opp_action_value = tup[0]

            # If we think our opponent would explode next, dont do that move
            if type(opp_action_value) is not int: continue

            # Decide if this is the best so far
            diff = our_action_value - opp_action_value
            if not current_best_difference:
                current_best_difference = diff
                best_move = our_action
            elif diff > current_best_difference:
                best_move = our_action
                # If we have seen 37% of the options, take the next best
                if i / our_queue_len > 0.37:
                    return best_move
                current_best_difference = diff

            # Update our progress through the queue
            i += 1

        return best_move

        # print(create_action_queue(self.colour, self.state))

        # return calculate_next_action(self.colour, self.state)


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

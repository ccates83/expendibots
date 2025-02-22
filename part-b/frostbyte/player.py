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
        return self.four_ply()


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
        self.state.update(colour, action)


    def two_ply(self):
        """
        two play search for the player
        """
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
            if type(opp_action_value) is not int:
                # If their explosion would be in our favor, do it
                temp_opp = test_action(temp, get_opp_colour(self.colour), tup[1])
                if get_ratio(self.colour, temp_opp) > get_ratio(self.colour, temp):
                    return our_action
                else: continue

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



    def four_ply(self):
        """
        4-ply Search algorithm for the player
        """
        first_move_queue = create_action_queue(self.colour, self.state)
        first_move_queue_len = len(first_move_queue)

        if first_move_queue_len == 1:
            return first_move_queue[0]

        current_best_difference = None
        current_best_move = None

        progress = 0
        while first_move_queue:
            tup = first_move_queue.pop(0)
            our_first_move = tup[1]
            our_first_move_value = tup[0]

            # Optimal stopping problem search limit
            if progress / first_move_queue_len > 0.37:
                break

            test_first_action_state = test_action(self.state, self.colour, our_first_move)
            tup = calculate_next_action(get_opp_colour(self.colour), test_first_action_state)
            opp_first_action = tup[1]
            opp_first_action_value = tup[0]

            # If we calculate that the next move would mean the opp blowing up in their favor, shortcircuit
            if opp_first_action_value == 'BOOM':
                continue

            # Look ahead the next two moves
            second_state = test_action(test_first_action_state, get_opp_colour(self.colour), opp_first_action)
            second_move_queue = create_action_queue(self.colour, second_state)
            second_move_queue_len = len(second_move_queue)

            if second_move_queue_len == 1:
                return our_first_move

            progress2 = 0
            while second_move_queue:
                tup = second_move_queue.pop(0)
                our_second_move = tup[1]
                our_second_move_value = tup[0]

                # Optimal stopping problem search limit
                if progress2 / second_move_queue_len > 0.37:
                    break

                test_second_action_state = test_action(second_state, self.colour, our_second_move)
                tup = calculate_next_action(get_opp_colour(self.colour), test_second_action_state)
                opp_second_action = tup[1]
                opp_second_action_value = tup[0]

                # If we calculate that the next move would mean the opp blowing up in their favor, shortcircuit
                if opp_second_action_value == 'BOOM':
                    continue

                diff = (our_first_move_value + our_second_move_value) - (opp_first_action_value + opp_second_action_value)
                if not current_best_difference:
                    current_best_difference = diff
                    current_best_move = our_first_move
                elif diff > current_best_difference:
                    current_best_move = our_first_move
                    current_best_difference = diff

                progress2 += 1

            progress += 1

        return current_best_move

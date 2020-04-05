from search2.util import *
from search2.Action import *
from search2.Node import *

from copy import deepcopy

class Solver():
    """
    Class object to perform all actions of finding the winning solution to the
    game.
    """
    def __init__(self, board):
        """
        Init
        """
        self.board = board
        self.actions = []


    def solve(self):
        """
        Finds the solution and stores every move of the successful path in self.actions
        to be printed later. Once a node reaches a goal state, call with new board state
        after the explosion.
        """
        # Step 1: Find the target locations in order of priority
        print("# Step 1: find target locs")
        target_locations = list_target_locations(self.board)
        print("# Targets:", target_locations)
        print("#\n#\n#")

        # Step 2: Try to move each white to each target and see if we win
        #
        #   TODO: Use the node closest to the target first
        #
        start_nodes = []
        for white in self.board.get_whites():
            for target in target_locations:
                node = Node(self.board, get_piece_location(white), white[0], target[1])
                start_nodes.append(node)
                print("\nStart:", node, "to", target[1])
                self.search(node, target[1])


    def search(self, start_node, target_location, visited=[]):
        """
        Find the solution path from the start  node to the target location
        """
        # Base case - we have reached the target
        if start_node.location == target_location:
            print("EXPLODE HERE")
            return True

        current_x = start_node.location[0]
        current_y = start_node.location[1]

        visited.append(start_node.location)

        queue = []
        # Try each path, sort by manhattan distance low to high
        #
        # TODO: Allow stacking and unstacking
        # for pieces_to_move in range(1, start_node.stack_size):
        for distance in range(1, start_node.stack_size+1):
            # up
            new_loc = (current_x, current_y + distance)
            if valid_move(self.board, new_loc, visited):
                up_node = deepcopy(start_node)
                up_node.move_to(new_loc, up_node.stack_size)
                queue.append(up_node)

            # down
            new_loc = (current_x, current_y - distance)
            if valid_move(self.board, new_loc, visited):
                down_node = deepcopy(start_node)
                down_node.move_to(new_loc, down_node.stack_size)
                queue.append(down_node)

            # left
            new_loc = (current_x - distance, current_y)
            if valid_move(self.board, new_loc, visited):
                left_node = deepcopy(start_node)
                left_node.move_to(new_loc, left_node.stack_size)
                queue.append(left_node)

            # right
            new_loc = (current_x + distance, current_y)
            if valid_move(self.board, new_loc, visited):
                right_node = deepcopy(start_node)
                up_node.move_to(new_loc, right_node.stack_size)
                queue.append(right_node)

        # Sort the queue by heuristic value
        queue.sort(key=lambda node: node.heuristic)
        for elem in queue:
            print(elem)


    def print_actions(self):
        """
        Prints the actions taken by the solver to the solution of the board
        """
        print("#\n# Solution #")
        for action in self.actions:
            action.print()

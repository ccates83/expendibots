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
        # Check if we the game is over
        if self.did_win(): return True
        if self.did_lose(): return False

        # Step 1: Find the target locations in order of priority
        target_locations = list_target_locations(self.board)

        # Step 2: Iterate through start states and solve
        #
        #   Algorithm:
        #       - for each target location, list the white pieces by distance (low-high)
        #           - create a start state from that piece and target location
        #           - try to solve using the start state
        for target in target_locations:
            for tup in list_pieces_by_distance(self.board.get_whites(), target[1]):
                print("\n\n\n")
                print("----- {} to {} -----\n".format(tup[1], target))
                # For each targte location, try each white piece as a starting node
                # in order, closest to the target first
                white = tup[1]
                node = Node(self.board, get_piece_location(white), white[0], target[1])
                if self.search(node, target[1], visited=[]):
                    self.actions += node.actions
                    return True


    def find_next_moves(self, current_node, target_location, visited=[]):
        """
        Return a list of the next moves (nodes) to explore from the current_node
        """
        current_x = current_node.location[0]
        current_y = current_node.location[1]

        visited.append(current_node.location)

        queue = []
        # Try each path, sort by manhattan distance low to high
        #
        # Steps:
        #   - Check if the move location is valid
        #   - Create a new node and move it to that location, updating the board state
        #   - Increment the depth of the new node
        #   - Add that new node holding the state of the board to a queue of paths to try
        #
        # TODO: Allow stacking and unstacking - board class handles functionality, just
        #       need to add those moves into the queue
        # for pieces_to_move in range(1, start_node.stack_size):
        for distance in range(1, current_node.stack_size+1):
            # up
            new_loc = (current_x, current_y + distance)
            if valid_move(self.board, new_loc, visited):
                up_node = deepcopy(current_node)
                up_node.move_to(new_loc, up_node.stack_size)
                up_node.depth += 1
                queue.append(up_node)

            # down
            new_loc = (current_x, current_y - distance)
            if valid_move(self.board, new_loc, visited):
                down_node = deepcopy(current_node)
                down_node.move_to(new_loc, down_node.stack_size)
                down_node.depth += 1
                queue.append(down_node)

            # left
            new_loc = (current_x - distance, current_y)
            if valid_move(self.board, new_loc, visited):
                left_node = deepcopy(current_node)
                left_node.move_to(new_loc, left_node.stack_size)
                left_node.depth += 1
                queue.append(left_node)

            # right
            new_loc = (current_x + distance, current_y)
            if valid_move(self.board, new_loc, visited):
                right_node = deepcopy(current_node)
                right_node.move_to(new_loc, right_node.stack_size)
                right_node.depth += 1
                queue.append(right_node)

        return queue


    def search(self, node, target_location, visited=[], queue=[]):
        """
        Find the solution path from the start  node to the target location
        """
        node.board.print()

        # Base Case 1 - we won the game
        if node.board.get_blacks() == []:
            return True

        # Base Case 2 - we lost
        if not node.board.get_whites() and node.board.get_blacks():
            return False

        # Base Case 3 - Depth limit exceeded, prune this branch
        if node.depth > node.depth_limit:
            print("---- Depth Limit Reached ----")
            return False

        # Recursive Case 1 - If we hit our target, move on the the next white piece
        if node.location == target_location:
            node.explode()

            # Search with the next white and the updated board state
            new_solver = Solver(node.board)
            new_solver.actions += node.actions
            return new_solver.solve()

        # Find all the next moves the node can take
        next_moves = self.find_next_moves(node, target_location, visited)

        # Sort the queue by heuristic value
        queue = next_moves
        queue.sort(key=lambda node: node.heuristic)

        # Try each path
        for node in queue:
            if self.search(node, target_location, visited, queue):
                return True


    def did_win(self):
        return not self.board.get_blacks()


    def did_lose(self):
        return self.board.get_blacks() and not self.board.get_whites()


    def print_actions(self):
        """
        Prints the actions taken by the solver to the solution of the board
        """
        print("# -Solution- #")
        print("# Solved in {} turns".format(len(self.actions)))
        for action in self.actions:
            action.print()
        print("#    -----   #")

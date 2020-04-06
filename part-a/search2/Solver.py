from search2.util import *
from search2.Node import *

from copy import deepcopy

class Solver():
    """
    Class object to perform all actions of finding the winning solution to the
    game.
    """
    def __init__(self, board, path=[]):
        """
        Init
        """
        self.board = board
        self.path = path


    def print(self):
        """
        print for debugging the solver
        """
        print("# SOLVER OBJECT:")
        print("# board:")
        self.board.print()
        print("# path:", self.path)
        print("#\n#")


    def solve(self, path=[]):
        """
        Finds the solution and stores every move of the successful path in self.actions
        to be printed later. Once a node reaches a goal state, call with new board state
        after the explosion.
        """

        # Check if we the game is over
        if self.did_win():
            # self.print_actions()
            return True
        if self.did_lose():
            print("# This path failed")
            return False

        # Step 1: Find the target locations in order of priority
        target_locations = list_target_locations(self.board)

        # Step 2: Iterate through start states and solve
        #
        #   Algorithm:
        #       - for each target location, list the white pieces by distance (low-high)
        #           - create a start state from that piece and target location
        #           - try to solve using the start state



        for piece in self.board.get_whites():
            for target in list_targets_by_distance(piece, target_locations):
                piece_loc = (piece[1], piece[2])
                n = piece[0]
                target_loc = target[1]
                node = Node(board=deepcopy(self.board), location=piece_loc, stack_size=n, target_location=target_loc)
                print("# Trying new start state:", node)
                node.print_board()
                result = self.search(node, visited=[])
                # If the search finds a solution, return true that we found a solution to the game
                self.print()
                if result:
                    return True
                print("move on")

        return False

        # Iterate through each target location
        for target in target_locations:
            piece_queue = list_pieces_by_distance(self.board.get_whites(), target[1])
            target_loc = target[1]
            # Iterate through each piece, matching each with each target location
            for piece in piece_queue:
                self.current_target_reached = False
                loc = (piece[1][1], piece[1][2])
                n = piece[1][0]
                # Create a new node with the start state of the board with each piece and location
                node = Node(board=deepcopy(self.board), location=loc, stack_size=n, target_location=target_loc)
                # Try to solve using this node
                print("# Trying new start state:", node)
                node.print_board()
                result = self.search(node, visited=[])
                # If the search finds a solution, return true that we found a solution to the game
                self.print()
                if result:
                    return True
                print("move on")


    def find_next_moves(self, current_node, target_location, visited=[]):
        """
        Return a list of the next moves (nodes) to explore from the current_node
        """
        current_x = current_node.location[0]
        current_y = current_node.location[1]

        moves = []
        # Look ahead to each move, sort by manhattan distance low to high
        #
        # Steps:
        #   - Check if the move location is valid
        #   - Create a new node and move it to that location, updating the board state
        #   - Increment the depth of the new node
        #   - Add that new node holding the state of the board to a queue of paths to try
        #
        # TODO: Allow stacking and unstacking - board class handles functionality, just
        #       need to add those moves into the queue

        # Create new states for each combination of possible moves for the current node
        #   - Move 1 to n pieces a distance of 1 to n tiles
        for num_pieces in range(1, current_node.stack_size+1):
            for step in range(1, current_node.stack_size+1):
                print("#\n# Move {} pieces {} tiles".format(num_pieces, step))

                # For each direction:
                #   - copy the current node
                #   - move the copied node using the new location and num pieces we are moving
                #   - append newly copied and moved node to the list of moves the current node can take

                # Up
                new_loc = (current_x, current_y + step)
                if valid_move(current_node.board, new_loc, visited):
                    up_node = current_node.copy()
                    up_node.move_to(new_loc, num_pieces)
                    moves.append(up_node)
                else:
                    print("# {} is not a valid move location".format(new_loc))

                # Down
                new_loc = (current_x, current_y - step)
                if valid_move(current_node.board, new_loc, visited):
                    down_node = current_node.copy()
                    down_node.move_to(new_loc, num_pieces)
                    moves.append(down_node)
                else:
                    print("# {} is not a valid move location".format(new_loc))

                # Right
                new_loc = (current_x + step, current_y)
                print("Move righ to", new_loc)
                if valid_move(current_node.board, new_loc, visited):
                    right_node = current_node.copy()
                    right_node.move_to(new_loc, num_pieces)
                    moves.append(right_node)
                else:
                    print("# {} is not a valid move location".format(new_loc))

                # Left
                new_loc = (current_x - step, current_y)
                if valid_move(current_node.board, new_loc, visited):
                    left_node = current_node.copy()
                    left_node.move_to(new_loc, num_pieces)
                    moves.append(left_node)
                else:
                    print("# {} is not a valid move location".format(new_loc))

        return moves


    def search(self, node, visited=[]):
        """
        Find the solution path from the start node to the target location
        """
        print("#\n# --- Trying to move <{}> to {}".format(node, node.target_location))
        node.print_board()
        visited.append(node.location)
        print("# Visited locations", visited)


        # Base Case - Depth limit exceeded, prune this branch
        if node.at_depth_limit():
            print("---- Depth Limit Reached ----")
            return False

        # Goal state case: we have reached the target location
        if node.at_target():
            self.current_target_reached = True
            explosion_node = node.copy()
            print("\n\n\n# EXPLODE #")
            explosion_node.explode()
            print("# Making new solver for state after the explosion:")
            new_solver = Solver(deepcopy(explosion_node.board))
            print(new_solver.board.data)
            new_solver.print()
            # Try the solution with this explosion, only if this potential solution
            # is successful fo we return out of here, otherwise continue without the
            # Explosion
            return new_solver.solve()
            # result = new_solver.solve()
            # if result:
            #     print("Solution found")
            #     return True

        print("# NO EXPLOSION, continuing with:", node)


        # If the current node hasn't reached our target location, queue each potential
        # move as a new node to search based off of
        # self.print()
        next_moves = self.find_next_moves(node, node.target_location, visited)

        # Sort the next moves by which brings us closest to the target location
        next_moves.sort(key=lambda node: node.heuristic)
        print("# \n# Next moves for {}:".format(node))
        for node in next_moves:
            print("#\t", node.heuristic, node)

        # Try each move in order
        for move in next_moves:
            print("# Attempting {} move to".format(move.stack_size), move.location)
            move.print_board()
            # Only try the moves if the node never reached its target
            result = self.search(move, deepcopy(visited))
            # If the path from this move finds a solution, return True
            if result:
                return True

        print("#\n# No more moves for", node)
        print("#")

        return False

        # # Find all the next moves the node can take
        # next_moves = self.find_next_moves(node, target_location, visited)
        #
        # # Sort the queue by heuristic value
        # next_moves.sort(key=lambda node: node.heuristic)
        #
        # # Try each path
        # for node in next_moves:
        #     # If the path finds a solution, back out and return true
        #     if self.search(node, target_location, visited, deepcopy(node.path)):
        #         return True


    def did_win(self):
        return not self.board.get_blacks()


    def did_lose(self):
        return self.board.get_blacks() and not self.board.get_whites()


    def print_actions(self):
        """
        Prints the actions taken by the solver to the solution of the board
        """
        print("#\n# --- SOLUTION --- \n#")
        curr_loc = self.path[0][1]
        for elem in self.path[1:]:
            if elem == "EXPLODE":
                print_boom(curr_loc[0], curr_loc[1])
                if self.path.index(elem)+1 != len(self.path):
                    curr_loc = self.path[self.path.index(elem)+1][1]
            else:
                next_loc = elem[1]
                if next_loc != curr_loc:
                    n = elem[0]
                    print_move(n, curr_loc[0], curr_loc[1], next_loc[0], next_loc[1])
                    curr_loc = next_loc

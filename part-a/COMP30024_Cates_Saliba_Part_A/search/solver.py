from search.util import *
from search.node import *
from search.board import *
from search.Constants import *

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
        self.target_reached = False


    def print(self):
        """
        print for debugging the solver
        """
        print("# SOLVER OBJECT:")
        print("# board:")
        self.board.print()


    def solve(self):
        """
        Finds the solution and stores every move of the successful path in self.actions
        to be printed later. Once a node reaches a goal state, call with new board state
        after the explosion.
        """
        # Check if we the game is over
        if self.did_win():
            self.print_actions()
            return True
        if self.did_lose():
            return False

        # Step 1:
        # Find the target locations in order of priority
        target_locations = self.get_targets()

        # Step 2:
        # Match the target location with each piece, sorted by distance from the target
        queue = []
        for target in target_locations:
            for piece in list_pieces_by_distance(self.board.get_whites(), target):
                queue.append((target, piece))

        # Step 3:
        # Sort the queue of (target, piece) pairs by the manhattan distance between them
        queue.sort(key=lambda tup: calculate_manhattan_distance(tup[0], (tup[1][1], tup[1][2])))

        # Step 4:
        # Try each element of the queue as a start state. If a solution is found we
        # return True and are done
        for elem in queue:
            target = elem[0]
            piece = elem[1]
            self.target_reached = False
            piece_loc = (piece[1], piece[2])
            n = piece[0]
            new_path = deepcopy(self.path)
            node = Node(board=deepcopy(self.board), location=piece_loc, stack_size=n, target_location=target, path=new_path)
            result = self.search(node, visited=[])

            # If the search finds a solution, return true that we found a solution to the game
            if result:
                return True

        # If no solution is found, return False, meaning the board cannot be won
        return False


    def find_next_moves(self, current_node, target_location, visited=[]):
        """
        Return a list of the next moves (nodes) to explore from the current_node
        """
        # If we have already hit the target, there are no potential moves for this node
        if self.target_reached:
            return []

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

        # Create new states for each combination of possible moves for the current node
        #   - Move 1 to n pieces a distance of 1 to n tiles
        for num_pieces in range(1, current_node.stack_size+1):
            for step in range(1, current_node.stack_size+1):
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

                # Down
                new_loc = (current_x, current_y - step)
                if valid_move(current_node.board, new_loc, visited):
                    down_node = current_node.copy()
                    down_node.move_to(new_loc, num_pieces)
                    moves.append(down_node)

                # Right
                new_loc = (current_x + step, current_y)
                if valid_move(current_node.board, new_loc, visited):
                    right_node = current_node.copy()
                    right_node.move_to(new_loc, num_pieces)
                    moves.append(right_node)

                # Left
                new_loc = (current_x - step, current_y)
                if valid_move(current_node.board, new_loc, visited):
                    left_node = current_node.copy()
                    left_node.move_to(new_loc, num_pieces)
                    moves.append(left_node)

        return moves


    def search(self, node, visited=[]):
        """
        Find the solution path from the start node to the target location
        """
        # If we call search and the current target location has already been tried,
        # stop seaching
        if self.target_reached:
            return False

        visited.append(node.location)

        # Base Case - Depth limit exceeded, prune this branch
        # if node.at_depth_limit():
        #     # print("---- Depth Limit Reached ----")
        #     return False

        # Goal state case: we have reached the target location
        if node.at_target():
            self.target_reached = True
            node.explode()
            new_solver = Solver(deepcopy(node.board))

            # Try the solution with this explosion, only if this potential solution
            # is successful fo we return out of here, otherwise continue without the
            # Explosion
            new_solver.path = deepcopy(node.path)
            new_solver.path.append(("EXPLODE", node.location))
            return new_solver.solve()

        # If the current node hasn't reached our target location, queue each potential
        # move as a new node to search based off of
        next_moves = self.find_next_moves(node, node.target_location, visited)

        # Sort the next moves by which brings us closest to the target location
        next_moves.sort(key=lambda node: node.heuristic)

        # Try each move in order
        for move in next_moves:
            result = self.search(move, deepcopy(visited))
            # If the path from this move finds a solution, return True
            if result:
                return True

        return False


    def did_win(self):
        """
        Check if the win state has been reached
        """
        return not self.board.get_blacks()


    def did_lose(self):
        """
        Check if we have lost the game
        """
        return self.board.get_blacks() and not self.board.get_whites()


    def print_actions(self):
        """
        Prints the actions taken by the solver to the solution of the board. An
        action is either a move or an explosion. They are represented in the list
        as:
            - ("move", old_loc, new_loc)
            - ("EXPLODE", explosion_location)
        """
        print("#\n# --- SOLUTION --- \n#")
        for action in self.path:
            if action[0] == "EXPLODE":
                print_boom(action[1][0], action[1][1])
            else:
                print_move(action[0], action[1][0], action[1][1], action[2][0], action[2][1])


    def get_targets(self):
        """
        Get the target locations for the board state
        """
        targets = []

        # For all the potential targets, test if they cause us to lose. If so,
        # do not include them in the final list of target locations
        potential_targets = list_target_locations(self.board)
        for target in potential_targets:
            loc = target[1]

            # Create a node to test the explosion
            test_board = ExpBoard(deepcopy(self.board.data), BOARD_SIDE_LENGTH)
            test_board.place_pieces(loc, 1)
            test_node = Node(board=test_board, location=loc, stack_size=1, target_location=loc)
            test_node.explode()

            if not (not test_node.board.get_whites() and test_node.board.get_blacks()):
                targets.append(loc)

        # Sort the targets by which has the highest heuristic (most blacks exploded)
        targets.sort(key=lambda loc: calculate_heuristic_value(self.board, loc), reverse=True)
        return targets

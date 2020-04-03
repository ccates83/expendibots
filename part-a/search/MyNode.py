BOARD_SIZE_MIN = 0
BOARD_SIZE_MAX = 7

import search.my_util as MyUtil
from search.board import *
from search.priority_queue import *
from copy import deepcopy

class MyNode():
    """
    My Node class, rewriting to clean up the code
    """
    def __init__(self, board, location, stack_size, visited_nodes=[], actions=[]):
        """
        Init
        """
        self.board = board# Board representation
        self.location = location # Location on the board
        self.stack_size = stack_size # Stack size at the location
        self.visited_nodes = visited_nodes # List of the coordinated the node has been to
        self.actions = actions # Tracks all the actions aka the solution of this path

        self.heuristic_cost = self.calculate_heuristic_cost()

        # Child Nodes
        self.move_up = None
        self.move_down = None
        self.move_left = None
        self.move_right = None


    def __cmp__(self, other):
        """
        Overwrite the comparison operators
        """
        return self.heuristic_cost.cmp(other.heuristic_cost)


    def print_path(self):
        """
        Print the solution path
        """
        while(self.actions):
            action = self.actions.pop(0)
            if (action[0] == "move"):
                print_move(action[1], action[2][0], action[2][1], action[3][0], action[3][1])
            else:
                print_boom(action[1][0], action[1][1])


    def stack(self, new_loc, pieces_to_move):
        """
        Returns a new board after stacking onto the next location
        """
        new_board = self.board.copy()
        new_stack = new_board.get_stack_size(new_loc) + pieces_to_move

        # Put the newly created stack down
        new_board.remove_piece(new_loc)
        new_board.place_piece(new_stack, new_loc)

        # Fix the old spot
        new_board.remove_piece(self.location)
        old_stack =  self.stack_size - pieces_to_move
        if old_stack > 0:
            new_board.place_piece(old_stack, self.location)

        return new_board


    def move(self, new_loc, pieces_to_move):
        """
        Returns a new board after moving pieces to an empty location
        """
        new_board = self.board.copy()

        # Put the newly created stack down
        new_board.place_piece(pieces_to_move, new_loc)

        # Fix the old spot
        new_board.remove_piece(self.location)
        old_stack =  new_board.get_stack_size(self.location) - pieces_to_move
        if old_stack > 0:
            new_board.place_piece(old_stack, self.location)

        return new_board


    def try_move(self, new_loc, pieces_to_move):
        """
        Shared functionality between the try_move directional functions
        """
        # If it is occupied by white, stack it
        new_board = self.board.copy()
        if new_board.is_occupied_by_white(new_loc):
            new_board = self.stack(new_loc, pieces_to_move)
        # Else if there is no stacking involved
        else:
            new_board = self.move(new_loc, pieces_to_move)

        return new_board


    def try_move_up(self, move_distance, pieces_to_move):
        """
        Attempt to move up from the current location. If successful, return a
        new node with the updated state and data.
        """
        old_loc  = self.location
        new_loc = (self.location[0], self.location[1]+move_distance)

        # Make sure it is a valid tile to move to
        if new_loc[1] > BOARD_SIZE_MAX or self.board.is_occupied_by_black(new_loc):
            return False

        new_stack = self.board.get_stack_size(new_loc) + pieces_to_move
        new_board = self.try_move(new_loc, pieces_to_move)

        # Return the Node to represent this move
        updated_visited_nodes = deepcopy(self.visited_nodes)
        updated_visited_nodes.append(new_loc)
        updated_actions = deepcopy(self.actions)
        updated_actions.append(("move", pieces_to_move, old_loc, new_loc))
        return MyNode(board=new_board,
                      location=new_loc,
                      stack_size=new_stack,
                      visited_nodes=updated_visited_nodes,
                      actions=updated_actions)


    def try_move_down(self, move_distance, pieces_to_move):
        """
        Attempt to move down from the current location. If successful, return a
        new node with the updated state and data.
        """
        old_loc  = self.location
        new_loc = (self.location[0], self.location[1]-move_distance)

        # Make sure it is a valid tile to move to
        if new_loc[1] < BOARD_SIZE_MIN or self.board.is_occupied_by_black(new_loc):
            return False

        new_stack = self.board.get_stack_size(new_loc) + pieces_to_move
        new_board = self.try_move(new_loc, pieces_to_move)

        # Return the Node to represent this move
        updated_visited_nodes = deepcopy(self.visited_nodes)
        updated_visited_nodes.append(new_loc)
        updated_actions =  deepcopy(self.actions)
        updated_actions.append(("move", pieces_to_move, old_loc, new_loc))
        return MyNode(board=new_board,
                      location=new_loc,
                      stack_size=new_stack,
                      visited_nodes=updated_visited_nodes,
                      actions=updated_actions)


    def try_move_left(self, move_distance, pieces_to_move):
        """
        Attempt to move left from the current location. If successful, return a
        new node with the updated state and data.
        """
        old_loc  = self.location
        new_loc = (self.location[0]-move_distance, self.location[1])

        # Make sure it is a valid tile to move to
        if new_loc[0] < BOARD_SIZE_MIN or self.board.is_occupied_by_black(new_loc):
            return False

        new_stack = self.board.get_stack_size(new_loc) + pieces_to_move
        new_board = self.try_move(new_loc, pieces_to_move)

        # Updated passed information and return the new Node above
        updated_visited_nodes = deepcopy(self.visited_nodes)
        updated_visited_nodes.append(new_loc)
        updated_actions = deepcopy(self.actions)
        updated_actions.append(("move", pieces_to_move, old_loc, new_loc))
        return MyNode(board=new_board,
                      location=new_loc,
                      stack_size=new_stack,
                      visited_nodes=updated_visited_nodes,
                      actions=updated_actions)


    def try_move_right(self, move_distance, pieces_to_move):
        """
        Attempt to move right from the current location. If successful, return a
        new node with the updated state and data.
        """
        old_loc  = self.location
        new_loc = (self.location[0]+move_distance, self.location[1])

        # Make sure it is a valid tile to move to
        if new_loc[0] > BOARD_SIZE_MAX or self.board.is_occupied_by_black(new_loc):
            return False

        new_stack = self.board.get_stack_size(new_loc) + pieces_to_move
        new_board = self.try_move(new_loc, pieces_to_move)

        # Return the Node to represent this move
        updated_visited_nodes = deepcopy(self.visited_nodes)
        updated_visited_nodes.append(new_loc)
        updated_actions = deepcopy(self.actions)
        updated_actions.append(("move", pieces_to_move, old_loc, new_loc))
        return MyNode(board=new_board,
                      location=new_loc,
                      stack_size=new_stack,
                      visited_nodes=updated_visited_nodes,
                      actions=updated_actions)


    def calculate_heuristic_cost(self):
        """
        Heuristic formula for a node
        """
        return 0


    def h_search(self):
        """
        Search algorithm using a ehuristic to organize the priority queue of nodes
        representing the different paths to take
        """
        # Create the queue of nodes and add the first node to it
        queue = MyPriorityQueue()
        queue.push(self)

        # While there are still paths to explore
        while not queue.isEmpty():
            current_node = queue.pop()

            # current_node.board.print()

            # Check if we are in a position to explode
            for black in current_node.board.get_blacks():
                if are_neighbors((black[1], black[2]), current_node.location):
                    # Try the explosion and add to the queue
                    temp_board = current_node.board.copy()
                    temp_actions = deepcopy(current_node.actions)
                    MyUtil.explode(temp_board, current_node.location, temp_actions)

                    # Check if we have won from the explosion
                    if MyUtil.did_win(temp_board):
                        current_node.actions = temp_actions
                        current_node.print_path()
                        return True

                    # If we did not lose from this scenario, add to the queue
                    if not MyUtil.did_lose(temp_board):
                        next_white = temp_board.get_whites()[0]
                        queue.append(MyNode(board=temp_board, location=(next_white[1], next_white[2]),
                                          stack_size=next_white[0], visited_nodes=current_node.visited_nodes,
                                          actions=temp_actions))
                    # We are not backing out yet, we try each directional path too

            # Explore each directional path
            # Try each possible move with the stack size
            for move_distance in range(1, current_node.stack_size+1):
                for pieces_to_move in range(1, current_node.stack_size+1):
                    # print("Trying to move {} pieces {} tiles".format(pieces_to_move, move_distance))

                    # Try each direction, only adding to the queue if that location has not been visited yet:
                    if current_node.try_move_up(move_distance, pieces_to_move):
                        if (current_node.location[0], current_node.location[1]+move_distance) not in current_node.visited_nodes:
                            queue.append(current_node.try_move_up(move_distance, pieces_to_move))
                    if current_node.try_move_down(move_distance, pieces_to_move):
                        if (current_node.location[0], current_node.location[1]-move_distance) not in current_node.visited_nodes:
                            queue.append(current_node.try_move_down(move_distance, pieces_to_move))
                    if current_node.try_move_right(move_distance, pieces_to_move):
                        if (current_node.location[0]+move_distance, current_node.location[1]) not in current_node.visited_nodes:
                            queue.append(current_node.try_move_right(move_distance, pieces_to_move))
                    if current_node.try_move_left(move_distance, pieces_to_move):
                        if (current_node.location[0]-move_distance, current_node.location[1]) not in current_node.visited_nodes:
                            queue.append(current_node.try_move_left(move_distance, pieces_to_move))





#end file

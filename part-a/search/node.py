BOARD_SIZE_MIN = 0
BOARD_SIZE_MAX = 7

from search.util import *
from search.DescendingPriorityQueue import *
import copy

class Node():
    def __init__(self,state,stack_size,location,piece_number,parent,action=None,depth=None,path_cost=None,heuristic_cost=0):
        self.state = state
        self.piece_number = piece_number
        self.parent = parent # parent node
        self.action = action # move up, left, down, right
        self.depth = depth # depth of the node in the tree
        self.path_cost = path_cost # accumulated g(n), the cost to reach the current node

        new_state = self.state

        # Coordinate of the current piece
        self.location = location

        # Stack size of the tokens in the node
        self.stack_size = stack_size

        self.heuristic_cost = self.calculate_heuristic_cost()

        self.visited_nodes = set([self.location])

        # children node
        self.move_up = None
        self.move_left = None
        self.move_down = None
        self.move_right = None

        # Keep track of the actions this node takes (aka the white piece)
        self.actions = []


    def __lt__(self, other):
        """
        Overwrite < operator for heuristic value comparison
        """
        return self.heuristic_cost < other.heuristic_cost
    def __gt__(self, other):
        """
        Overwrite > operator for heuristic value comparison
        """
        return self.heuristic_cost > other.heuristic_cost


    # check if chosen white piece move lands on black piece
    def lands_on_black_check(self, new_x, new_y):
        for i in self.state["black"]:
            if new_x == i[1] and new_y == i[2]:
                return True


    # check if chosen white piece move lands on white piece
    def lands_on_white(self, new_x, new_y, pieces_to_move):
        return False

        for i in self.state["white"]:
            if new_x == i[1] and new_y == i[2]:
                i[0]+= pieces_to_move # add moved pieces to newly formed white stack
                if pieces_to_move == self.state["white"][self.piece_number][0]: # if moving all pieces delete the original white piece
                    del new_state["white"][self.piece_number]
                else: # else decrease the number of pieces in the original stack
                    self.state["white"][self.piece_number][0] -= pieces_to_move
                return True


    def try_move_up(self, move_distance, pieces_to_move, new_stack_size):
        old_x = self.state["white"][self.piece_number][1]
        old_y = self.state["white"][self.piece_number][2]
        new_x = self.state["white"][self.piece_number][1] # x stays the same
        new_y = self.state["white"][self.piece_number][2] + move_distance # y moves up by n
        new_state = copy.deepcopy(self.state)

        # check if move by n is valid
        if new_y > BOARD_SIZE_MAX:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white(new_x, new_y, pieces_to_move):
            remove_piece(new_state, (old_x, old_y))
            self.location = (new_x, new_y)
            return new_state
        else:
            if pieces_to_move == self.stack_size: #self.state["white"][self.piece_number][0]: # if moving all pieces in stack just change the y variable
                new_state["white"][self.piece_number][2] = new_y
                remove_piece(new_state, (old_x, old_y))
                self.location = (new_x, new_y)
            else: # else decrease number of pieces in original stack and add new piece location to white list
                new_state["white"][self.piece_number][0] -= pieces_to_move
                place_piece(new_state, new_stack_size, (new_x, new_y))

            self.stack_size = pieces_to_move
            return new_state

    def try_move_down(self, move_distance, pieces_to_move, new_stack_size):
        old_x = self.state["white"][self.piece_number][1]
        old_y = self.state["white"][self.piece_number][2]
        new_x = self.state["white"][self.piece_number][1] # x stays the same
        new_y = self.state["white"][self.piece_number][2] - move_distance # y moves down by n
        new_state = copy.deepcopy(self.state)

        # check if move by n is valid
        if new_y < BOARD_SIZE_MIN:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white(new_x, new_y, pieces_to_move):
            remove_piece(new_state, (old_x, old_y))
            self.location = (new_x, new_y)
            return new_state
        else:
            if pieces_to_move == self.stack_size: #self.state["white"][self.piece_number][0]:
                new_state["white"][self.piece_number][2] = new_y
                remove_piece(new_state, (old_x, old_y))
                self.location = (new_x, new_y)
            else:
                new_state["white"][self.piece_number][0] -= pieces_to_move
                place_piece(new_state, new_stack_size, (new_x, new_y))

            self.stack_size = pieces_to_move
            return new_state

    def try_move_right(self, move_distance, pieces_to_move, new_stack_size):
        old_stack_size = self.stack_size

        old_x = self.state["white"][self.piece_number][1]
        old_y = self.state["white"][self.piece_number][2]
        new_x = self.state["white"][self.piece_number][1] + move_distance # x moves right by n
        new_y = self.state["white"][self.piece_number][2] # y stays the same
        new_state = copy.deepcopy(self.state)

        # check if move by n is valid
        if new_x > BOARD_SIZE_MAX:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white(new_x, new_y, pieces_to_move):
            remove_piece(new_state, (old_x, old_y))
            self.location = (new_x, new_y)
            return new_state
        else:
            if pieces_to_move == self.stack_size: #self.state["white"][self.piece_number][0]:
                new_state["white"][self.piece_number][1] = new_x
                remove_piece(new_state, (old_x, old_y))
                self.location = (new_x, new_y)
            else:
                new_state["white"][self.piece_number][0] -= pieces_to_move
                place_piece(new_state, new_stack_size, (new_x, new_y))

            self.stack_size = pieces_to_move
            return new_state


    def try_move_left(self, move_distance, pieces_to_move, new_stack_size):
        old_x = self.state["white"][self.piece_number][1]
        old_y = self.state["white"][self.piece_number][2]
        new_x = self.state["white"][self.piece_number][1] - move_distance # x moves left by n
        new_y = self.state["white"][self.piece_number][2] # y stays the same
        # new_state = self.state.copy()
        new_state = copy.deepcopy(self.state)

        # check if move by n is allowable
        if new_x < BOARD_SIZE_MIN:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white(new_x, new_y, pieces_to_move):
            remove_piece(new_state, (old_x, old_y))
            self.location = (new_x, new_y)
            return new_state
        else:
            if pieces_to_move == self.stack_size: #self.state["white"][self.piece_number][0]:
                new_state["white"][self.piece_number][1] = new_x
                remove_piece(new_state, (old_x, old_y))
                self.location = (new_x, new_y)
            else:
                new_state["white"][self.piece_number][0] -= pieces_to_move
                place_piece(new_state, new_stack_size, (new_x, new_y))

            self.stack_size = pieces_to_move
            return new_state


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


    def search(self):
        """
        implemeting FIFO queue without heuristic for now just a simple version to make it work
        """

        queue = [self] # queue of found unvisited nodes

        depth_queue = [0] # node depth
        path_cost_queue = [0] # path cost
        visited_nodes = set([]) # set of visited white pieces

        while queue:
            current_node = queue.pop(0) # select and remove the first white piece
            current_depth = depth_queue.pop(0) # select and remove the depth for current node
            current_path_cost = path_cost_queue.pop(0) # select and remove the path cost for reaching current node
            old_location = copy.deepcopy(current_node.location)
            visited_nodes.add(self.location)

            # Check if our current location neighbors any of the black pieces
            for black in current_node.state["black"]:
                if (are_neighbors((black[1], black[2]), current_node.location)):

                    # Copy the current state and try the explosion. If it the explosion causes
                    # a win or it doesn't cause a loss, we execute it and use the next white node from
                    # the queue.
                    temp_state = copy.deepcopy(current_node.state)
                    temp_actions = copy.deepcopy(current_node.actions)
                    explode(temp_state, current_node.location, temp_actions)

                    # check if we win after the explosion, if not move on to the next white
                    # piece. if there are no more then we lost and can return False
                    if (did_win(temp_state)):
                        current_node.actions = temp_actions
                        current_node.print_path()
                        return True

                    # if the explosion causes us to lose, dont reset the state and current node
                    if (not did_lose(temp_state)):
                        # Append the state with the explosion and moving to the queue as the next white node
                        tup = temp_state["white"][0]
                        next = Node(state=temp_state, stack_size=tup[0], location=(tup[1], tup[2]),piece_number=0,parent=None,action=None,depth=0,path_cost=0,heuristic_cost=0)
                        next.actions = temp_actions
                        queue.append(next)
                        # Continue with the current node as if we didnt perform the explosion

            # find path when goal is found
            if (not current_node.state["black"]):
                current_node.print_path()
                return True

            else:
                # print("Searching...")
                # Try every combination of stack sizes and distances to move
                for move_distance in range(1, self.stack_size+1):
                    for pieces_to_move in range(1, self.stack_size+1):
                        new_stack_size = self.stack_size - pieces_to_move

                        # try moving down
                        if current_node.try_move_down(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            new_state = current_node.try_move_down(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)

                            # check if the down node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # create new child node
                                current_node.move_down = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='down',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                                current_node.move_down.actions = copy.deepcopy(current_node.actions)
                                current_node.move_down.actions.append(("move", pieces_to_move, old_location, current_node.location))
                                queue.append(current_node.move_down)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)

                        # try moving right
                        if current_node.try_move_right(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            new_state = current_node.try_move_right(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)
                            # check if the right node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # create new child node
                                current_node.move_right = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='right',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                                current_node.move_right.actions = copy.deepcopy(current_node.actions)
                                current_node.move_right.actions.append(("move", pieces_to_move, old_location, current_node.location))
                                queue.append(current_node.move_right)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)

                        # try moving up
                        if current_node.try_move_up(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            new_state = current_node.try_move_up(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)
                            # check if the up node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # create new child node
                                current_node.move_up = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='up',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                                current_node.move_up.actions = copy.deepcopy(current_node.actions)
                                current_node.move_up.actions.append(("move", pieces_to_move, old_location, current_node.location))
                                queue.append(current_node.move_up)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)

                        # try moving left
                        if current_node.try_move_left(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            new_state = current_node.try_move_left(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)
                            # check if the left node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # create new child node
                                current_node.move_left = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='left',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                                current_node.move_left.actions = copy.deepcopy(current_node.actions)
                                current_node.move_left.actions.append(("move", pieces_to_move, old_location, current_node.location))
                                queue.append(current_node.move_left)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)


    def calculate_heuristic_cost(self):
        """
        Returns the value of the self nodeself.
        Factors:
            - Number of black tiles self can explode
        """
        return count_eliminated_tiles(self.location, self.state)



    def h_search(self):
        """
        implemeting FIFO queue without heuristic for now just a simple version to make it work
        """

        queue = [self] # queue of found unvisited nodes

        depth_queue = [0] # node depth
        path_cost_queue = [0] # path cost
        visited_nodes = set([]) # set of visited white pieces

        while queue:
            queue.sort(reverse=True)
            current_node = queue.pop(0) # select and remove the first white piece
            current_depth = depth_queue.pop(0) # select and remove the depth for current node
            current_path_cost = path_cost_queue.pop(0) # select and remove the path cost for reaching current node
            old_location = copy.deepcopy(current_node.location)
            visited_nodes.add(self.location)

            # Check if our current location neighbors any of the black pieces
            for black in current_node.state["black"]:
                if (are_neighbors((black[1], black[2]), current_node.location)):

                    # Copy the current state and try the explosion. If it the explosion causes
                    # a win or it doesn't cause a loss, we execute it and use the next white node from
                    # the queue.
                    temp_state = copy.deepcopy(current_node.state)
                    temp_actions = copy.deepcopy(current_node.actions)
                    explode(temp_state, current_node.location, temp_actions)

                    # check if we win after the explosion, if not move on to the next white
                    # piece. if there are no more then we lost and can return False
                    if (did_win(temp_state)):
                        current_node.actions = temp_actions
                        current_node.print_path()
                        return True

                    # if the explosion causes us to lose, dont reset the state and current node
                    if (not did_lose(temp_state)):
                        # Append the state with the explosion and moving to the queue as the next white node
                        tup = temp_state["white"][0]
                        next = Node(state=temp_state, stack_size=tup[0], location=(tup[1], tup[2]),piece_number=0,parent=None,action=None,depth=0,path_cost=0,heuristic_cost=0)
                        next.actions = temp_actions
                        queue.append(next)
                        # Continue with the current node as if we didnt perform the explosion

            # find path when goal is found
            if (not current_node.state["black"]):
                current_node.print_path()
                return True

            else:
                # print("Searching...")
                # Try every combination of stack sizes and distances to move
                for move_distance in range(1, self.stack_size+1):
                    for pieces_to_move in range(1, self.stack_size+1):
                        new_stack_size = self.stack_size - pieces_to_move

                        # try moving down
                        if current_node.try_move_down(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            new_state = current_node.try_move_down(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)

                            # check if the down node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # create new child node
                                current_node.move_down = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='down',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                                current_node.move_down.actions = copy.deepcopy(current_node.actions)
                                current_node.move_down.actions.append(("move", pieces_to_move, old_location, current_node.location))
                                queue.append(current_node.move_down)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)

                        # try moving right
                        if current_node.try_move_right(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            new_state = current_node.try_move_right(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)
                            # check if the right node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # create new child node
                                current_node.move_right = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='right',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                                current_node.move_right.actions = copy.deepcopy(current_node.actions)
                                current_node.move_right.actions.append(("move", pieces_to_move, old_location, current_node.location))
                                queue.append(current_node.move_right)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)

                        # try moving up
                        if current_node.try_move_up(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            new_state = current_node.try_move_up(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)
                            # check if the up node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # create new child node
                                current_node.move_up = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='up',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                                current_node.move_up.actions = copy.deepcopy(current_node.actions)
                                current_node.move_up.actions.append(("move", pieces_to_move, old_location, current_node.location))
                                queue.append(current_node.move_up)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)

                        # try moving left
                        if current_node.try_move_left(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            new_state = current_node.try_move_left(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)
                            # check if the left node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # create new child node
                                current_node.move_left = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='left',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                                current_node.move_left.actions = copy.deepcopy(current_node.actions)
                                current_node.move_left.actions.append(("move", pieces_to_move, old_location, current_node.location))
                                queue.append(current_node.move_left)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)







    # def h_search(self):
    #
    #     queue = [(self,0)] # queue(found unvisited nodes, heuristic cost)
    #     depth_queue = [(0,0)] # queue(depth, heuristic cost)
    #     path_cost_queue = [(0,0)] # queue(path_cost, heuristic cost)
    #     visited_nodes = set([]) # set of visited white pieces
    #
    #     while queue:
    #         print(queue)
    #         # sort queues based on heuristic cost
    #         queue = sorted(queue, key=lambda x: x[1])
    #         depth_queue = sorted(depth_queue, key=lambda x: x[1])
    #         path_cost_queue = sorted(path_cost_queue, key=lambda x: x[1])
    #
    #         current_node = queue.pop(0)[0] # select and remove the first white piece
    #         current_depth = depth_queue.pop(0)[0] # select and remove the depth for current node
    #         current_path_cost = path_cost_queue.pop(0)[0] # select and remove the path cost for reaching current node
    #
    #         for white_pieces in current_node.state["white"]:
    #             visited_nodes.add(tuple(white_pieces)) # added as a tupple to be able to put list in set
    #         print("visited nodes:", visited_nodes)
    #
    #         # Check if our current location neighbors any of the black pieces
    #         for black in current_node.state["black"]:
    #             if (are_neighbors((black[1], black[2]), current_node.location)):
    #
    #                 # Copy the current state and try the explosion. If it the explosion causes
    #                 # a win or it doesn't cause a loss, we execute it and use the next white node from
    #                 # the queue.
    #                 temp_state = copy.deepcopy(current_node.state)
    #
    #                 explode(temp_state, current_node.location)
    #
    #
    #                 # check if we win after the explosion, if not move on to the next white
    #                 # piece. if there are no more then we lost and can return False
    #                 if (did_win(temp_state)): return True
    #
    #                 # if the explosion causes us to lose, dont reset the state and current node
    #                 if (not did_lose(temp_state)):
    #                     current_node = queue.pop(0)
    #                     current_node.state = temp_state
    #                 # return True
    #
    #         # find path when goal is found
    #         if (not current_node.state["black"]):
    #             #print path***************
    #             return True
    #
    #         else:
    #             # try moving down
    #             if current_node.try_move_down(1,self.piece_number):
    #                 new_state = current_node.try_move_down(1,self.piece_number)
    #                 # check if the down node is visited
    #                 if tuple(new_state["white"][-1]) not in visited_nodes:
    #                     h_cost = self.heuristic_function()
    #                     # create new child node
    #                     current_node.move_down = Node(state=new_state,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
    #                                             action='down',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=h_cost)
    #
    #                     queue.append((current_node.move_down,h_cost))
    #                     depth_queue.append((current_depth+1,h_cost))
    #                     path_cost_queue.append((current_path_cost,h_cost))
    #
    #             # try moving right
    #             if current_node.try_move_right(1,self.piece_number):
    #                 new_state = current_node.try_move_right(1,self.piece_number)
    #                 # check if the right node is visited
    #                 if tuple(new_state["white"][-1]) not in visited_nodes:
    #                     h_cost = self.heuristic_function()
    #                     # create new child node
    #                     current_node.move_right = Node(state=new_state,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
    #                                             action='right',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=h_cost)
    #                     queue.append((current_node.move_down,h_cost))
    #                     depth_queue.append((current_depth+1,h_cost))
    #                     path_cost_queue.append((current_path_cost,h_cost))
    #
    #             # try moving up
    #             if current_node.try_move_up(1,self.piece_number):
    #                 new_state = current_node.try_move_up(1,self.piece_number)
    #                 # check if the up node is visited
    #                 if tuple(new_state["white"][-1]) not in visited_nodes:
    #                     h_cost = self.heuristic_function()
    #                     # create new child node
    #                     current_node.move_up = Node(state=new_state,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
    #                                             action='up',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=h_cost)
    #                     queue.append((current_node.move_down,h_cost))
    #                     depth_queue.append((current_depth+1,h_cost))
    #                     path_cost_queue.append((current_path_cost,h_cost))
    #
    #             # try moving left
    #             if current_node.try_move_left(1,self.piece_number):
    #                 new_state = current_node.try_move_left(1,self.piece_number)
    #                 # check if the left node is visited
    #                 if tuple(new_state["white"][-1]) not in visited_nodes:
    #                     h_cost = self.heuristic_function
    #                     # create new child node
    #                     current_node.move_left = Node(state=new_state,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
    #                                             action='left',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=h_cost)
    #                     queue.append((current_node.move_down,h_cost))
    #                     depth_queue.append((current_depth+1,h_cost))
    #                     path_cost_queue.append((current_path_cost,h_cost))
    #
    #             # just printing to test what's happening
    #             print_board(new_state)

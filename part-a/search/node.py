BOARD_SIZE_MIN = 0
BOARD_SIZE_MAX = 7

from search.util import *
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

        # children node
        self.move_up = None
        self.move_left = None
        self.move_down = None
        self.move_right = None

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
        # new_state = self.state.copy()
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

                # remove the old piece and place an updated version there
                # remove_piece(new_state, (old_x, old_y))
                place_piece(new_state, new_stack_size, (new_x, new_y))
                # new_state["white"].append([new_stack_size,old_x,old_y])
                # print_board(new_state)
            # remove_piece(new_state, (old_x, old_y))
            self.stack_size = pieces_to_move
            # self.location = (new_x, new_y)
            return new_state

    def try_move_down(self, move_distance, pieces_to_move, new_stack_size):
        old_x = self.state["white"][self.piece_number][1]
        old_y = self.state["white"][self.piece_number][2]
        new_x = self.state["white"][self.piece_number][1] # x stays the same
        new_y = self.state["white"][self.piece_number][2] - move_distance # y moves down by n
        # new_state = self.state.copy()
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

                # remove the old piece and place an updated version there
                # remove_piece(new_state, (old_x, old_y))
                place_piece(new_state, new_stack_size, (new_x, new_y))
                # new_state["white"].append([new_stack_size,old_x,old_y])
                # print_board(new_state)
            # remove_piece(new_state, (old_x, old_y))
            self.stack_size = pieces_to_move
            # self.location = (new_x, new_y)
            return new_state

    def try_move_right(self, move_distance, pieces_to_move, new_stack_size):
        # print_board(self.state)
        old_stack_size = self.stack_size

        old_x = self.state["white"][self.piece_number][1]
        old_y = self.state["white"][self.piece_number][2]
        new_x = self.state["white"][self.piece_number][1] + move_distance # x moves right by n
        new_y = self.state["white"][self.piece_number][2] # y stays the same
        # new_state = self.state.copy()
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
            # print("here")
            if pieces_to_move == self.stack_size: #self.state["white"][self.piece_number][0]:
                new_state["white"][self.piece_number][1] = new_x
                remove_piece(new_state, (old_x, old_y))
                self.location = (new_x, new_y)
            else:
                # print("UNSTACK")
                new_state["white"][self.piece_number][0] -= pieces_to_move

                # remove the old piece and place an updated version there
                # remove_piece(new_state, (old_x, old_y))
                place_piece(new_state, new_stack_size, (new_x, new_y))
                # new_state["white"].append([new_stack_size,old_x,old_y])
                # print_board(new_state)
            # remove_piece(new_state, (old_x, old_y))
            self.stack_size = pieces_to_move
            # self.location = (new_x, new_y)
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

                # remove the old piece and place an updated version there
                # remove_piece(new_state, (old_x, old_y))
                place_piece(new_state, new_stack_size, (new_x, new_y))
                # new_state["white"].append([self.stack_size-pieces_to_move,old_x,old_y])
            # remove_piece(new_state, (old_x, old_y))
            self.stack_size = pieces_to_move
            # self.location = (new_x, new_y)
            return new_state



    def search(self):
        #implemeting FIFO queue without heuristic for now just a simple version to make it work
        #currently assumes only 1 white piece in the game

        queue = [self] # queue of found unvisited nodes

        depth_queue = [0] # node depth
        path_cost_queue = [0] # path cost
        visited_nodes = set([]) # set of visited white pieces

        while queue:
            current_node = queue.pop(0) # select and remove the first white piece
            current_depth = depth_queue.pop(0) # select and remove the depth for current node
            current_path_cost = path_cost_queue.pop(0) # select and remove the path cost for reaching current node

            # for white_pieces in current_node.state["white"]:
            #     visited_nodes.add(tuple(white_pieces)) # added as a tupple to be able to put list in set
            visited_nodes.add(self.location)
            # print("visited nodes:", visited_nodes)
            print_board(current_node.state)

            # Check if our current location neighbors any of the black pieces
            for black in current_node.state["black"]:
                if (are_neighbors((black[1], black[2]), current_node.location)):

                    # Copy the current state and try the explosion. If it the explosion causes
                    # a win or it doesn't cause a loss, we execute it and use the next white node from
                    # the queue.
                    temp_state = copy.deepcopy(current_node.state)
                    # print_board(temp_state)
                    explode(temp_state, current_node.location)
                    # print_board(temp_state)

                    # check if we win after the explosion, if not move on to the next white
                    # piece. if there are no more then we lost and can return False
                    if (did_win(temp_state)): return True

                    # if the explosion causes us to lose, dont reset the state and current node
                    if (not did_lose(temp_state)):
                        print(temp_state)
                        current_node = queue.pop(0)
                        current_node.state = temp_state
                    # return True

            # find path when goal is found
            if (not current_node.state["black"]):
                #print path***************
                return True

            else:
                # print("Searching...")
                # Try every combination of stack sizes and distances to move
                old_location = current_node.location
                for move_distance in range(1, self.stack_size+1):
                    for pieces_to_move in range(1, self.stack_size+1):
                        new_stack_size = self.stack_size - pieces_to_move
                        # print("Try moving {} piece {} spots".format(pieces_to_move, move_distance))
                # new_stack_size = 1
                # move_distance = 1
                # pieces_to_move = 1

                        # try moving down
                        if current_node.try_move_down(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            # print("down")
                            new_state = current_node.try_move_down(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)
                            # print_board(new_state)
                            # print(new_state, " : ", visited_nodes)
                            # check if the down node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # print("moving down")
                                # create new child node
                                current_node.move_down = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='down',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)

                                queue.append(current_node.move_down)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)

                                print_move(pieces_to_move, old_location[0], old_location[1], current_node.location[0], current_node.location[1])
                                print_board(new_state)
                            # else:
                            #     print("already visited, dead end")

                        # try moving right
                        if current_node.try_move_right(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            # print("right")
                            new_state = current_node.try_move_right(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)
                            # check if the right node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # create new child node
                                current_node.move_right = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='right',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                                queue.append(current_node.move_right)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)#######

                                print_move(pieces_to_move, old_location[0], old_location[1], current_node.location[0], current_node.location[1])
                                print_board(new_state)
                            # else:
                            #     print("already visited, dead end")

                        # try moving up
                        if current_node.try_move_up(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            # print("up")
                            new_state = current_node.try_move_up(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)
                            # check if the up node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # create new child node
                                current_node.move_up = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='up',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                                queue.append(current_node.move_up)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)

                                print_move(pieces_to_move, old_location[0], old_location[1], current_node.location[0], current_node.location[1])
                                print_board(new_state)
                            # else:
                            #     print("already visited, dead end")

                        # try moving left
                        if current_node.try_move_left(move_distance, pieces_to_move, current_node.stack_size-new_stack_size):
                            # print("left")
                            new_state = current_node.try_move_left(move_distance, pieces_to_move, current_node.stack_size-new_stack_size)
                            # check if the left node is visited
                            if tuple(new_state["white"][-1]) not in visited_nodes:
                                # create new child node
                                current_node.move_left = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                        action='left',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                                queue.append(current_node.move_left)
                                depth_queue.append(current_depth+1)
                                path_cost_queue.append(current_path_cost)

                                print_move(pieces_to_move, old_location[0], old_location[1], current_node.location[0], current_node.location[1])
                                print_board(new_state)
                            # else:
                            #     print("already visited, dead end")

                        # just printing to test what's happening
                        # print("queue of nodes", queue)
                        # for i in queue:
                        #     print("queue",i.state["white"])
                        # print("depth_queue",depth_queue)
                        # print_board(new_state)

    def heuristic_function(self):
        # checks the number of black pieces in 3x3 radius of node
        black_pieces_near_node = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                loc = (self.location[0]+i, self.location[1]+j)
                if (is_occupied_by_black(loc, self.state)):
                    black_pieces.append(loc)
        return len(black_pieces_near_node)

    def h_search(self):

        queue = [(self,0)] # queue(found unvisited nodes, heuristic cost)
        depth_queue = [(0,0)] # queue(depth, heuristic cost)
        path_cost_queue = [(0,0)] # queue(path_cost, heuristic cost)
        visited_nodes = set([]) # set of visited white pieces

        while queue:
            print(queue)
            # sort queues based on heuristic cost
            queue = sorted(queue, key=lambda x: x[1])
            depth_queue = sorted(depth_queue, key=lambda x: x[1])
            path_cost_queue = sorted(path_cost_queue, key=lambda x: x[1])

            current_node = queue.pop(0)[0] # select and remove the first white piece
            current_depth = depth_queue.pop(0)[0] # select and remove the depth for current node
            current_path_cost = path_cost_queue.pop(0)[0] # select and remove the path cost for reaching current node

            for white_pieces in current_node.state["white"]:
                visited_nodes.add(tuple(white_pieces)) # added as a tupple to be able to put list in set
            print("visited nodes:", visited_nodes)

            # Check if our current location neighbors any of the black pieces
            for black in current_node.state["black"]:
                if (are_neighbors((black[1], black[2]), current_node.location)):

                    # Copy the current state and try the explosion. If it the explosion causes
                    # a win or it doesn't cause a loss, we execute it and use the next white node from
                    # the queue.
                    temp_state = copy.deepcopy(current_node.state)

                    explode(temp_state, current_node.location)


                    # check if we win after the explosion, if not move on to the next white
                    # piece. if there are no more then we lost and can return False
                    if (did_win(temp_state)): return True

                    # if the explosion causes us to lose, dont reset the state and current node
                    if (not did_lose(temp_state)):
                        current_node = queue.pop(0)
                        current_node.state = temp_state
                    # return True

            # find path when goal is found
            if (not current_node.state["black"]):
                #print path***************
                return True

            else:
                # try moving down
                if current_node.try_move_down(1,self.piece_number):
                    new_state = current_node.try_move_down(1,self.piece_number)
                    # check if the down node is visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        h_cost = self.heuristic_function()
                        # create new child node
                        current_node.move_down = Node(state=new_state,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                action='down',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=h_cost)

                        queue.append((current_node.move_down,h_cost))
                        depth_queue.append((current_depth+1,h_cost))
                        path_cost_queue.append((current_path_cost,h_cost))

                # try moving right
                if current_node.try_move_right(1,self.piece_number):
                    new_state = current_node.try_move_right(1,self.piece_number)
                    # check if the right node is visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        h_cost = self.heuristic_function()
                        # create new child node
                        current_node.move_right = Node(state=new_state,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                action='right',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=h_cost)
                        queue.append((current_node.move_down,h_cost))
                        depth_queue.append((current_depth+1,h_cost))
                        path_cost_queue.append((current_path_cost,h_cost))

                # try moving up
                if current_node.try_move_up(1,self.piece_number):
                    new_state = current_node.try_move_up(1,self.piece_number)
                    # check if the up node is visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        h_cost = self.heuristic_function()
                        # create new child node
                        current_node.move_up = Node(state=new_state,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                action='up',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=h_cost)
                        queue.append((current_node.move_down,h_cost))
                        depth_queue.append((current_depth+1,h_cost))
                        path_cost_queue.append((current_path_cost,h_cost))

                # try moving left
                if current_node.try_move_left(1,self.piece_number):
                    new_state = current_node.try_move_left(1,self.piece_number)
                    # check if the left node is visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        h_cost = self.heuristic_function
                        # create new child node
                        current_node.move_left = Node(state=new_state,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                action='left',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=h_cost)
                        queue.append((current_node.move_down,h_cost))
                        depth_queue.append((current_depth+1,h_cost))
                        path_cost_queue.append((current_path_cost,h_cost))

                # just printing to test what's happening
                print_board(new_state)

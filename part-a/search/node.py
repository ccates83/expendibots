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
        for i in self.state["white"]:
            if new_x == i[1] and new_y == i[2]:
                i[0]+= pieces_to_move # add moved pieces to newly formed white stack
                if pieces_to_move == self.state["white"][self.piece_number][0]: # if moving all pieces delete the original white piece
                    del new_state["white"][self.piece_number]
                else: # else decrease the number of pieces in the original stack
                    self.state["white"][self.piece_number][0] -= pieces_to_move
                return True


    def try_move_up(self, move_distance, pieces_to_move):
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
            if pieces_to_move == self.state["white"][self.piece_number][0]: # if moving all pieces in stack just change the y variable
                new_state["white"][self.piece_number][2] = new_y
            else: # else decrease number of pieces in original stack and add new piece location to white list
                new_state["white"][self.piece_number][0] -= pieces_to_move
                new_state["white"].append([pieces_to_move,new_x,new_y])
            remove_piece(new_state, (old_x, old_y))
            self.location = (new_x, new_y)
            return new_state

    def try_move_down(self, move_distance, pieces_to_move):
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
            if pieces_to_move == self.state["white"][self.piece_number][0]:
                new_state["white"][self.piece_number][2] = new_y
            else:
                new_state["white"][self.piece_number][0] -= pieces_to_move
                new_state["white"].append([pieces_to_move,new_x,new_y])
            remove_piece(new_state, (old_x, old_y))
            self.location = (new_x, new_y)
            return new_state

    def try_move_right(self, move_distance, pieces_to_move):
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
            if pieces_to_move == self.state["white"][self.piece_number][0]:
                new_state["white"][self.piece_number][1] = new_x
            else:
                new_state["white"][self.piece_number][0] -= pieces_to_move
                new_state["white"].append([pieces_to_move,new_x,new_y])
            remove_piece(new_state, (old_x, old_y))
            self.location = (new_x, new_y)
            return new_state


    def try_move_left(self, move_distance, pieces_to_move):
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
            if pieces_to_move == self.state["white"][self.piece_number][0]:
                new_state["white"][self.piece_number][1] = new_x
            else:
                new_state["white"][self.piece_number][0] -= pieces_to_move
                new_state["white"].append([pieces_to_move,new_x,new_y])
            remove_piece(new_state, (old_x, old_y))
            self.location = (new_x, new_y)
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
            print("visited nodes:", visited_nodes)
            print_board(current_node.state)

            # Check if our current location neighbors any of the black pieces
            for black in current_node.state["black"]:
                if (are_neighbors((black[1], black[2]), current_node.location)):

                    # Copy the current state and try the explosion. If it the explosion causes
                    # a win or it doesn't cause a loss, we execute it and use the next white node from
                    # the queue.
                    temp_state = copy.deepcopy(current_node.state)
                    print_board(temp_state)
                    explode(temp_state, current_node.location)
                    print_board(temp_state)

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
                print("Searching...")
                # Try every combination of stack sizes and distances to move
                # for move_distance in range(1, self.stack_size):
                #     for pieces_to_move in range(1, self.stack_size):
                #         new_stack_size = self.stack_size - pieces_to_move
                new_stack_size = 1
                move_distance = 1
                pieces_to_move = 1

                # try moving down
                if current_node.try_move_down(move_distance, pieces_to_move):
                    print("down")
                    new_state = current_node.try_move_down(move_distance, pieces_to_move)
                    print_board(new_state)
                    print(new_state, " : ", visited_nodes)
                    # check if the down node is visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        print("moving down")
                        # create new child node
                        current_node.move_down = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                action='down',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)

                        queue.append(current_node.move_down)
                        depth_queue.append(current_depth+1)
                        path_cost_queue.append(current_path_cost)
                    else:
                        print("already visited, dead end")

                # try moving right
                if current_node.try_move_right(move_distance, pieces_to_move):
                    print("right")
                    new_state = current_node.try_move_right(move_distance, pieces_to_move)
                    # check if the right node is visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        # create new child node
                        current_node.move_right = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                action='right',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                        queue.append(current_node.move_right)
                        depth_queue.append(current_depth+1)
                        path_cost_queue.append(current_path_cost)#######
                    else:
                        print("already visited, dead end")

                # try moving up
                if current_node.try_move_up(move_distance, pieces_to_move):
                    print("up")
                    new_state = current_node.try_move_up(move_distance, pieces_to_move)
                    # check if the up node is visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        # create new child node
                        current_node.move_up = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                action='up',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                        queue.append(current_node.move_up)
                        depth_queue.append(current_depth+1)
                        path_cost_queue.append(current_path_cost)
                    else:
                        print("already visited, dead end")

                # try moving left
                if current_node.try_move_left(move_distance, pieces_to_move):
                    print("left")
                    new_state = current_node.try_move_left(move_distance, pieces_to_move)
                    # check if the left node is visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        # create new child node
                        current_node.move_left = Node(state=new_state,stack_size=new_stack_size,location=current_node.location,piece_number=self.piece_number,parent=current_node,\
                                                action='left',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                        queue.append(current_node.move_left)
                        depth_queue.append(current_depth+1)
                        path_cost_queue.append(current_path_cost)
                    else:
                        print("already visited, dead end")

                # just printing to test what's happening
                print("queue of nodes", queue)
                for i in queue:
                    print("queue",i.state["white"])
                print("depth_queue",depth_queue)
                print_board(new_state)

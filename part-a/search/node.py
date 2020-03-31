BOARD_SIZE_MIN = 0
BOARD_SIZE_MAX = 7

from search.util import *

class Node():
    def __init__(self,state,piece_number,parent,action=None,depth=None,path_cost=None,heuristic_cost=0):
        self.state = state
        self.piece_number = piece_number
        self.parent = parent # parent node
        self.action = action # move up, left, down, right
        self.depth = depth # depth of the node in the tree
        self.path_cost = path_cost # accumulated g(n), the cost to reach the current node

        new_state = self.state

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
        new_x = self.state["white"][self.piece_number][1] # x stays the same
        new_y = self.state["white"][self.piece_number][2] + move_distance # y moves up by n
        new_state = self.state.copy()
        # check if move by n is valid
        if new_y > BOARD_SIZE_MAX:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white(new_x, new_y, pieces_to_move):
            return new_state
        else:
            if pieces_to_move == self.state["white"][self.piece_number][0]: # if moving all pieces in stack just change the y variable
                new_state["white"][self.piece_number][2] = new_y
            else: # else decrease number of pieces in original stack and add new piece location to white list
                new_state["white"][self.piece_number][0] -= pieces_to_move
                new_state["white"].append([pieces_to_move,new_x,new_y])
            return new_state

    def try_move_down(self, move_distance, pieces_to_move):
        new_x = self.state["white"][self.piece_number][1] # x stays the same
        new_y = self.state["white"][self.piece_number][2] - move_distance # y moves down by n
        new_state = self.state.copy()
        # check if move by n is valid
        if new_y < BOARD_SIZE_MIN:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white(new_x, new_y, pieces_to_move):
            return new_state
        else:
            if pieces_to_move == self.state["white"][self.piece_number][0]:
                new_state["white"][self.piece_number][2] = new_y
            else:
                new_state["white"][self.piece_number][0] -= pieces_to_move
                new_state["white"].append([pieces_to_move,new_x,new_y])
            return new_state

    def try_move_right(self, move_distance, pieces_to_move):
        new_x = self.state["white"][self.piece_number][1] + move_distance # x moves right by n
        new_y = self.state["white"][self.piece_number][2] # y stays the same
        new_state = self.state.copy()
        # check if move by n is valid
        if new_x > BOARD_SIZE_MAX:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white(new_x, new_y, pieces_to_move):
            return new_state
        else:
            if pieces_to_move == self.state["white"][self.piece_number][0]:
                new_state["white"][self.piece_number][1] = new_x
            else:
                new_state["white"][self.piece_number][0] -= pieces_to_move
                new_state["white"].append([pieces_to_move,new_x,new_y])
            return new_state


    def try_move_left(self, move_distance, pieces_to_move):
        new_x = self.state["white"][self.piece_number][1] - move_distance # x moves left by n
        new_y = self.state["white"][self.piece_number][2] # y stays the same
        new_state = self.state.copy()
        # check if move by n is allowable
        if new_x < BOARD_SIZE_MIN:
            return False
        # check if white piece lands on any black pieces
        if self.lands_on_black_check(new_x, new_y):
            return False
        # check if white piece lands on any white pieces
        if self.lands_on_white(new_x, new_y, pieces_to_move):
            return new_state
        else:
            if pieces_to_move == self.state["white"][self.piece_number][0]:
                new_state["white"][self.piece_number][1] = new_x
            else:
                new_state["white"][self.piece_number][0] -= pieces_to_move
                new_state["white"].append([pieces_to_move,new_x,new_y])
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

            for white_pieces in current_node.state["white"]:
                visited_nodes.add(tuple(white_pieces)) # avoid repeated state
            print("visited nodes:",visited_nodes)


            # when the goal state is found, trace back to the root node and print out the path
            if (not current_node.state["black"]):
                #print path
                return True

            else:
                # see if moving upper tile down is a valid move
                if current_node.try_move_down(1,self.piece_number):
                    new_state = current_node.try_move_down(1,self.piece_number)
                    # check if the resulting node is already visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        # create a new child node
                        current_node.move_down = Node(state=new_state,piece_number=self.piece_number,parent=current_node,\
                                                action='down',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)

                        queue.append(current_node.move_down)
                        depth_queue.append(current_depth+1)
                        path_cost_queue.append(current_path_cost)

                # see if moving left tile to the right is a valid move
                if current_node.try_move_right(1,self.piece_number):
                    new_state = current_node.try_move_right(1,self.piece_number)
                    # check if the resulting node is already visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        # create a new child node
                        current_node.move_right = Node(state=new_state,piece_number=self.piece_number,parent=current_node,\
                                                action='right',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                        queue.append(current_node.move_right)
                        depth_queue.append(current_depth+1)
                        path_cost_queue.append(current_path_cost)#######

                # see if moving lower tile up is a valid move
                if current_node.try_move_up(1,self.piece_number):
                    new_state = current_node.try_move_up(1,self.piece_number)
                    # check if the resulting node is already visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        # create a new child node
                         current_node.move_up = Node(state=new_state,piece_number=self.piece_number,parent=current_node,\
                                                action='up',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                         queue.append(current_node.move_up)
                         depth_queue.append(current_depth+1)
                         path_cost_queue.append(current_path_cost)

                # see if moving right tile to the left is a valid move
                if current_node.try_move_left(1,self.piece_number):
                    new_state = current_node.try_move_left(1,self.piece_number)
                    # check if the resulting node is already visited
                    if tuple(new_state["white"][-1]) not in visited_nodes:
                        # create a new child node
                        current_node.move_left = Node(state=new_state,piece_number=self.piece_number,parent=current_node,\
                                                action='left',depth=current_depth+1,path_cost=current_path_cost,heuristic_cost=0)
                        queue.append(current_node.move_left)
                        depth_queue.append(current_depth+1)
                        path_cost_queue.append(current_path_cost)
                for i in queue:
                    print("queue",i.state["white"])

                print("depth_queue",depth_queue)
                print_board(new_state)

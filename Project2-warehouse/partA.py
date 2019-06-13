#
# === Introduction ===
#
# In this problem, you will build a planner that helps a robot
#   find the best path through a warehouse filled with boxes
#   that it has to pick up and deliver to a dropzone.
#
# Your file must be called `partA.py` and must have a class
#   called `DeliveryPlanner`.
# This class must have an `__init__` function that takes three
#   arguments: `self`, `warehouse`, and `todo`.
# The class must also have a function called `plan_delivery` that
#   takes a single argument, `self`.
#
# === Input Specifications ===
#
# `warehouse` will be a list of m strings, each with n characters,
#   corresponding to the layout of the warehouse. The warehouse is an
#   m x n grid. warehouse[i][j] corresponds to the spot in the ith row
#   and jth column of the warehouse, where the 0th row is the northern
#   end of the warehouse and the 0th column is the western end.
#
# The characters in each string will be one of the following:
#
# '.' (period) : traversable space. The robot may enter from any adjacent space.
# '#' (hash) : a wall. The robot cannot enter this space.
# '@' (dropzone): the starting point for the robot and the space where all boxes must be delivered.
#   The dropzone may be traversed like a '.' space.
# [0-9a-zA-Z] (any alphanumeric character) : a box. At most one of each alphanumeric character
#   will be present in the warehouse (meaning there will be at most 62 boxes). A box may not
#   be traversed, but if the robot is adjacent to the box, the robot can pick up the box.
#   Once the box has been removed, the space functions as a '.' space.
#
# For example,
#   warehouse = ['1#2',
#                '.#.',
#                '..@']
#   is a 3x3 warehouse.
#   - The dropzone is at the warehouse cell in row 2, column 2.
#   - Box '1' is located in the warehouse cell in row 0, column 0.
#   - Box '2' is located in the warehouse cell in row 0, column 2.
#   - There are walls in the warehouse cells in row 0, column 1 and row 1, column 1.
#   - The remaining five warehouse cells contain empty space.
#
# The argument `todo` is a list of alphanumeric characters giving the order in which the
#   boxes must be delivered to the dropzone. For example, if
#   todo = ['1','2']
#   is given with the above example `warehouse`, then the robot must first deliver box '1'
#   to the dropzone, and then the robot must deliver box '2' to the dropzone.
#
# === Rules for Movement ===
#
# - Two spaces are considered adjacent if they share an edge or a corner.
# - The robot may move horizontally or vertically at a cost of 2 per move.
# - The robot may move diagonally at a cost of 3 per move.
# - The robot may not move outside the warehouse.
# - The warehouse does not "wrap" around.
# - As described earlier, the robot may pick up a box that is in an adjacent square.
# - The cost to pick up a box is 4, regardless of the direction the box is relative to the robot.
# - While holding a box, the robot may not pick up another box.
# - The robot may put a box down on an adjacent empty space ('.') or the dropzone ('@') at a cost
#   of 2 (regardless of the direction in which the robot puts down the box).
# - If a box is placed on the '@' space, it is considered delivered and is removed from the ware-
#   house.
# - The warehouse will be arranged so that it is always possible for the robot to move to the
#   next box on the todo list without having to rearrange any other boxes.
#
# An illegal move will incur a cost of 100, and the robot will not move (the standard costs for a
#   move will not be additionally incurred). Illegal moves include:
# - attempting to move to a nonadjacent, nonexistent, or occupied space
# - attempting to pick up a nonadjacent or nonexistent box
# - attempting to pick up a box while holding one already
# - attempting to put down a box on a nonadjacent, nonexistent, or occupied space
# - attempting to put down a box while not holding one
#
# === Output Specifications ===
#
# `plan_delivery` should return a LIST of moves that minimizes the total cost of completing
#   the task successfully.
# Each move should be a string formatted as follows:
#
# 'move {i} {j}', where '{i}' is replaced by the row-coordinate of the space the robot moves
#   to and '{j}' is replaced by the column-coordinate of the space the robot moves to
#
# 'lift {x}', where '{x}' is replaced by the alphanumeric character of the box being picked up
#
# 'down {i} {j}', where '{i}' is replaced by the row-coordinate of the space the robot puts
#   the box, and '{j}' is replaced by the column-coordinate of the space the robot puts the box
#
# For example, for the values of `warehouse` and `todo` given previously (reproduced below):
#   warehouse = ['1#2',
#                '.#.',
#                '..@']
#   todo = ['1','2']
# `plan_delivery` might return the following:
#   ['move 2 1',
#    'move 1 0',
#    'lift 1',
#    'move 2 1',
#    'down 2 2',
#    'move 1 2',
#    'lift 2',
#    'down 2 2']
#
# === Grading ===
#
# - Your planner will be graded against a set of test cases, each equally weighted.
# - If your planner returns a list of moves of total cost that is K times the minimum cost of
#   successfully completing the task, you will receive 1/K of the credit for that test case.
# - Otherwise, you will receive no credit for that test case. This could happen for one of several
#   reasons including (but not necessarily limited to):
#   - plan_delivery's moves do not deliver the boxes in the correct order.
#   - plan_delivery's output is not a list of strings in the prescribed format.
#   - plan_delivery does not return an output within the prescribed time limit.
#   - Your code raises an exception.
#
# === Additional Info ===
#
# - You may add additional classes and functions as needed provided they are all in the file `partA.py`.
# - Upload partA.py to Project 2 on T-Square in the Assignments section. Do not put it into an
#   archive with other files.
# - Your partA.py file must not execute any code when imported.
# - Ask any questions about the directions or specifications on Piazza.
#
import heapq
import copy

# define a priorityQueue, using code from AI class CS6601

class PriorityQueue(object):

    def __init__(self):
       #Initialize a new Priority Queue
        self.queue = []

    def pop(self):
        #Pop top priority node from queue.
        if self.queue:
            return heapq.heappop(self.queue)
        return None


    def __iter__(self):
        #Queue iterator.
        return iter(sorted(self.queue))

    def __str__(self):
        #Priority Queue to string
        return 'PQ:%s' % self.queue

    def __contains__(self, key):
        #Containment Check operator for 'in'
        return key in [n for _, n in self.queue]

    def __eq__(self, other):
        #Compare this Priority Queue with another Priority Queue.
        return self == other

    def append(self, node):
        #Append a node to the queue.
        heapq.heappush(self.queue, node)

    def size(self):
        return len(self.queue)


class DeliveryPlanner:

    def __init__(self, warehouse, todo):
        #translate the location of drop zone, boxes, walls and empty spaces in to grid indexes
        drop_zone=[]
        boxes={}
        walls=[]
        empties=[]
        for m in range(len(warehouse)):
            for n in range(len(warehouse[m])):
                if warehouse[m][n]=='@':
                    drop_zone.append([m,n])
                # check if character is alphanumeric  https://stackoverflow.com/questions/44057069/checking-if-any-character-in-a-string-is-alphanumeric
                elif warehouse[m][n].isalnum():
                    boxes[warehouse[m][n]]=[m,n]
                elif warehouse[m][n]=='#':
                    walls.append([m,n])
                elif warehouse[m][n]=='.':
                    empties.append([m,n])

        self.todo=todo
        self.warehouse=warehouse
        self.drop_zone=drop_zone[0]
        self.boxes_to_lift=[boxes[i] for i in todo]
        self.walls=walls
        self.empties=empties



    def accessible_neighbors(self,node):
        x=node[0]
        y=node[1]
        neighbors=[[x+1,y],[x-1,y],[x,y+1],[x,y-1],[x+1,y+1],[x-1,y-1],[x+1,y-1],[x-1,y+1]]
        accessible_neighbors=copy.deepcopy(neighbors)
        for neighbor in neighbors:
            if neighbor not in self.empties and (neighbor != self.drop_zone):
                accessible_neighbors.remove(neighbor)
        return accessible_neighbors

    def cost(self,node1, node2):
        cost=100
        if node1==node2:
            cost=0
        if node1[0]==node2[0] or node1[1]==node2[1]:
            cost=2
        if abs(node1[0]-node2[0])==1 and abs(node1[1]-node2[1])==1:
            cost=3
        return cost

    def heuristic(self,node1, node2):
        return sum([(x - y) ** 2 for (x, y) in zip(node1, node2)]) ** (0.5)

    def path_to_string(self,path):
        if path[0] in self.boxes_to_lift or path[0]==self.drop_zone:
            path=path[1:]
        if path[-1] in self.boxes_to_lift or path[-1]==self.drop_zone:
            path=path[:-1]
        moves=[]
        for element in path:
            move='move'+' '+str(element[0])+' '+str(element[1])
            moves.append(move)
        return moves

    def optimal_path(self,start,goal):
        if start==goal:
            return []
        frontier = PriorityQueue()
        frontier.append((0, [start]))
        explored = []
        while frontier.size() > 0:
            cost, path = frontier.pop()
            last_in_path = path[-1]
            if last_in_path == goal:
                return self.path_to_string(path)
            elif last_in_path not in explored:
                for node in self.accessible_neighbors(last_in_path):
                    new_path = list(path)
                    new_path.append(node)
                    # cost contains from last in path to goal distance
                    if node==goal:
                        cost_sum=cost
                    elif node in self.accessible_neighbors(goal):
                        cost_sum=cost+self.cost(last_in_path,node)
                    else:
                        cost_sum = cost + self.cost(last_in_path,node) + self.heuristic( node, goal) - self.heuristic(last_in_path, goal)
                    frontier.append((cost_sum, new_path))
                explored.append(last_in_path)

    def reset_grid(self,box):
        # replace a character in a string https://stackoverflow.com/questions/41752946/replacing-a-character-from-a-certain-index
        self.warehouse[box[0]] = self.warehouse[box[0]][:box[1]] + '.' + self.warehouse[box[0]][box[1] + 1:]
        self.empties.append(box)

    def string_to_index(self,str):
        #convert to move coordinate from string
        parsed=str.split()
        return [int(parsed[1]),int(parsed[2])]

    def plan_delivery(self):
        moves=[]
        moves_only=[('move' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1]))]
        swap = False
        for i in range (len(self.boxes_to_lift)):
            successful = False
            while not successful:
                box=self.boxes_to_lift[i]
                box_num=self.warehouse[box[0]][box[1]]
                # reset grid
                self.reset_grid(box)

                if box in self.accessible_neighbors(self.drop_zone) and moves_only[-1] == (
                                'move' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1])):
                    move_pos = box
                    move_to1=self.drop_zone
                    move_to2=self.drop_zone
                    move_to3 = self.drop_zone
                    move_to4 = self.drop_zone
                    neighborA = [self.drop_zone[0] - (self.drop_zone[0] - box[0]), self.drop_zone[1]]
                    neighborB = [self.drop_zone[0], self.drop_zone[1] - (self.drop_zone[1] - box[1])]
                    neighborC = [box[0], self.drop_zone[1] - 1]
                    neighborD = [box[0], self.drop_zone[1] + 1]
                    neighborE = [self.drop_zone[0] - 1, box[1]]
                    neighborF = [self.drop_zone[0] + 1, box[1]]
                    neighborG=[self.drop_zone[0],self.drop_zone[1]+1]
                    neighborH=[self.drop_zone[0],self.drop_zone[1]-1]
                    neighborI=[self.drop_zone[0]+1,self.drop_zone[1]]
                    neighborJ =[self.drop_zone[0]-1,self.drop_zone[1]]
                    if abs(self.drop_zone[0] - box[0]) == 1 and abs(
                                    self.drop_zone[1] - box[1]) == 1:  # box at diagonal position
                        move_to1 = neighborA
                        move_to2 = neighborB
                        move_to3 = neighborA
                        move_to4 = neighborB

                    elif abs(self.drop_zone[0] - box[0]) == 0: # box at verticle
                        move_to1 = neighborE
                        move_to2 = neighborF
                        move_to3=neighborI
                        move_to4=neighborJ
                    elif abs(self.drop_zone[1] - box[1]) == 0:
                        move_to1 = neighborC
                        move_to2 = neighborD
                        move_to3 = neighborG
                        move_to4 = neighborH
                        #     if move_to1 in self.accessible_neighbors(box):
                        #         move_pos=move_to1
                        #     elif move_to2 in self.accessible_neighbors(box):
                        #         move_pos=move_to2

                    cost=[100,100,100,100]
                    move_tos=[move_to1,move_to2,move_to3,move_to4]

                    for i in range(4):
                        if move_tos[i] in self.accessible_neighbors(box)  and move_tos[i]!=self.drop_zone:
                            if i<len(self.boxes_to_lift)-1:
                                cost[i]=self.heuristic(move_tos[i],self.boxes_to_lift[i+1])
                            if i==len(self.boxes_to_lift)-1:
                                cost[i] = self.heuristic(move_tos[i], box)
                    if min(cost)<100:
                        move_pos = move_tos[cost.index(min(cost))]

                    if move_pos!=box and len(moves)>0:
                        if moves[-1][:4]=='lift':
                            moves += [('move' + ' ' + str(move_pos[0]) + ' ' + str(move_pos[1]))]
                            moves_only += [('move' + ' ' + str(move_pos[0]) + ' ' + str(move_pos[1]))]
                            moves += [('down' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1]))]
                            moves += [('lift' + ' ' + box_num)]
                            successful = True
                            continue

                        moves += [('lift' + ' ' + box_num)]
                        moves += [('move' + ' ' + str(move_pos[0]) + ' ' + str(move_pos[1]))]
                        moves_only += [('move' + ' ' + str(move_pos[0]) + ' ' + str(move_pos[1]))]
                        moves += [('down' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1]))]
                        successful = True
                        continue

                    elif (i<len(self.boxes_to_lift)-1 ) or\
                                (i==len(self.boxes_to_lift)-1):

                        moves += [('lift' + ' ' + box_num)]
                        moves += [('move' + ' ' + str(move_pos[0]) + ' ' + str(move_pos[1]))]
                        moves_only+=[('move' + ' ' + str(move_pos[0]) + ' ' + str(move_pos[1]))]
                        moves += [('down' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1]))]

                        moves += [('move' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1]))]
                        moves_only+=[('move' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1]))]
                        successful = True
                        continue

                moves_to_box=self.optimal_path(self.drop_zone,box)
                moves_to_dropzone=self.optimal_path(box,self.drop_zone)

                if len(moves_only)>1:
                    if moves_only[-1][:4]=='move':
                        xy=self.string_to_index(moves_only[-1])
                        # x2 = int(moves_to_box[0][5])
                        # y2 = int(moves_to_box[0][7])
                        moves_to_box = self.optimal_path(xy, box)

                        # delete repeated actions before and after down;
                        if len(moves_to_box)>0:
                            if moves_only[-1]==moves_to_box[0]:
                                moves_to_box.remove(moves_to_box[0])
                if swap==True:
                    if len(moves_to_box) > 0 :
                        moves+=[moves_to_box[0]]
                        moves_only+=[moves_to_box[0]]
                        moves_to_box.remove(moves_to_box[0])

                    elif box in self.accessible_neighbors(self.drop_zone):
                        if abs(self.drop_zone[0]-box[0])==1 and abs(self.drop_zone[1]-box[1])==1:
                            move_to1=[self.drop_zone[0]-(self.drop_zone[0]-box[0]),self.drop_zone[1]]
                            move_to2=[self.drop_zone[0],self.drop_zone[1]-(self.drop_zone[1]-box[1])]
                            if move_to1 in self.accessible_neighbors(box):
                                moves += [('move' + ' ' + str(move_to1[0]) + ' ' + str(move_to1[1]))]
                                moves_only +=[('move' + ' ' + str(move_to1[0]) + ' ' + str(move_to1[1]))]
                            elif move_to2 in self.accessible_neighbors(box):
                                moves += [('move' + ' ' + str(move_to2[0]) + ' ' + str(move_to2[1]))]
                                moves_only+=[('move' + ' ' + str(move_to2[0]) + ' ' + str(move_to2[1]))]

                            else:
                                moves += [('move' + ' ' + str(box[0]) + ' ' + str(box[1]))]
                                moves_only += [('move' + ' ' + str(box[0]) + ' ' + str(box[1]))]

                    if moves[-1]!='move' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1]):
                        moves += [('down' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1]))]
                    else:
                        moves.pop()
                        moves += [('down' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1]))]
                        moves+=[('move' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1]))]

                moves+=moves_to_box
                moves_only+=moves_to_box
                moves+=[('lift'+' '+box_num)]

                if len(moves_only) > 1:
                    if moves_only[-1][:4] == 'move':
                        xy=self.string_to_index(moves_only[-1])
                        moves_to_dropzone = self.optimal_path(xy, self.drop_zone)
                        # delete repeated actions before and after lift;
                        if len(moves_to_dropzone)>0:
                            if moves_only[-1] == moves_to_dropzone[0]:
                                moves_to_dropzone.remove(moves_to_dropzone[0])
                moves+=moves_to_dropzone
                moves_only+=moves_to_dropzone

                if moves_only[-1]!=('move' + ' ' + str(self.drop_zone[0]) + ' ' + str(self.drop_zone[1])) :
                    moves+=[('down'+' '+str(self.drop_zone[0])+' '+str(self.drop_zone[1]))]
                    swap=False
                    successful=True


                elif box_num==self.todo[-1]:
                    successful=False
                else:
                    swap=True
                    successful=True

        if moves[-1][:4]!='down':
            moves=moves[:-1]
        return moves
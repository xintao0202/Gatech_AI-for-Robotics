#
# === Introduction ===
#
# In this problem, you will again build a planner that helps a robot
#   find the best path through a warehouse filled with boxes
#   that it has to pick up and deliver to a dropzone. Unlike Part A,
#   however, in this problem the robot is moving in a continuous world
#   (albeit in discrete time steps) and has constraints on the amount
#   it can turn its wheels in a given time step.
#
# Your file must be called `partB.py` and must have a class
#   called `DeliveryPlanner`.
# This class must have an `__init__` function that takes five
#   arguments: `self`, `warehouse`, `todo`, `max_distance`, and
#   `max_steering`.
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
# '.' (period) : traversable space.
# '#' (hash) : a wall. If the robot contacts a wall space, it will crash.
# '@' (dropzone): the space where all boxes must be delivered. The dropzone may be traversed like
#   a '.' space.
#
# Each space is a 1 x 1 block. The upper-left corner of space warehouse[i][j] is at the point (j,-i) in
#   the plane. Spaces outside the warehouse are considered walls; if any part of the robot leaves the
#   warehouse, it will be considered to have crashed into the exterior wall of the warehouse.
#
# For example,
#   warehouse = ['.#.',
#                '.#.',
#                '..@']
#   is a 3x3 warehouse. The dropzone is at space (2,-2) and there are walls at spaces (1,0)
#   and (1,-1). The rest of the warehouse is empty space.
#
# The robot is a circle of radius 0.25. The robot begins centered in the dropzone space.
#   The robot's initial bearing is 0.
#
# The argument `todo` is a list of points representing the center point of each box.
#   todo[0] is the first box which must be delivered, followed by todo[1], and so on.
#   Each box is a square of size 0.2 x 0.2. If the robot contacts a box, it will crash.
#
# The arguments `max_distance` and `max_steering` are parameters constraining the movement
#   of the robot on a given time step. They are described more below.
#
# === Rules for Movement ===
#
# - The robot may move any distance between 0 and `max_distance` per time step.
# - The robot may set its steering angle anywhere between -`max_steering` and
#   `max_steering` per time step. A steering angle of 0 means that the robot will
#   move according to its current bearing. A positive angle means the robot will
#   turn counterclockwise by `steering_angle` radians; a negative steering_angle
#   means the robot will turn clockwise by abs(steering_angle) radians.
# - Upon a movement, the robot will change its steering angle instantaneously to the
#   amount indicated by the move, and then it will move a distance in a straight line in its
#   new bearing according to the amount indicated move.
# - The cost per move is 1 plus the amount of distance traversed by the robot on that move.
#
# - The robot may pick up a box whose center point is within 0.5 units of the robot's center point.
# - If the robot picks up a box, it incurs a total cost of 2 for that move (this already includes
#   the 1-per-move cost incurred by the robot).
# - While holding a box, the robot may not pick up another box.
# - The robot may put a box down at a total cost of 1.5 for that move. The box must be placed so that:
#   - The box is not contacting any walls, the exterior of the warehouse, any other boxes, or the robot
#   - The box's center point is within 0.5 units of the robot's center point
# - A box is always oriented so that two of its edges are horizontal and the other two are vertical.
# - If a box is placed entirely within the '@' space, it is considered delivered and is removed from the
#   warehouse.
# - The warehouse will be arranged so that it is always possible for the robot to move to the
#   next box on the todo list without having to rearrange any other boxes.
#
# - If the robot crashes, it will stop moving and incur a cost of 100*distance, where distance
#   is the length it attempted to move that move. (The regular movement cost will not apply.)
# - If an illegal move is attempted, the robot will not move, but the standard cost will be incurred.
#   Illegal moves include (but are not necessarily limited to):
#     - picking up a box that doesn't exist or is too far away
#     - picking up a box while already holding one
#     - putting down a box too far away or so that it's touching a wall, the warehouse exterior,
#       another box, or the robot
#     - putting down a box while not holding a box
#
# === Output Specifications ===
#
# `plan_delivery` should return a LIST of strings, each in one of the following formats.
#
# 'move {steering} {distance}', where '{steering}' is a floating-point number between
#   -`max_steering` and `max_steering` (inclusive) and '{distance}' is a floating-point
#   number between 0 and `max_distance`
#
# 'lift {b}', where '{b}' is replaced by the index in the list `todo` of the box being picked up
#   (so if you intend to lift box 0, you would return the string 'lift 0')
#
# 'down {x} {y}', where '{x}' is replaced by the x-coordinate of the center point of where the box
#   will be placed and where '{y}' is replaced by the y-coordinate of that center point
#   (for example, 'down 1.5 -2.9' means to place the box held by the robot so that its center point
#   is (1.5,-2.9)).
#
# === Grading ===
#
# - Your planner will be graded against a set of test cases, each equally weighted.
# - Each task will have a "baseline" cost. If your set of moves results in the task being completed
#   with a total cost of K times the baseline cost, you will receive 1/K of the credit for the
#   test case. (Note that if K < 1, this means you earn extra credit!)
# - Otherwise, you will receive no credit for that test case. This could happen for one of several
#   reasons including (but not necessarily limited to):
#   - plan_delivery's moves do not deliver the boxes in the correct order.
#   - plan_delivery's output is not a list of strings in the prescribed format.
#   - plan_delivery does not return an output within the prescribed time limit.
#   - Your code raises an exception.
#
# === Additional Info ===
#
# - You may add additional classes and functions as needed provided they are all in the file `partB.py`.
# - Your partB.py file must not execute any code when it is imported.
# - Upload partB.py to Project 2 on T-Square in the Assignments section. Do not put it into an
#   archive with other files.
# - Ask any questions about the directions or specifications on Piazza.
#
import heapq
import copy
from math import *

import itertools

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

    def __init__(self, warehouse, todo, max_distance, max_steering):

        ######################################################################################
        # TODO: You may use this function for any initialization required for your planner
        ######################################################################################
        drop_zone = []
        discretized_by=5
        walls = []
        empties = []

        for m in range(len(warehouse)):
            for n in range(len(warehouse[m])):
                if warehouse[m][n] == '@':
                    drop_zone.append([m, n])
                elif warehouse[m][n] == '#':
                    walls.append([m, n])
                elif warehouse[m][n] == '.':
                    empties.append([m, n])

        self.todo = todo
        self.warehouse = warehouse
        self.max_distance=max_distance
        self.max_steering=max_steering
        self.drop_zone = drop_zone[0]
        self.walls = walls
        self.empties = empties
        # define how much the grid will be expanded
        self.resolution=[len(warehouse[0])*discretized_by,len(warehouse)*discretized_by]
        self.discretized_by=discretized_by
        #calculate robot start cooridnate and size of grid
        self.Xsize=len(warehouse[0])
        self.Ysize=len(warehouse)
        self.robot_start=self.centerof(drop_zone[0],1)
        self.robot_R=0.25
        self.box_L=0.2
        self.grid_d,self.drop_zones_d, self.empties_d=self.grid_discretization()

    def centerof(self, node,discretized_by):
        x=((node[1]+node[1]+1.0)/discretized_by)/2.0
        y=((-node[0]-node[0]-1.0)/discretized_by)/2.0
        x=round(x,6)
        y=round(y, 6)
        return [x,y]

    def robot_start_d(self):
        center_x=int(self.drop_zone[0]*self.discretized_by+self.discretized_by/2)
        center_y=int(self.drop_zone[1]*self.discretized_by+self.discretized_by/2)
        return [center_x,center_y]

    def heuristic(self, node1, node2):
        return sum([(x - y) ** 2 for (x, y) in zip(node1, node2)]) ** (0.5)

    def threshold_dist(self,node1,R,node2,L):
        theta = atan2(abs(node1[1] - node2[1]), abs(node1[0] - node2[0]))
        if theta==0 or theta==pi/2:
            return R+L/2
        a = L / 2 - (L / 2) / tan(theta)
        dist = (L / 2) / sin(theta) + a * cos(theta) + sqrt(R ** 2 - a ** 2 * (sin(theta) ** 2))
        return dist

    def grid_discretization(self):
        #initialize the new grid to all'#'
        grid_new=[['#' for row in range(self.resolution[0])] for col in range(self.resolution[1])]
        drop_zones = []
        empties=[]
        for m in range(self.Ysize*self.discretized_by):
            for n in range (self.Xsize*self.discretized_by):
                #mark all dropzones
                if self.warehouse[m/self.discretized_by][n/self.discretized_by]=='@':
                    grid_new[m]=grid_new[m][:n]+['@']+grid_new[m][n+1:]
                    if [m,n] not in drop_zones:
                        drop_zones.append([m,n])
                        #empties.append([m,n])
                elif self.warehouse[m/self.discretized_by][n/self.discretized_by]=='.':
                    grid_new[m] = grid_new[m][:n] + ['.'] + grid_new[m][n + 1:]
                    if [m,n] not in empties:
                        empties.append([m,n])

        # if drop_zone_point center is too close to drop zone then remove the point from drop_zone_d and make it empty
        zone_left=self.drop_zone[1]
        zone_right=self.drop_zone[1]+1
        zone_up=-self.drop_zone[0]
        zone_down=-self.drop_zone[0]-1
        drop_zones_d=copy.deepcopy(drop_zones)
        for drop in drop_zones:
            if abs(self.centerof(drop,self.discretized_by)[0]-zone_left)<(self.box_L+0.01)/2.0 or \
                abs(self.centerof(drop, self.discretized_by)[0] - zone_right) < (self.box_L + 0.01) / 2.0 or \
                abs(self.centerof(drop, self.discretized_by)[1] - zone_up) < (self.box_L + 0.01) / 2.0 or \
                abs(self.centerof(drop, self.discretized_by)[1] - zone_down) < (self.box_L + 0.01) / 2.0:
                drop_zones_d.remove(drop)
                empties.append(drop)
        return grid_new,drop_zones_d,empties

    def accessible_neighbors(self,node):
        x=node[0]
        y=node[1]
        neighbors=[[x+1,y],[x-1,y],[x,y+1],[x,y-1],[x+1,y+1],[x-1,y-1],[x+1,y-1],[x-1,y+1]]
        accessible_neighbors=copy.deepcopy(neighbors)
        for neighbor in neighbors:
            if neighbor not in self.empties_d and (neighbor not in self.drop_zones_d):
                accessible_neighbors.remove(neighbor)
        return accessible_neighbors

    def cost(self,node1, node2, lift=False,down=False, steering=False):
        cost=1
        #when there is a steer of reach max, then add 1 cost
        #cost=1
        # - The cost per move is 1 plus the amount of distance traversed by the robot on that move.

        if steering==False:
            cost-=1
        if node1!=node2:
            cost+=self.heuristic(node1,node2)
        else:
            cost=0
        # - If the robot picks up a box, it incurs a total cost of 2 for that move (this already includes
        #   the 1-per-move cost incurred by the robot).
        if lift==True:
            cost+=1
        #- The robot may put a box down at a total cost of 1.5 for that move.
        if down==True:
            cost += 0.5

        return cost
    # use code from project 1
    def angle_trunc(self,a):
        """This maps all angles to a domain of [-pi, pi]"""
        while a < 0.0:
            a += pi * 2
        return ((a + pi) % (pi * 2)) - pi

    def path_to_string(self, path, last_bearing=0):
        moves = []
        if len(path)==2:
            bearing = self.angle_trunc(atan2(-path[1][0] + path[0][0], path[1][1] - path[0][1]))
            steering =bearing-last_bearing
            dist = self.heuristic(self.centerof(path[0], self.discretized_by),
                                  self.centerof(path[1], self.discretized_by))
            while abs(steering) > self.max_steering:
                move = 'move' + ' ' + str(self.max_steering * (steering / abs(steering))) + ' ' + str(0.0)
                moves.append(move)
                steering -= self.max_steering * (steering / abs(steering))
            while dist>self.max_distance:
                move = 'move' + ' ' + str(steering) + ' ' + str(self.max_distance)
                moves.append(move)
                dist-=self.max_distance
                steering=0
            move = 'move' + ' ' + str(steering) + ' ' + str(dist)
            moves.append(move)

        bearing=[last_bearing for i in range(len(path))]
        bearing[1] = self.angle_trunc(atan2(-path[1][0] + path[0][0], path[1][1] - path[0][1]))
        last_in_seg=0
        for i in range(2,len(path)):
            bearing[i]=self.angle_trunc(atan2(-path[i][0]+path[i-1][0],path[i][1]-path[i-1][1]))
            steering =bearing[i]-bearing[i-1]
            dist = self.heuristic(self.centerof(path[last_in_seg], self.discretized_by),
                                  self.centerof(path[i - 1], self.discretized_by))
            steer_angle = self.angle_trunc(bearing[i - 1] - bearing[last_in_seg])
            if steering!=0:
                while abs(steer_angle)>self.max_steering:
                    move = 'move' + ' ' + str(self.max_steering*(steer_angle/abs(steer_angle))) + ' ' + str(0.0)
                    moves.append(move)
                    steer_angle-=self.max_steering*(steer_angle/abs(steer_angle))

                last_in_seg = i - 1
                while dist>self.max_distance:
                    move='move' + ' ' + str(steer_angle) + ' ' + str(self.max_distance)
                    moves.append(move)
                    dist-=self.max_distance
                    steer_angle=0
                move = 'move' + ' ' + str(steer_angle) + ' ' + str(dist)
                moves.append(move)
            elif dist>self.max_distance:
                last_in_seg = i - 2
                dist-=self.heuristic(self.centerof(path[i - 2], self.discretized_by),
                                  self.centerof(path[i - 1], self.discretized_by))
                while abs(steer_angle)>self.max_steering:
                    move = 'move' + ' ' + str(self.max_steering*(steer_angle/abs(steer_angle))) + ' ' + str(0.0)
                    moves.append(move)
                    steer_angle-=self.max_steering*(steer_angle/abs(steer_angle))
                move = 'move' + ' ' + str(steer_angle) + ' ' + str(dist)
                moves.append(move)
            if i==len(path)-1:
                steer_angle = self.angle_trunc(bearing[i] - bearing[last_in_seg])
                dist = self.heuristic(self.centerof(path[last_in_seg], self.discretized_by),
                                      self.centerof(path[i], self.discretized_by))
                while abs(steer_angle)>self.max_steering:
                    move = 'move' + ' ' + str(self.max_steering*(steer_angle/abs(steer_angle))) + ' ' + str(0.0)
                    moves.append(move)
                    steer_angle-=self.max_steering*(steer_angle/abs(steer_angle))
                while dist>self.max_distance:
                    move='move' + ' ' + str(steer_angle) + ' ' + str(self.max_distance)
                    moves.append(move)
                    dist-=self.max_distance
                    steer_angle=0
                move = 'move' + ' ' + str(steer_angle) + ' ' + str(dist)
                moves.append(move)

        return moves,bearing[len(path)-1]

    def lift_areas(self,box):
        areas = []
        # if lift_areas return none, then find next distance around box
        increment=0
        while len(areas)==0:
            for point in self.empties_d+self.drop_zones_d:
                dist = self.heuristic(box, self.centerof(point,self.discretized_by))
                if dist <=0.5+increment and dist>=self.threshold_dist(self.centerof(point,self.discretized_by),self.robot_R,box,self.box_L):
                    areas.append(point)
            increment+=0.5/self.discretized_by
        return areas

    def close_box_points(self, box, empties):
        close_points=[]
        for point in empties:
            dist = self.heuristic(box, self.centerof(point, self.discretized_by))
            if dist < self.threshold_dist(self.centerof(point, self.discretized_by), self.robot_R, box,self.box_L):
                close_points.append(point)
        return close_points

    def close_wall_points(self):
        close_points=[]
        for point in self.empties_d+self.drop_zones_d:
            grid_center = self.centerof(point, self.discretized_by)
            for wall in self.walls:
                wall_center = self.centerof(wall, 1)
                dist=self.heuristic(grid_center, wall_center)
                if dist < self.robot_R+sqrt(2*0.5**2):
                    close_points.append(point)
        return close_points

    def close_boarder_points(self):
        boarder_points = []
        dist_to_boarder=0.5/self.discretized_by
        if dist_to_boarder<self.robot_R:
            for point in self.empties_d+self.drop_zones_d:
                if point[0]==0 or point[0]==len(self.grid_d)-1 or point[1]==0 or point[1]==len(self.grid_d[0])-1:
                    if point not in boarder_points:
                        boarder_points.append(point)
        return boarder_points

    def drop_areas(self):
        areas=[]
        for point in self.empties_d:
            for drop in self.drop_zones_d:
                dist=self.heuristic(self.centerof(drop,self.discretized_by),self.centerof(point,self.discretized_by))
                if dist<self.threshold_dist(self.centerof(point,self.discretized_by),self.robot_R,self.centerof(drop,self.discretized_by),self.box_L) and\
                    point not in areas:
                    areas.append(point)
        return areas

    def closed_drop_zone(self, drop):
        dist={}
        for i in range(len(self.drop_zones_d)):
            dist[i]=self.heuristic(self.centerof(drop,self.discretized_by),self.centerof(self.drop_zones_d[i],self.discretized_by))
        min_index=min(dist, key=dist.get)
        return self.drop_zones_d[min_index]

    # take a first guess of best pair of pick-drop pairs
    def best_areas_tolift(self,last_loc,box):
        pairs=PriorityQueue()
        pair=[]
        for lift in self.lift_areas(box):
            dist = self.heuristic(self.centerof(lift, self.discretized_by),
                                  self.centerof(last_loc,self.discretized_by))
            if[lift, last_loc] not in pair:
                pairs.append((dist, [lift, last_loc]))
                pair.append([lift, last_loc])
        return pairs

    def best_areas_todrop(self,last_loc,box):
        pairs=PriorityQueue()
        pair=[]

        for drop in self.drop_areas():
            dist = self.heuristic(self.centerof(last_loc,self.discretized_by), self.centerof(drop,self.discretized_by))
            if [last_loc,drop] not in pair:
                pairs.append((dist,[last_loc,drop]))
                pair.append([last_loc, drop])
        return pairs

    def optimal_path(self, start, goal,last_bearing):
        if start == goal:
            return []
        if goal in self.accessible_neighbors(start):
            path=[start,goal]
            return self.path_to_string(path, last_bearing)
        frontier = PriorityQueue()
        frontier.append((0, [start]))
        explored = []
        while frontier.size() > 0:
            cost, path = frontier.pop()
            last_in_path = path[-1]
            if last_in_path == goal:
                return self.path_to_string(path,last_bearing)
            elif last_in_path not in explored:
                for node in self.accessible_neighbors(last_in_path):
                    if node not in explored:
                        new_path = list(path)
                        new_path.append(node)
                        # cost contains from last in path to goal distance
                        # penalty for not moving
                        if len(new_path) > 1 and new_path[-1] == new_path[-2]:
                            cost += 100
                        if node == goal:
                            cost_sum = cost
                        else:
                            add_cost=self.cost(last_in_path, node,steering=False)
                            # determine when to add additional 1 cost
                            if len(new_path)==1 or\
                                (len(new_path) > 2 and abs(self.heuristic(new_path[-3], new_path[-2]) +
                                                               self.heuristic(new_path[-2],new_path[-1]) - self.heuristic(new_path[-3], new_path[-1])) > 0.0001):
                                add_cost = self.cost(last_in_path, node, steering=True)
                            cost_sum = cost + add_cost + self.heuristic(node, goal) - self.heuristic(
                                last_in_path, goal)
                        frontier.append((cost_sum, new_path))
                explored.append(last_in_path)
        return [[],last_bearing]
    # if there is a final move needed to get close enough to the box, then need to merge this move with the previous move
    def absorb_tail(self,path,last_bearing,last_loc,box,difference):
        moves=[]
        side2=difference+0.01 #overshoot a little to make sure it within reaching distances
        bearing2 = self.angle_trunc(atan2(box[1] - self.centerof(last_loc, self.discretized_by)[1],
                                          box[0] - self.centerof(last_loc, self.discretized_by)[0]))
        bearing1=last_bearing
        steer_angle2 = self.angle_trunc(bearing2 - bearing1)

        if len(path)==0:
            new_steering=steer_angle2
            new_length=side2
            while abs(new_steering) > self.max_steering:
                moves += ['move' + ' ' + str(self.max_steering * (new_steering / abs(new_steering))) + ' ' + str(0.0)]
                new_steering -= self.max_steering * (new_steering / abs(new_steering))
            moves += ['move' + ' ' + str(new_steering) + ' ' + str(new_length)]  # add 0.01 more
            return  moves

        new_path=path[:-1]
        threshold = 0.05
        #new length will be the third side of an triangle
        side1=float(path[-1].split()[2])

        angle=self.angle_trunc(pi-steer_angle2)
        if abs(steer_angle2)<threshold or abs(steer_angle2-pi)<threshold or abs(steer_angle2+pi)<threshold:
            new_length=sqrt(side1**2+side2**2-2*side1*side2*cos(angle))
            new_steering= float(path[-1].split()[1])+steer_angle2
        else:
            new_length=side2
            new_steering=steer_angle2
        while abs(new_steering) > self.max_steering:
            moves += ['move' + ' ' + str(self.max_steering* (new_steering / abs(new_steering))) + ' ' + str(0.0)]
            new_steering -= self.max_steering*(new_steering/abs(new_steering))
        while new_length > self.max_distance:
            moves+=['move' + ' ' + str(new_steering) + ' ' + str(self.max_distance)]
            new_length -= self.max_distance
            new_steering = 0
        moves += ['move' + ' ' + str(new_steering) + ' ' + str(new_length)]  # add 0.01 more
        if abs(steer_angle2) < threshold or abs(steer_angle2-pi)<threshold or abs(steer_angle2+pi)<threshold:
            new_path+=moves
        else:
            new_path+=[path[-1]]+moves
        return new_path

    def absorb_head(self,path,last_bearing,difference):
        moves = []
        if len(path)==0:
            new_steering=pi
            new_length=difference+0.01
            while abs(new_steering) > self.max_steering:
                moves += ['move' + ' ' + str(self.max_steering * (new_steering / abs(new_steering))) + ' ' + str(0.0)]
                new_steering -= self.max_steering * (new_steering / abs(new_steering))
            moves += ['move' + ' ' + str(new_steering) + ' ' + str(new_length)]  # add 0.01 more
            return  moves
        #find the non zero move
        index=0
        steer_angle=0
        threshold=0.05
        for i in range(len(path)):
            if round(float(path[i].split()[2]),1)==0.0:
                steer_angle += float(path[i].split()[1])
            else:
                index = i
                steer_angle += float(path[i].split()[1])
                break
        steer_angle=self.angle_trunc(steer_angle)
        new_path=path[index+1:]
        side1=difference+0.01
        side2=float(path[index].split()[2])
        bearing1=last_bearing+pi
        angle = self.angle_trunc(pi - steer_angle)
        if abs(steer_angle)<threshold or abs(steer_angle-pi)<threshold or abs(steer_angle+pi)<threshold:
            new_length=sqrt(side1**2+side2**2-2*side1*side2*cos(angle))
            new_steering= self.angle_trunc(bearing1+steer_angle-last_bearing)
        else:
            new_length = side1
            new_steering = pi
        while abs(new_steering) > self.max_steering:
            moves += ['move' + ' ' + str(self.max_steering* (new_steering / abs(new_steering))) + ' ' + str(0.0)]
            new_steering -= self.max_steering*(new_steering/abs(new_steering))
        while new_length > self.max_distance:
            moves+=['move' + ' ' + str(new_steering) + ' ' + str(self.max_distance)]
            new_length -= self.max_distance
            new_steering = 0
        moves += ['move' + ' ' + str(new_steering) + ' ' + str(new_length)]  # add 0.01 more
        if abs(steer_angle) <threshold or abs(steer_angle-pi)<threshold or abs(steer_angle+pi)<threshold:
            new_path=moves+new_path
        else:
            new_path=moves+path
        return new_path


    def plan_delivery(self):
        moves = []
        pair=[]
        last_loc = self.robot_start_d()
        last_bearing = 0
        empties_e=copy.deepcopy(self.empties_d)
        empties_d=copy.deepcopy(self.drop_zones_d)
        # add box restrictions
        for i in range(len(self.todo)):
            for point in self.close_box_points(self.todo[i], empties_e):
                if point in self.empties_d:
                    self.empties_d.remove(point)

            for point in self.close_box_points(self.todo[i], empties_d):
                if point in self.drop_zones_d:
                    self.drop_zones_d.remove(point)

            for point in self.close_wall_points()+self.close_boarder_points():
                if point in self.empties_d:
                    self.empties_d.remove(point)
                if point in self.drop_zones_d:
                    self.drop_zones_d.remove(point)
        for i in range(len(self.todo)):
            pairs_to_box=self.best_areas_tolift(last_loc,self.todo[i])
            path_to_box=[]
            while not path_to_box and pairs_to_box.size()>0:
                length,pair=pairs_to_box.pop()
                if pair[0]==pair[1]:
                    break
                else:
                    path_to_box,last_bearing=self.optimal_path(last_loc,pair[0],last_bearing)
            last_loc=pair[0]
            moves+=path_to_box
            #check if robot center is less than 0.5
            difference=self.heuristic(self.centerof(last_loc,self.discretized_by),self.todo[i])-0.5
            bearing=last_bearing
            if difference>=0:
                bearing= self.angle_trunc(atan2(self.todo[i][1] - self.centerof(last_loc,self.discretized_by)[1], self.todo[i][0] - self.centerof(last_loc,self.discretized_by)[0]))
                moves=self.absorb_tail(moves,last_bearing,last_loc,self.todo[i],difference)
                moves += ['lift' + ' ' + str(i)]
                last_bearing=self.angle_trunc(bearing+pi)
            else:
                moves+=['lift'+' '+str(i)]
            for point in self.close_box_points(self.todo[i],empties_e):
                self.empties_d.append(point)
            for point in self.close_box_points(self.todo[i], empties_d):
                self.drop_zones_d.append(point)
            pairs_to_drop=self.best_areas_todrop(last_loc,self.todo[i])
            path_to_drop=[]
            while not path_to_drop and pairs_to_drop.size()>0:
                length,pair=pairs_to_drop.pop()
                if pair[0]==pair[1]:
                    break
                else:
                    path_to_drop,last_bearing=self.optimal_path(pair[0],pair[1],last_bearing)

            if difference>=0:
                path_to_drop=self.absorb_head(path_to_drop,self.angle_trunc(bearing),difference)
            moves+=path_to_drop
            last_loc=pair[1]
            down_x=self.centerof(self.closed_drop_zone(last_loc),self.discretized_by)[0]
            down_y=self.centerof(self.closed_drop_zone(last_loc),self.discretized_by)[1]
            moves+=['down'+' '+str(down_x)+' '+str(down_y)]

        return moves
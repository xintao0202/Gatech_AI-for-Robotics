import string
import sys
import copy

from functools import wraps
from Queue import Queue
from Queue import Empty as QueueEmptyError
from threading import Thread
from multiprocessing import TimeoutError

import unittest
import timeit

import partB
from math import *

warehouse= ['@.#...#',
                          '#...#..']
todo=   [(6.8, -1.8), (6.0, -1.2), (5.0, -0.8),
                     (4.0, -0.2), (3.8, -1.2), (2.8, -1.2),
                     (1.8, -1.8), (1.2, -1.1), (1.1, -0.1)]

student_planner = partB.DeliveryPlanner(copy.copy(warehouse), copy.copy(todo),
                                        0.29, pi / 5.7)
# print student_planner.centerof([0,0],3) #pass
# print student_planner.centerof([14,14],3) #pass

#print student_planner.best_areas((4.5, -.5),first_round=True)


# print student_planner.lift_areas([0.5, -1.0])
#print student_planner.best_areas([1.5,-0.5])
# b=student_planner.best_areas([1.5,-0.5])
# while  b.size()>0:
#       a=b.pop()
#       print a
#print student_planner.accessible_neighbors([1, 7]) #pass
# cost=student_planner.cost([2,2],[1,0]) #pass
# print student_planner.heuristic([0.5, -1.0],student_planner.centerof([2, 0],discretized_by=3)) #pass
# print student_planner.threshold_dist(student_planner.centerof([2, 0],student_planner.discretized_by),student_planner.robot_R,[0.5, -1.0],student_planner.box_L)
#print student_planner.optimal_path([1, 1], [4, 19], 0)
#print student_planner.close_boarder_points()
#print student_planner.close_wall_points()
#print student_planner.angle_trunc(-3.14159265358)

# path=[[11, 11], [12, 10], [13, 9], [13, 8], [13, 7], [13, 6], [13, 5], [12, 4], [11, 4], [10, 4], [9, 4], [8, 4], [7, 4], [6, 4], [5, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10], [4, 11], [4, 12], [4, 13], [4, 14], [3, 15]]
#
# print student_planner.path_to_string (path,0.7853981633974483)
#print student_planner.absorb_head(['move 0.0 2.666667', 'move 0.785398163397 0.471404049387'],1.57079632679,0.0)

#print student_planner.absorb_tail(['move -1.58079632679 0.0', 'move -1.56079632679 0.333333'], -3.14159265359, [1, 6], (1.5, -0.5), 0.166667)

#print student_planner.best_areas_tolift([20,20],(4.0, -2.5))

print student_planner.best_path([1,1],[5,5])

a,b,c=student_planner.grid_discretization()
for row in a:
    print row

#print student_planner.plan_delivery()

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

import partA

warehouse=  ['..1.',
                          '..@.',
                          '....',
                          '2...']
todo=  ['1', '2']

student_planner = partA.DeliveryPlanner(copy.copy(warehouse), copy.copy(todo))
# accessible_neighbors = student_planner.accessible_neighbors([2,1]) #pass
# cost=student_planner.cost([2,2],[1,0]) #pass
# heuristic=student_planner.heuristic([0,0],[1,1]) #pass
# optimal_path=student_planner.optimal_path([0,0],[2,2])
plan_delivery=student_planner.plan_delivery()
print plan_delivery
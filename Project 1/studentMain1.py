# These import steps give you access to libraries which you may (or may
# not) want to use.
from math import *
from robot import *
from matrix import *
import random

# This is the function you have to write. The argument 'measurement' is a
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    X_measure = measurement[0]
    Y_measure = measurement[1]

    if not OTHER:  # this is the first measurement
        pos_pre = (random.random() * X_measure, random.random() * Y_measure)  # in the format of (X,Y)
        orientation_pre = random.random() * 2 * pi
        dist_sum = 0
        num_measure = 0
        deltaX_pst=0
        deltaY_pst=0
        orientation_measure=atan2(Y_measure, X_measure)
        orientation_sum = 0


    else:
        pos_pre = OTHER['pos']
        orientation_pre = OTHER['orientation']
        dist_sum = OTHER['sum']
        num_measure = OTHER['num']
        orientation_sum = OTHER['orientation_sum']


        X_pre = pos_pre[0]
        Y_pre = pos_pre[1]
        deltaX = X_measure - X_pre
        deltaY = Y_measure - Y_pre
        orientation_measure = atan2(deltaY, deltaX)
        angle_steer = orientation_measure - orientation_pre
        angle_steer %= 2 * pi  # make sure to normalize the angle
        #print angle_steer
        # calculate the pst position and orientation using pre and measurement (assume distance the same)
        dist = distance_between(measurement, pos_pre)

        # normalize distances to obtain more realist distance by obtaining the mean of movements, also adding noise
        dist_sum = dist_sum + dist
        num_measure = num_measure + 1

        dist_correction = dist_sum / num_measure
        orientation_sum += angle_trunc(angle_steer)
        if num_measure<=2:
            orientation_correction=angle_trunc(angle_steer)
        else:
            orientation_correction = orientation_sum / (num_measure-2)
        orientation_pst = orientation_measure + orientation_correction

        deltaX_pst = dist_correction * cos(orientation_pst)
        deltaY_pst = dist_correction * sin(orientation_pst)
    X_pst = X_measure + deltaX_pst
    Y_pst = Y_measure + deltaY_pst

    xy_estimate = (X_pst, Y_pst)
    OTHER = {'pos': measurement, 'orientation': orientation_measure, 'sum': dist_sum, 'num': num_measure,'orientation_sum':orientation_sum}
    # You must return xy_estimate (x, y), and OTHER (even if it is None)
    # in this order for grading purposes.
    #print "measure:", measurement
    #print "est:", xy_estimate
    #print "dist:", distance_between(measurement,xy_estimate)
    return xy_estimate, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
from math import *
from matrix import *
from robot import *
import random

    # This function will be called after each time the target moves. 
    # The OTHER variable is a place for you to store any historical 
    # information about the progress of the hunt (or maybe some 
    # localization information). Your must return a tuple of three 
    # values: turning, distance, OTHER

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):
    #Change these:

    xy_estimate, OTHER = estimate_next_pos(target_measurement, OTHER)
    heading_to_target = atan2(xy_estimate[1] - hunter_position[1], xy_estimate[0] - hunter_position[0])
    turning = angle_trunc(heading_to_target - hunter_heading)
    dist = distance_between(xy_estimate, hunter_position)
    if dist < max_distance:
        distance = dist
    else:
        distance = max_distance  # full speed ahead!

    return turning, distance, OTHER


def estimate_next_pos(measurement, OTHER=None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    X_measure = measurement[0]
    Y_measure = measurement[1]

    if not OTHER:  # this is the first measurement
        dist_sum = 0
        num_measure = 0
        deltaX_pst=0
        deltaY_pst=0
        orientation_measure=atan2(Y_measure, X_measure)

    else:
        pos_pre = OTHER['pos']
        orientation_pre = OTHER['orientation']
        dist_sum = OTHER['sum']
        num_measure = OTHER['num']

        X_pre = pos_pre[0]
        Y_pre = pos_pre[1]
        deltaX = X_measure - X_pre
        deltaY = Y_measure - Y_pre
        orientation_measure = atan2(deltaY, deltaX)
        angle_steer = orientation_measure - orientation_pre
        angle_steer %= 2 * pi  # make sure to normalize the angle

        # calculate the pst position and orientation using pre and measurement (assume distance the same)
        dist = distance_between(measurement, pos_pre)
        # normalize distances to obtain more realist distance by obtaining the mean of movements, also adding noise

        dist_sum = dist_sum + dist
        num_measure = num_measure + 1
        dist_correction = dist_sum / num_measure
        dist_correction = random.uniform(dist_correction - dist_correction * 0.05, dist_correction + dist_correction * 0.05)
        orientation_pst = orientation_measure + angle_steer  # assume steer the same amount
        deltaX_pst = dist_correction * cos(orientation_pst)
        deltaY_pst = dist_correction * sin(orientation_pst)
    X_pst = X_measure + deltaX_pst
    Y_pst = Y_measure + deltaY_pst

    xy_estimate = (X_pst, Y_pst)
    OTHER = {'pos': measurement, 'orientation': orientation_measure, 'sum': dist_sum, 'num': num_measure}
    # You must return xy_estimate (x, y), and OTHER (even if it is None)
    # in this order for grading purposes.
    # xy_estimate = (3.2, 9.1)
    return xy_estimate, OTHER
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi
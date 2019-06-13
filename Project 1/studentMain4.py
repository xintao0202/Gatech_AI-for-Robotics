from math import *
from matrix import *
from robot import *
import random

    # This function will be called after each time the target moves.
    # The OTHER variable is a place for you to store any historical
    # information about the progress of the hunt (or maybe some
    # localization information). Your must return a tuple of three
    # values: turning, distance, OTHER
def estimate_next_pos(measurement, hunter_position,OTHER=None):

    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    X_measure = measurement[0]
    Y_measure = measurement[1]
    if not OTHER:
        pos_pre = (0, 0)
        num_measure = 0
        dist_sum = 0
        orientation_sum = 0
        orientation_measure=atan2(Y_measure, X_measure)
        deltaX_pst=0
        deltaY_pst=0
        orientation_pst = atan2(Y_measure - hunter_position[1], X_measure - hunter_position[0])
        orientation_pre = orientation_measure

    else:
        num_measure = OTHER['num']
        pos_pre = OTHER['pos']
        orientation_pre = OTHER['orientation']
        dist_sum = OTHER['dist_sum']
        orientation_sum = OTHER['orientation_sum']

    X_pre = pos_pre[0]
    Y_pre = pos_pre[1]
    deltaX = X_measure - X_pre
    deltaY = Y_measure - Y_pre
    orientation_measure = atan2(deltaY, deltaX)


    angle_steer = orientation_measure - orientation_pre
    orientation_sum += angle_trunc(angle_steer)
    if num_measure <= 1:
        orientation_correction = 0
    else:
        orientation_correction = orientation_sum / (num_measure - 1)
    #orientation_correction = random.uniform(orientation_correction - orientation_correction * 0.025, orientation_correction + orientation_correction * 0.025)
    orientation_pst = orientation_measure + orientation_correction

    # calculate the pst position and orientation using pre and measurement (assume distance the same)
    dist = distance_between(measurement, pos_pre)

    # normalize distances to obtain more realist distance by obtaining the mean of movements, also adding noise
    num_measure = num_measure + 1
    dist_sum += dist
    dist_correction = dist_sum / num_measure
    dist_correction = random.uniform(dist_correction - dist_correction * 0.025, dist_correction + dist_correction * 0.025)
    #dist_correction=random.gauss(dist_correction,0.09)

    deltaX_pst = dist_correction * cos(orientation_pst)
    deltaY_pst = dist_correction * sin(orientation_pst)
    X_pst = X_measure + deltaX_pst
    Y_pst = Y_measure + deltaY_pst
    xy_estimate = (X_pst, Y_pst)

    OTHER = {'pos': measurement, 'orientation': orientation_measure, 'dist_sum': dist_sum, 'orientation_sum':orientation_sum,'num': num_measure,'last_orientation':orientation_pst}
    # You must return xy_estimate (x, y), and OTHER (even if it is None)
    # in this order for grading purposes.
    # xy_estimate = (3.2, 9.1)
    return xy_estimate, OTHER

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER=None):
    # This function will be called after each time the target moves.

    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.

    if OTHER is None:
        X_measure = target_measurement[0]
        Y_measure = target_measurement[1]
        RR_next_pos, OTHER = estimate_next_pos(target_measurement, hunter_position, OTHER)
        dist = distance_between(hunter_position, RR_next_pos)
        turning = atan2(Y_measure - hunter_position[1], X_measure - hunter_position[0])

    else:
        RR_next_pos, OTHER = estimate_next_pos(target_measurement,hunter_position, OTHER)

        RR_next_orientation =  OTHER['last_orientation']

        dist = distance_between(hunter_position, RR_next_pos)

        n = 0
        while (dist >= (n + 1) * max_distance):
            n += 1
            prev_X = RR_next_pos[0]
            prev_Y = RR_next_pos[1]
            RR_next_orientation += OTHER['orientation_sum'] / OTHER['num']
            current_X = prev_X +(OTHER['dist_sum'] / OTHER['num']) * cos(RR_next_orientation)
            current_Y = prev_Y + (OTHER['dist_sum'] / OTHER['num']) * sin(RR_next_orientation)
            RR_next_pos = (current_X, current_Y)
            dist = distance_between(hunter_position, RR_next_pos)

        turning = get_heading(hunter_position, RR_next_pos) - hunter_heading

    if dist > max_distance:
        dist = max_distance

    return turning, dist, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading
def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi
# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess 
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered 
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position. 
#
# ----------
# GRADING
# 
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.
import random
from numpy import *

# This is the function you have to write. Note that measurement is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    test_target = robot(2.1, 4.3, 0.5, 2 * pi / 34.0, 1.5)
    measurement_noise = 0.05 * test_target.distance
    test_target.set_noise(0.0, 0.0, measurement_noise)
    X_measure=measurement[0]
    Y_measure=measurement[1]
    
    
    if not OTHER: # this is the first measurement
        pos_pre = (random.random()*X_measure, random.random()*Y_measure) #in the format of (X,Y)
        orientation_pre=random.random()*2*pi
        dist_sum=0
        num_measure=0
         
    else:
        pos_pre=OTHER['pos']
        orientation_pre=OTHER['orientation']
        dist_sum=OTHER['sum']
        num_measure=OTHER['num'] 
    
    X_pre=pos_pre[0]
    Y_pre=pos_pre[1]
    deltaX=X_measure-X_pre
    deltaY=Y_measure-Y_pre 
    orientation_measure=atan2(deltaY,deltaX)
    angle_steer=orientation_measure-orientation_pre
    angle_steer%=2*pi # make sure to normalize the angle
    
    
    #calculate the pst position and orientation using pre and measurement (assume distance the same)
    dist=distance_between(measurement,pos_pre)
    # normalize distances to obtain more realist distance by obtaining the mean of movements, also adding noise
    dist_sum=dist_sum+dist
    num_measure=num_measure+1
    dist_correction=dist_sum/num_measure
    dist_correction=random.uniform(dist_correction-measurement_noise,dist_correction+measurement_noise)
    orientation_pst=orientation_measure+angle_steer #assume steer the same amount
    deltaX_pst=dist_correction*cos(orientation_pst)
    deltaY_pst=dist_correction*sin(orientation_pst)
    X_pst=X_measure+ deltaX_pst
    Y_pst=Y_measure+ deltaY_pst
    
    
    xy_estimate = (X_pst,Y_pst)
    OTHER={'pos':measurement, 'orientation':orientation_measure,'sum':dist_sum,'num':num_measure }
    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    #xy_estimate = (3.2, 9.1)
    return xy_estimate, OTHER

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want. 
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    while not localized and ctr <= 1000:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 1000:
            print "Sorry, it took you too many steps to localize the target."
    return localized

# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
# test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
# measurement_noise = 0.05 * test_target.distance
# test_target.set_noise(0.0, 0.0, measurement_noise)

#demo_grading(naive_next_pos, test_target)




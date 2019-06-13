# ----------
# Part Four
#
# Again, you'll track down and recover the runaway Traxbot.
# But this time, your speed will be about the same as the runaway bot.
# This may require more careful planning than you used last time.
#
# ----------
# YOUR JOB
#
# Complete the next_move function, similar to how you did last time.
#
# ----------
# GRADING
#
# Same as part 3. Again, try to catch the target in as few steps as possible.

from robot import *
from math import *
from matrix import *
import random


def estimate_next_pos(measurement, OTHER=None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    X_measure = measurement[0]
    Y_measure = measurement[1]

    if not OTHER:  # this is the first measurement
        pos_pre = (random.random() * X_measure, random.random() * Y_measure)  # in the format of (X,Y)
        orientation_pre = random.random() * 2 * pi
        dist_sum = 0
        num_measure = 0

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


def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER=None):
    # This function will be called after each time the target moves.
    # calculate where RR robot will move

    if not OTHER:
        OTHER_stop = 0
        xy_estimate, OTHER_estimate = estimate_next_pos(target_measurement, None)
    else:
        xy_estimate, OTHER_estimate = estimate_next_pos(target_measurement, OTHER['estimate'])
        dist = distance_between(xy_estimate, hunter_position)
        dist_RR = distance_between(xy_estimate, target_measurement)
        dist_Hunter = distance_between(hunter_position, target_measurement)
        heading_to_target2 = atan2(xy_estimate[1] - hunter_position[1], xy_estimate[0] - hunter_position[0])
        heading_difference2 = angle_trunc(heading_to_target2 - hunter_heading)
        # stop1 is to move for hunter to move 1 step ahead after stop to make is closer to the track of RR robot
        # stop2 is the final stop, the releasing condition is when the RR robot come closer.
        if OTHER['stop'] == 1:
            OTHER['stop'] = 2
            return 0, dist_Hunter, OTHER
        if OTHER['stop'] == 2:
            if ((dist - dist_RR) < dist_RR*2 and (dist - dist_RR) > 0 and max_distance > dist_RR) or \
                    ((dist_RR - dist) < dist_RR  and (dist - dist_RR) < 0 and max_distance < dist_RR):
                return heading_difference2, max(dist, max_distance), OTHER
            else:
                return 0, 0, OTHER

    heading_to_target = get_heading(hunter_position, xy_estimate)
    heading_difference = heading_to_target - hunter_heading
    heading_to_target2 = atan2(xy_estimate[1] - hunter_position[1], xy_estimate[0] - hunter_position[0])
    heading_difference2 = angle_trunc(heading_to_target2 - hunter_heading)
    turning = heading_difference  # turn towards the target
    dist = distance_between(xy_estimate, hunter_position)
    dist_RR = distance_between(xy_estimate, target_measurement)
    turning_RR = get_heading(target_measurement, xy_estimate)
    if turning < -pi/0.6  and abs(dist - dist_RR) < dist_RR*1.2:
        turning = 0
        OTHER_stop = 1
    else:
        OTHER_stop = 0

    if dist < max_distance:
        distance = dist
    else:
        distance = max_distance  # full speed ahead!
    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.

    OTHER = {'estimate': OTHER_estimate, 'stop': OTHER_stop}

    # print OTHER['stop']
    return heading_difference2, distance, OTHER


def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER=None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we
    will grade your submission."""
    max_distance = 0.98 * target_bot.distance  # 0.98 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance  # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0
    # For Visualization
    import turtle
    window = turtle.Screen()
    window.bgcolor('white')
    chaser_robot = turtle.Turtle()
    chaser_robot.shape('arrow')
    chaser_robot.color('blue')
    chaser_robot.resizemode('user')
    chaser_robot.shapesize(0.3, 0.3, 0.3)
    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.3, 0.3, 0.3)
    size_multiplier = 15.0  # change size of animation
    chaser_robot.hideturtle()
    chaser_robot.penup()
    chaser_robot.goto(hunter_bot.x * size_multiplier, hunter_bot.y * size_multiplier - 100)
    chaser_robot.showturtle()
    broken_robot.hideturtle()
    broken_robot.penup()
    broken_robot.goto(target_bot.x * size_multiplier, target_bot.y * size_multiplier - 100)
    broken_robot.showturtle()
    measuredbroken_robot = turtle.Turtle()
    measuredbroken_robot.shape('circle')
    measuredbroken_robot.color('red')
    measuredbroken_robot.penup()
    measuredbroken_robot.resizemode('user')
    measuredbroken_robot.shapesize(0.1, 0.1, 0.1)
    broken_robot.pendown()
    chaser_robot.pendown()
    # End of Visualization
    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:
        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        if separation < separation_tolerance:
            print "You got it right! It took you ", ctr, " steps to catch the target."
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance,
                                                 OTHER)

        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()
        # Visualize it
        measuredbroken_robot.setheading(target_bot.heading * 180 / pi)
        measuredbroken_robot.goto(target_measurement[0] * size_multiplier,
                                  target_measurement[1] * size_multiplier - 100)
        measuredbroken_robot.stamp()
        broken_robot.setheading(target_bot.heading * 180 / pi)
        broken_robot.goto(target_bot.x * size_multiplier, target_bot.y * size_multiplier - 100)
        chaser_robot.setheading(hunter_bot.heading * 180 / pi)
        chaser_robot.goto(hunter_bot.x * size_multiplier, hunter_bot.y * size_multiplier - 100)
        # End of visualization
        ctr += 1
        if ctr >= 1000:
            print "It took too many steps to catch the target."
    return caught


def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi


def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading


def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all
    the target measurements, hunter positions, and hunter headings over time, but it doesn't
    do anything with that information."""
    if not OTHER:  # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings)  # now I can keep track of history
    else:  # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER  # now I can always refer to these variables

    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning = heading_difference  # turn towards the target
    distance = max_distance  # full speed ahead!
    return turning, distance, OTHER

# target = robot(0.0, 10.0, 0.0, 2*pi / 30, 1.5)
# measurement_noise = .05*target.distance
# target.set_noise(0.0, 0.0, measurement_noise)
#
# hunter = robot(-10.0, -10.0, 0.0)
#
# print demo_grading(hunter, target, next_move)






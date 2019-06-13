#!/usr/bin/python

import math
import random
import robot
import sys

from functools import wraps
from Queue import Queue
from Queue import Empty as QueueEmptyError
from threading import Thread
from multiprocessing import TimeoutError

import unittest
import timeit

try:
    import studentMain1
except Exception as e:
    print "Error importing studentMain1:", e

try:
    import studentMain2
except Exception as e:
    print "Error importing studentMain2:", e

try:
    import studentMain3
except Exception as e:
    print "Error importing studentMain3:", e

try:
    import studentMain4
except Exception as e:
    print "Error importing studentMain4:", e


PI = math.pi

GLOBAL_SEEDS = [None, 
  None,
  'air_nomads',
  'water_tribes',
  'earth_kingdom',
  'fire_nation'
]

TIME_LIMIT = 5 # seconds

CREDIT_PER_PASS = 2.5 # points

GLOBAL_PARAMETERS = [None,

     {'test_case': 1,
     'target_x': -10.495402099,
     'target_y': -6.83265317961,
     'target_heading': -0.242728379915,
     'target_period': 4,
     'target_speed': 3.228570046,
     'target_line_length': 14,
     'hunter_x': -9.47802291015,
     'hunter_y': 13.778029331,
     'hunter_heading': 2.30637158245
    },
    {'test_case': 2,
     'target_x': 2.09139173822,
     'target_y': 9.14401638386,
     'target_heading': 0.330735695628,
     'target_period': 9,
     'target_speed': 3.00777784537,
     'target_line_length': 4,
     'hunter_x': -16.5542313216,
     'hunter_y': 18.1109745599,
     'hunter_heading': -2.7781543827
    },
    {'test_case': 3,
     'target_x': -2.51255394111,
     'target_y': -3.90992554461,
     'target_heading': 0.460561223754,
     'target_period': 11,
     'target_speed': 1.10250033762,
     'target_line_length': 10,
     'hunter_x': -9.41295379255,
     'hunter_y': 0.484148422171,
     'hunter_heading': 0.75225510408
    },
    {'test_case': 4,
     'target_x': 14.8970344385,
     'target_y': -13.7097014654,
     'target_heading': -0.433989101738,
     'target_period': 9,
     'target_speed': 2.24402954236,
     'target_line_length': 12,
     'hunter_x': -16.5747942537,
     'hunter_y': -17.6052857115,
     'hunter_heading': -1.50180394737
    },
    {'test_case': 5,
     'target_x': -2.18551374254,
     'target_y': 1.94826117535,
     'target_heading': -0.174300459841,
     'target_period': -10,
     'target_speed': 2.42996817664,
     'target_line_length': 13,
     'hunter_x': 6.45678335505,
     'hunter_y': 19.0914325093,
     'hunter_heading': 0.729514197775
    },
    {'test_case': 6,
     'target_x': -17.2475029545,
     'target_y': 5.24949093472,
     'target_heading': -1.19840826312,
     'target_period': 10,
     'target_speed': 1.67975491035,
     'target_line_length': 2,
     'hunter_x': -19.5902542896,
     'hunter_y': -15.0921351881,
     'hunter_heading': -1.30935571877
    },
    {'test_case': 7,
     'target_x': 7.84514997848,
     'target_y': -8.48597754822,
     'target_heading': -1.57169983156,
     'target_period': -11,
     'target_speed': 2.3757525123,
     'target_line_length': 5,
     'hunter_x': -11.9422205697,
     'hunter_y': 10.6381971738,
     'hunter_heading': -2.30566819863
    },
    {'test_case': 8,
     'target_x': -1.14112176327,
     'target_y': 3.02281227223,
     'target_heading': -0.664034955438,
     'target_period': 10,
     'target_speed': 1.49414008874,
     'target_line_length': 11,
     'hunter_x': 2.96449820717,
     'hunter_y': -7.25528868577,
     'hunter_heading': -1.65653130459
    },
    {'test_case': 9,
     'target_x': 1.52126945073,
     'target_y': -1.78534256949,
     'target_heading': -1.43273533745,
     'target_period': 11,
     'target_speed': 2.40006783335,
     'target_line_length': 4,
     'hunter_x': 13.9432845361,
     'hunter_y': -9.21340966185,
     'hunter_heading': -0.594707378927
    },
    {'test_case': 10,
     'target_x': 13.9184983584,
     'target_y': 3.08907778457,
     'target_heading': 1.98164525968,
     'target_period': 11,
     'target_speed': 3.72209876541,
     'target_line_length': 10,
     'hunter_x': 3.02604431353,
     'hunter_y': -7.88472145921,
     'hunter_heading': 2.96765705748
    },
    {'test_case': 11,
     'target_x': -1.87639847125,
     'target_y': -6.05897821398,
     'target_heading': 0.941047751978,
     'target_period': 3,
     'target_speed': 4.48576447022,
     'target_line_length': 12,
     'hunter_x': 1.28613924492,
     'hunter_y': -10.1856254731,
     'hunter_heading': 1.38964130707
    },
    {'test_case': 12,
     'target_x': -1.80093682558,
     'target_y': 19.5353103581,
     'target_heading': -2.07149187742,
     'target_period': 6,
     'target_speed': 3.30482491439,
     'target_line_length': 16,
     'hunter_x': 5.34106124269,
     'hunter_y': -10.45731767,
     'hunter_heading': -0.136004485901
    },
    {'test_case': 13,
     'target_x': 6.04653340408,
     'target_y': 0.939165715656,
     'target_heading': 1.76489737015,
     'target_period': -5,
     'target_speed': 3.2720839508,
     'target_line_length': 7,
     'hunter_x': -18.7928255191,
     'hunter_y': 1.28399373362,
     'hunter_heading': 1.09520268101
    },
    {'test_case': 14,
     'target_x': 10.2579035259,
     'target_y': -14.7965820121,
     'target_heading': -0.908115709585,
     'target_period': -3,
     'target_speed': 1.92406474044,
     'target_line_length': 6,
     'hunter_x': 7.23643425441,
     'hunter_y': 8.89942894119,
     'hunter_heading': -2.94045171545
    },
    {'test_case': 15,
     'target_x': -9.45463215079,
     'target_y': 10.7510126703,
     'target_heading': 2.08309789817,
     'target_period': 7,
     'target_speed': 4.85780578759,
     'target_line_length': 11,
     'hunter_x': 16.0113366486,
     'hunter_y': -12.0222629744,
     'hunter_heading': -1.29052903509
    },
    {'test_case': 16,
     'target_x': 16.9005383394,
     'target_y': 8.74357855186,
     'target_heading': 0.823428985198,
     'target_period': -3,
     'target_speed': 3.56671493966,
     'target_line_length': 8,
     'hunter_x': -0.917765623049,
     'hunter_y': 14.468049628,
     'hunter_heading': -2.81023208346
    },
    {'test_case': 17,
     'target_x': -2.90935392191,
     'target_y': 16.8272712144,
     'target_heading': 1.33761341963,
     'target_period': -4,
     'target_speed': 3.13820672394,
     'target_line_length': 9,
     'hunter_x': 9.28230588078,
     'hunter_y': -13.955916843,
     'hunter_heading': -1.46729795344
    },
    {'test_case': 18,
     'target_x': 4.25176721997,
     'target_y': 15.6806170301,
     'target_heading': -0.786472728235,
     'target_period': 8,
     'target_speed': 2.0997793277,
     'target_line_length': 11,
     'hunter_x': 11.7294267876,
     'hunter_y': 8.14362391964,
     'hunter_heading': -0.221676166136
    },
    {'test_case': 19,
     'target_x': 1.15321038003,
     'target_y': -10.9479385492,
     'target_heading': -1.48559462209,
     'target_period': 12,
     'target_speed': 1.25954302845,
     'target_line_length': 10,
     'hunter_x': -19.1235496805,
     'hunter_y': -5.74092338764,
     'hunter_heading': 2.50648135516
    },
    {'test_case': 20,
     'target_x': 3.36856739469,
     'target_y': -14.9518869748,
     'target_heading': 0.760249443132,
     'target_period': -4,
     'target_speed': 3.79794136626,
     'target_line_length': 5,
     'hunter_x': -1.37714850627,
     'hunter_y': 19.0824643889,
     'hunter_heading': 2.24718525245
    },
    {'test_case': 21,
     'target_x': 17.5978494187,
     'target_y': -2.48421820784,
     'target_heading': -1.89052541583,
     'target_period': 4,
     'target_speed': 1.41875030793,
     'target_line_length': 4,
     'hunter_x': 11.8553894323,
     'hunter_y': 9.7127425607,
     'hunter_heading': 1.19119027326
    },
    {'test_case': 22,
     'target_x': -18.7434431651,
     'target_y': -18.9370852471,
     'target_heading': 0.527365731783,
     'target_period': 8,
     'target_speed': 4.58588743631,
     'target_line_length': 16,
     'hunter_x': -11.0206724377,
     'hunter_y': 0.782488621764,
     'hunter_heading': -1.80881239955
    },
    {'test_case': 23,
     'target_x': -10.5454768949,
     'target_y': 6.863081344,
     'target_heading': 2.68653583642,
     'target_period': 11,
     'target_speed': 3.37318506439,
     'target_line_length': 14,
     'hunter_x': 10.4145874547,
     'hunter_y': -0.554474296616,
     'hunter_heading': 1.68648822302
    },
    {'test_case': 24,
     'target_x': -3.11480613908,
     'target_y': -12.8806307915,
     'target_heading': -1.2269962475,
     'target_period': -9,
     'target_speed': 2.52046208467,
     'target_line_length': 4,
     'hunter_x': 11.7494600423,
     'hunter_y': -0.270140997217,
     'hunter_heading': 1.11697066987
    },
    {'test_case': 25,
     'target_x': -14.2191682658,
     'target_y': 8.35492843482,
     'target_heading': -2.59879842494,
     'target_period': -10,
     'target_speed': 1.13069000674,
     'target_line_length': 9,
     'hunter_x': -19.1603136842,
     'hunter_y': 2.75779815495,
     'hunter_heading': -2.6851476499
    },
    {'test_case': 26,
     'target_x': 10.6866004865,
     'target_y': 1.95303367957,
     'target_heading': 0.56665920629,
     'target_period': 5,
     'target_speed': 2.74293953017,
     'target_line_length': 2,
     'hunter_x': -8.48941909688,
     'hunter_y': 4.5957159535,
     'hunter_heading': 1.56689678733
    },
    {'test_case': 27,
     'target_x': -14.8286404721,
     'target_y': -4.22484958398,
     'target_heading': 2.43920481825,
     'target_period': 3,
     'target_speed': 3.71534469875,
     'target_line_length': 11,
     'hunter_x': 18.3748957121,
     'hunter_y': -12.8796294509,
     'hunter_heading': -1.35215228729
    },
    {'test_case': 28,
     'target_x': -17.2582934274,
     'target_y': -3.62999516163,
     'target_heading': 1.2558238299,
     'target_period': 5,
     'target_speed': 1.20321271828,
     'target_line_length': 16,
     'hunter_x': 7.52883310332,
     'hunter_y': 15.635463335,
     'hunter_heading': -0.0816191019202
    },
    {'test_case': 29,
     'target_x': -8.63785263517,
     'target_y': -7.87887884834,
     'target_heading': 0.952833003194,
     'target_period': 12,
     'target_speed': 3.38921394751,
     'target_line_length': 14,
     'hunter_x': 19.2793316834,
     'hunter_y': 1.65657302581,
     'hunter_heading': -1.55905914022
    },
    {'test_case': 30,
     'target_x': -11.5088033556,
     'target_y': -5.19856615388,
     'target_heading': -1.887036971,
     'target_period': -12,
     'target_speed': 1.98486324009,
     'target_line_length': 15,
     'hunter_x': 10.9417554175,
     'hunter_y': 17.8135258191,
     'hunter_heading': -2.6593136243
    },
    {'test_case': 31,
     'target_x': -15.196445834,
     'target_y': 2.71333353914,
     'target_heading': -2.79018776296,
     'target_period': -11,
     'target_speed': 1.64385324544,
     'target_line_length': 1,
     'hunter_x': 3.70752909724,
     'hunter_y': 14.073716614,
     'hunter_heading': 0.983125443023
    },
    {'test_case': 32,
     'target_x': -0.115531320286,
     'target_y': 5.31465011634,
     'target_heading': 0.973908882235,
     'target_period': -12,
     'target_speed': 2.40070677729,
     'target_line_length': 14,
     'hunter_x': -10.4066247726,
     'hunter_y': 18.3900605597,
     'hunter_heading': -0.34268695742
    },
    {'test_case': 33,
     'target_x': -5.33469862609,
     'target_y': 3.54422074333,
     'target_heading': -0.547086712648,
     'target_period': 3,
     'target_speed': 1.14391719523,
     'target_line_length': 4,
     'hunter_x': -6.10104413876,
     'hunter_y': -16.159510731,
     'hunter_heading': 2.30778929729
    },
    {'test_case': 34,
     'target_x': -2.00285770814,
     'target_y': 12.1481446766,
     'target_heading': -0.497298962961,
     'target_period': -10,
     'target_speed': 3.70537552882,
     'target_line_length': 14,
     'hunter_x': -2.01561708851,
     'hunter_y': 5.75324630572,
     'hunter_heading': 0.129098313395
    },
    {'test_case': 35,
     'target_x': 7.00144227111,
     'target_y': -16.4687138709,
     'target_heading': 2.54817655103,
     'target_period': -8,
     'target_speed': 3.05821609726,
     'target_line_length': 15,
     'hunter_x': 15.6956130597,
     'hunter_y': 6.51998336374,
     'hunter_heading': 1.98902257094
    },
    {'test_case': 36,
     'target_x': 12.9954355701,
     'target_y': 15.3588225389,
     'target_heading': -1.99625986194,
     'target_period': -11,
     'target_speed': 2.92170166101,
     'target_line_length': 16,
     'hunter_x': -6.58519704121,
     'hunter_y': -15.5455096045,
     'hunter_heading': 1.31302753303
    },
    {'test_case': 37,
     'target_x': 9.59118748632,
     'target_y': -3.63783217366,
     'target_heading': -2.49711951001,
     'target_period': 9,
     'target_speed': 1.15923772424,
     'target_line_length': 11,
     'hunter_x': 10.4475298625,
     'hunter_y': 13.785647998,
     'hunter_heading': -0.778210601218
    },
    {'test_case': 38,
     'target_x': 14.305286914,
     'target_y': 17.380340861,
     'target_heading': -2.92557836701,
     'target_period': -11,
     'target_speed': 1.9919937826,
     'target_line_length': 6,
     'hunter_x': 16.0630753485,
     'hunter_y': 2.56838186056,
     'hunter_heading': 0.897329171303
    },
    {'test_case': 39,
     'target_x': 6.99457033118,
     'target_y': 17.0836657497,
     'target_heading': -1.07481915364,
     'target_period': 7,
     'target_speed': 3.53820360707,
     'target_line_length': 9,
     'hunter_x': 7.70618676942,
     'hunter_y': -1.13998237448,
     'hunter_heading': 0.158211398337
    },
    {'test_case': 40,
     'target_x': 16.5347904957,
     'target_y': -16.5936182981,
     'target_heading': 2.60588329416,
     'target_period': -11,
     'target_speed': 2.07472291796,
     'target_line_length': 6,
     'hunter_x': 13.1613561512,
     'hunter_y': -0.0560610481718,
     'hunter_heading': 1.07468585239
    },
     {'test_case': 41,
     'target_x': -13.3283935524,
     'target_y': 10.6731396024,
     'target_heading': -2.32434799764,
     'target_period': 7,
     'target_speed': 4.92974164215,
     'target_line_length': 6,
     'hunter_x': -18.9751194133,
     'hunter_y': 5.68045631327,
     'hunter_heading': 1.38263300172
    },
    {'test_case': 42,
     'target_x': -16.2272296623,
     'target_y': 9.34792850278,
     'target_heading': -2.62797088838,
     'target_period': -4,
     'target_speed': 2.24201591707,
     'target_line_length': 6,
     'hunter_x': -4.3840162146,
     'hunter_y': 17.7412101347,
     'hunter_heading': 0.482673996406
    },
    {'test_case': 43,
     'target_x': 13.7724093056,
     'target_y': 12.1019980168,
     'target_heading': -0.0355305878351,
     'target_period': -3,
     'target_speed': 1.23859768362,
     'target_line_length': 5,
     'hunter_x': 16.230357962,
     'hunter_y': 8.33013290851,
     'hunter_heading': 0.90866722162
    },
    {'test_case': 44,
     'target_x': 18.1331323499,
     'target_y': 2.00916948448,
     'target_heading': -0.950916807956,
     'target_period': 3,
     'target_speed': 1.82264429358,
     'target_line_length': 1,
     'hunter_x': -8.24880555695,
     'hunter_y': -7.47488511655,
     'hunter_heading': -2.05195839181
    },
    {'test_case': 45,
     'target_x': -7.98141512399,
     'target_y': 9.56538518873,
     'target_heading': -0.0128082551467,
     'target_period': 8,
     'target_speed': 3.32127694066,
     'target_line_length': 13,
     'hunter_x': 10.0771504046,
     'hunter_y': -10.2179294978,
     'hunter_heading': 0.833963127903
    },
    {'test_case': 46,
     'target_x': -4.22918560038,
     'target_y': -2.38361903802,
     'target_heading': -1.14154094473,
     'target_period': 4,
     'target_speed': 2.71677792293,
     'target_line_length': 14,
     'hunter_x': 2.96443166091,
     'hunter_y': -7.77441056703,
     'hunter_heading': 2.4054365831
    },
    {'test_case': 47,
     'target_x': 17.3839306106,
     'target_y': 1.8339394515,
     'target_heading': -0.924981970591,
     'target_period': 4,
     'target_speed': 4.29844092339,
     'target_line_length': 3,
     'hunter_x': -8.17702649356,
     'hunter_y': -1.26122887274,
     'hunter_heading': 0.24703786906
    },
    {'test_case': 48,
     'target_x': 13.3202100936,
     'target_y': -10.5465191416,
     'target_heading': 1.09010901464,
     'target_period': 5,
     'target_speed': 3.98255777674,
     'target_line_length': 4,
     'hunter_x': -9.40974197522,
     'hunter_y': 13.6046664535,
     'hunter_heading': -1.70375494583
    },
    {'test_case': 49,
     'target_x': -2.78252531507,
     'target_y': -7.47370197309,
     'target_heading': 1.19379416873,
     'target_period': 4,
     'target_speed': 3.8896306003,
     'target_line_length': 14,
     'hunter_x': -10.8021215467,
     'hunter_y': -10.2860200899,
     'hunter_heading': 2.84252524542
    },
    {'test_case': 50,
     'target_x': 13.866475305,
     'target_y': 5.60208953477,
     'target_heading': -1.21981819549,
     'target_period': 11,
     'target_speed': 2.20976934406,
     'target_line_length': 9,
     'hunter_x': 14.6738016851,
     'hunter_y': 13.1144266346,
     'hunter_heading': 1.21767220201
    },
    {'test_case': 51,
     'target_x': 6.38499511376,
     'target_y': -12.7408267953,
     'target_heading': 2.54851519341,
     'target_period': 5,
     'target_speed': 3.24523802061,
     'target_line_length': 8,
     'hunter_x': 11.9092925583,
     'hunter_y': 1.50886213766,
     'hunter_heading': 0.911664614115
    },
    {'test_case': 52,
     'target_x': 19.3781014433,
     'target_y': -7.22549005473,
     'target_heading': -2.27726116103,
     'target_period': 4,
     'target_speed': 3.16229625697,
     'target_line_length': 12,
     'hunter_x': -4.87141710364,
     'hunter_y': 8.60673139875,
     'hunter_heading': -2.35987939599
    },
    {'test_case': 53,
     'target_x': 14.4069686452,
     'target_y': -5.31615962604,
     'target_heading': -1.19050932683,
     'target_period': 8,
     'target_speed': 2.22988970768,
     'target_line_length': 6,
     'hunter_x': 0.15865747414,
     'hunter_y': 18.1182981697,
     'hunter_heading': 2.87448880009
    },
    {'test_case': 54,
     'target_x': -7.70698341743,
     'target_y': 12.0138662827,
     'target_heading': -0.448498965693,
     'target_period': -4,
     'target_speed': 4.01349358078,
     'target_line_length': 7,
     'hunter_x': 7.5841709358,
     'hunter_y': 7.86793598794,
     'hunter_heading': -0.894325011027
    },
    {'test_case': 55,
     'target_x': 4.55343391166,
     'target_y': -15.720616017,
     'target_heading': 2.04444504637,
     'target_period': -8,
     'target_speed': 4.83363921098,
     'target_line_length': 13,
     'hunter_x': -0.892536363406,
     'hunter_y': -0.751210077819,
     'hunter_heading': -2.65059863675
    },
    {'test_case': 56,
     'target_x': 9.60321024688,
     'target_y': -11.2331358438,
     'target_heading': -1.12980331998,
     'target_period': 5,
     'target_speed': 3.25750999535,
     'target_line_length': 15,
     'hunter_x': -12.3147752799,
     'hunter_y': 9.11119576181,
     'hunter_heading': -0.939597611789
    },
    {'test_case': 57,
     'target_x': 0.809755132114,
     'target_y': 19.4085575181,
     'target_heading': 1.18307368294,
     'target_period': 11,
     'target_speed': 2.79928340657,
     'target_line_length': 9,
     'hunter_x': 19.7148775653,
     'hunter_y': 14.0559901096,
     'hunter_heading': -1.8151239956
    },
    {'test_case': 58,
     'target_x': -5.7471903975,
     'target_y': -14.9329082125,
     'target_heading': -1.33534435825,
     'target_period': -7,
     'target_speed': 2.83252338676,
     'target_line_length': 9,
     'hunter_x': 15.3191242771,
     'hunter_y': 12.4469627925,
     'hunter_heading': -1.63870946994
    },
    {'test_case': 59,
     'target_x': 4.47185470023,
     'target_y': -19.2411423982,
     'target_heading': 0.93458566468,
     'target_period': -11,
     'target_speed': 4.84965281263,
     'target_line_length': 4,
     'hunter_x': 1.6096343904,
     'hunter_y': 10.8073347903,
     'hunter_heading': 1.126814957
    },
    {'test_case': 60,
     'target_x': 1.17077752757,
     'target_y': -15.9439334946,
     'target_heading': -0.662345296966,
     'target_period': 4,
     'target_speed': 3.55607489512,
     'target_line_length': 4,
     'hunter_x': 16.3373513642,
     'hunter_y': -7.25231023767,
     'hunter_heading': -2.32458201651
    },
    {'test_case': 61,
     'target_x': 8.69066920561,
     'target_y': 6.99973043899,
     'target_heading': 1.66093996029,
     'target_period': 4,
     'target_speed': 4.42713505182,
     'target_line_length': 11,
     'hunter_x': -11.9988747429,
     'hunter_y': -3.30767412809,
     'hunter_heading': 2.24690024032
    },
    {'test_case': 62,
     'target_x': -16.7823576734,
     'target_y': -0.25991766396,
     'target_heading': -1.77518223853,
     'target_period': 10,
     'target_speed': 3.88389985299,
     'target_line_length': 10,
     'hunter_x': -9.01967423202,
     'hunter_y': -2.88018222253,
     'hunter_heading': -3.02092018372
    },
    {'test_case': 63,
     'target_x': 16.2885771346,
     'target_y': -3.81493077104,
     'target_heading': 1.42453031681,
     'target_period': -5,
     'target_speed': 2.37819697505,
     'target_line_length': 8,
     'hunter_x': -9.08989142886,
     'hunter_y': -15.278924362,
     'hunter_heading': 1.40117408651
    },
    {'test_case': 64,
     'target_x': -19.8553181844,
     'target_y': 19.0229198986,
     'target_heading': -2.97433903192,
     'target_period': -12,
     'target_speed': 4.01135148835,
     'target_line_length': 8,
     'hunter_x': 1.03993042222,
     'hunter_y': 6.11870911516,
     'hunter_heading': -1.68693300382
    },
    {'test_case': 65,
     'target_x': 0.482895856625,
     'target_y': 11.6872414965,
     'target_heading': -2.99429554429,
     'target_period': -11,
     'target_speed': 3.21388653633,
     'target_line_length': 16,
     'hunter_x': 12.0492624576,
     'hunter_y': -13.8001584268,
     'hunter_heading': -1.69554803391
    },
    {'test_case': 66,
     'target_x': -1.74041802905,
     'target_y': -16.1089135267,
     'target_heading': -1.6769076834,
     'target_period': 6,
     'target_speed': 4.55107307323,
     'target_line_length': 3,
     'hunter_x': -12.5910719854,
     'hunter_y': 12.4403957676,
     'hunter_heading': -2.75925608089
    },
    {'test_case': 67,
     'target_x': -1.98108836971,
     'target_y': 3.00116341978,
     'target_heading': 0.936949997136,
     'target_period': 7,
     'target_speed': 1.32370584743,
     'target_line_length': 5,
     'hunter_x': -8.91020071256,
     'hunter_y': 6.45997817567,
     'hunter_heading': 0.646529871832
    },
    {'test_case': 68,
     'target_x': 17.6938366948,
     'target_y': 4.45593824067,
     'target_heading': -0.56826832439,
     'target_period': -5,
     'target_speed': 2.63418071763,
     'target_line_length': 2,
     'hunter_x': -17.1677224738,
     'hunter_y': 3.19215003757,
     'hunter_heading': 3.08970625204
    },
    {'test_case': 69,
     'target_x': 13.0199167812,
     'target_y': -13.6347982116,
     'target_heading': -1.44466787152,
     'target_period': 8,
     'target_speed': 4.94753358559,
     'target_line_length': 12,
     'hunter_x': -11.6983348053,
     'hunter_y': 5.59184764304,
     'hunter_heading': -1.96998515885
    },
    {'test_case': 70,
     'target_x': 6.31369130594,
     'target_y': -17.3704345266,
     'target_heading': -2.5615724723,
     'target_period': -4,
     'target_speed': 4.09324788796,
     'target_line_length': 8,
     'hunter_x': 15.5836406818,
     'hunter_y': 9.41698507998,
     'hunter_heading': -0.881772283191
    },
    {'test_case': 71,
     'target_x': -7.09855494057,
     'target_y': 15.6141366395,
     'target_heading': 2.31542660957,
     'target_period': -12,
     'target_speed': 3.8532809049,
     'target_line_length': 14,
     'hunter_x': -4.40218670284,
     'hunter_y': -19.3120123492,
     'hunter_heading': 1.94516546622
    },
    {'test_case': 72,
     'target_x': 12.7277642594,
     'target_y': 2.7783283049,
     'target_heading': 0.507725851875,
     'target_period': 11,
     'target_speed': 4.29240684182,
     'target_line_length': 12,
     'hunter_x': 6.3255519727,
     'hunter_y': -19.2524918606,
     'hunter_heading': -2.94892485133
    },
    {'test_case': 73,
     'target_x': -13.1570007743,
     'target_y': -18.7882712886,
     'target_heading': 2.64084722445,
     'target_period': 6,
     'target_speed': 4.75754754575,
     'target_line_length': 7,
     'hunter_x': 18.5704848203,
     'hunter_y': 7.43311240876,
     'hunter_heading': -0.163678438864
    },
    {'test_case': 74,
     'target_x': 17.996230829,
     'target_y': -11.3703205053,
     'target_heading': -1.8042149623,
     'target_period': -6,
     'target_speed': 2.21613083293,
     'target_line_length': 8,
     'hunter_x': 6.61462587229,
     'hunter_y': 17.9743908091,
     'hunter_heading': 0.921535913829
    },
    {'test_case': 75,
     'target_x': -4.8602654119,
     'target_y': -6.47196583174,
     'target_heading': 0.519948414317,
     'target_period': -4,
     'target_speed': 2.29843558461,
     'target_line_length': 9,
     'hunter_x': 3.37542962682,
     'hunter_y': 18.464109508,
     'hunter_heading': 1.79896906866
    },
    {'test_case': 76,
     'target_x': 4.17570599744,
     'target_y': -3.46615038349,
     'target_heading': 2.60865253105,
     'target_period': -8,
     'target_speed': 2.65508450982,
     'target_line_length': 4,
     'hunter_x': -1.24943385481,
     'hunter_y': 14.7814810384,
     'hunter_heading': 0.309136768685
    },
    {'test_case': 77,
     'target_x': 1.50860158503,
     'target_y': -19.0071899833,
     'target_heading': 0.309924085715,
     'target_period': 9,
     'target_speed': 4.25516403108,
     'target_line_length': 6,
     'hunter_x': -4.7810817278,
     'hunter_y': 5.61181637899,
     'hunter_heading': 0.991365014983
    },
    {'test_case': 78,
     'target_x': 15.9264026895,
     'target_y': -13.0760751179,
     'target_heading': 0.304506706321,
     'target_period': -9,
     'target_speed': 4.38140308676,
     'target_line_length': 13,
     'hunter_x': -2.69656137876,
     'hunter_y': 15.1884630524,
     'hunter_heading': -1.06742718371
    },
    {'test_case': 79,
     'target_x': -5.32805225601,
     'target_y': 13.2450555064,
     'target_heading': 2.52728176741,
     'target_period': 5,
     'target_speed': 1.68721743955,
     'target_line_length': 13,
     'hunter_x': -16.1378359233,
     'hunter_y': -8.28761316544,
     'hunter_heading': 0.681577524504
    },
    {'test_case': 80,
     'target_x': 9.27497102292,
     'target_y': 14.0989281655,
     'target_heading': -1.10074578804,
     'target_period': 4,
     'target_speed': 1.22394435623,
     'target_line_length': 13,
     'hunter_x': -6.05678201181,
     'hunter_y': 9.39055943591,
     'hunter_heading': 2.59583787496
    },
     {'test_case': 81,
     'target_x': 15.1342463247,
     'target_y': -15.7924362218,
     'target_heading': 1.28430413999,
     'target_period': -9,
     'target_speed': 1.23277557086,
     'target_line_length': 11,
     'hunter_x': 12.9761058739,
     'hunter_y': -8.00077482126,
     'hunter_heading': 1.02590216314
    },
    {'test_case': 82,
     'target_x': 11.8325087635,
     'target_y': 2.60707583627,
     'target_heading': -0.216034205564,
     'target_period': 9,
     'target_speed': 2.16749365924,
     'target_line_length': 3,
     'hunter_x': 19.8754333023,
     'hunter_y': -12.1120032271,
     'hunter_heading': -2.08319308667
    },
    {'test_case': 83,
     'target_x': -1.93675647317,
     'target_y': -8.04175963818,
     'target_heading': -2.54869489117,
     'target_period': 10,
     'target_speed': 2.60403495599,
     'target_line_length': 9,
     'hunter_x': 18.2456486943,
     'hunter_y': 2.65118585464,
     'hunter_heading': -1.24845383537
    },
    {'test_case': 84,
     'target_x': -19.3062515942,
     'target_y': -5.55193132032,
     'target_heading': -1.60067196008,
     'target_period': 10,
     'target_speed': 2.62393680794,
     'target_line_length': 10,
     'hunter_x': 6.68143929538,
     'hunter_y': 11.0269789129,
     'hunter_heading': 1.58583298147
    },
    {'test_case': 85,
     'target_x': -5.4505872048,
     'target_y': -16.6399321618,
     'target_heading': 2.90088586612,
     'target_period': -6,
     'target_speed': 2.5290182238,
     'target_line_length': 16,
     'hunter_x': -8.78188375673,
     'hunter_y': -4.14836570118,
     'hunter_heading': -2.24965309521
    },
    {'test_case': 86,
     'target_x': -9.04054188538,
     'target_y': -3.8459527848,
     'target_heading': -3.04813069096,
     'target_period': 9,
     'target_speed': 3.77388388619,
     'target_line_length': 4,
     'hunter_x': -19.3772546229,
     'hunter_y': -13.084701002,
     'hunter_heading': -0.608999157039
    },
    {'test_case': 87,
     'target_x': -15.9565845034,
     'target_y': 3.88560676119,
     'target_heading': 1.60207486309,
     'target_period': 6,
     'target_speed': 2.99403365698,
     'target_line_length': 15,
     'hunter_x': 9.63791728991,
     'hunter_y': 19.2209669264,
     'hunter_heading': -0.0338741023755
    },
    {'test_case': 88,
     'target_x': 4.75668417897,
     'target_y': -19.6398774671,
     'target_heading': -0.367723107319,
     'target_period': -10,
     'target_speed': 1.46387128172,
     'target_line_length': 10,
     'hunter_x': -9.37411710954,
     'hunter_y': 16.7906412866,
     'hunter_heading': -2.59660731002
    },
    {'test_case': 89,
     'target_x': -16.4650118172,
     'target_y': -13.9410100975,
     'target_heading': 2.94199533997,
     'target_period': 9,
     'target_speed': 4.61327578575,
     'target_line_length': 14,
     'hunter_x': -14.4743404615,
     'hunter_y': -0.242360958985,
     'hunter_heading': 1.83494479204
    },
    {'test_case': 90,
     'target_x': -8.45828357042,
     'target_y': -0.858353686468,
     'target_heading': 2.76407305379,
     'target_period': -10,
     'target_speed': 1.01352320327,
     'target_line_length': 1,
     'hunter_x': -9.99354468148,
     'hunter_y': 18.7499094295,
     'hunter_heading': 2.82748398308
    },
    {'test_case': 91,
     'target_x': 7.18902800012,
     'target_y': -2.13248808885,
     'target_heading': -1.98458171698,
     'target_period': 5,
     'target_speed': 3.1916418446,
     'target_line_length': 11,
     'hunter_x': 4.95308454256,
     'hunter_y': -0.822233351368,
     'hunter_heading': -0.893442278766
    },
    {'test_case': 92,
     'target_x': 7.79588379492,
     'target_y': 5.25104064309,
     'target_heading': 0.700996819998,
     'target_period': 4,
     'target_speed': 4.90512013339,
     'target_line_length': 4,
     'hunter_x': -6.28838953406,
     'hunter_y': -12.520187699,
     'hunter_heading': -1.80111977422
    },
    {'test_case': 93,
     'target_x': 0.283060836006,
     'target_y': -13.5244313093,
     'target_heading': 2.54917032693,
     'target_period': -4,
     'target_speed': 2.09734787558,
     'target_line_length': 5,
     'hunter_x': -3.47844569776,
     'hunter_y': -5.87179818806,
     'hunter_heading': -1.68820925472
    },
    {'test_case': 94,
     'target_x': -13.3727027889,
     'target_y': 17.9243626594,
     'target_heading': 2.72980363118,
     'target_period': 8,
     'target_speed': 4.20968744917,
     'target_line_length': 4,
     'hunter_x': -0.149783456037,
     'hunter_y': 16.4813991348,
     'hunter_heading': -3.12544655955
    },
    {'test_case': 95,
     'target_x': 6.55455147237,
     'target_y': 9.23929066296,
     'target_heading': -2.18326064392,
     'target_period': -6,
     'target_speed': 3.50309425846,
     'target_line_length': 12,
     'hunter_x': -7.19123072644,
     'hunter_y': -8.54299448148,
     'hunter_heading': -0.158722841074
    },
    {'test_case': 96,
     'target_x': 15.6189374326,
     'target_y': 7.64983572461,
     'target_heading': -1.3941641825,
     'target_period': -6,
     'target_speed': 4.62220812637,
     'target_line_length': 8,
     'hunter_x': -9.51363850393,
     'hunter_y': -16.9827879886,
     'hunter_heading': 1.83495142124
    },
    {'test_case': 97,
     'target_x': 0.414264846574,
     'target_y': -15.7051680825,
     'target_heading': 0.291083014626,
     'target_period': -11,
     'target_speed': 1.86522136177,
     'target_line_length': 5,
     'hunter_x': 4.48087658793,
     'hunter_y': 18.9723800325,
     'hunter_heading': 1.75051756715
    },
    {'test_case': 98,
     'target_x': 4.07486120407,
     'target_y': -8.00912364873,
     'target_heading': 2.17829828518,
     'target_period': -4,
     'target_speed': 1.49883974096,
     'target_line_length': 12,
     'hunter_x': 1.32811267194,
     'hunter_y': 8.49175269723,
     'hunter_heading': 1.7938379208
    },
    {'test_case': 99,
     'target_x': 1.43906544548,
     'target_y': -2.15558532549,
     'target_heading': -2.20443222935,
     'target_period': 10,
     'target_speed': 1.802906147,
     'target_line_length': 11,
     'hunter_x': -3.67218648273,
     'hunter_y': -2.40664763482,
     'hunter_heading': 2.06567663109
    },
    {'test_case': 100,
     'target_x': 5.98155838394,
     'target_y': -11.0196874434,
     'target_heading': 2.78968228718,
     'target_period': -11,
     'target_speed': 1.94088866952,
     'target_line_length': 2,
     'hunter_x': 5.99467120228,
     'hunter_y': -17.591944235,
     'hunter_heading': 3.03225306186
    },
]

NOT_FOUND = """
Part {}, Test Case {}, did not succeed within {} steps.
"""

def distance(p, q):
    x1, y1 = p
    x2, y2 = q

    dx = x2 - x1
    dy = y2 - y1

    return math.sqrt(dx**2 + dy**2)


def truncate_angle(t):
    return ((t+PI)%(2*PI)) - PI


# The functions curr_time_millis, handler, and timeout are taken from 
# http://github.com/udacity/artificial-intelligence/blob/master/build-a-game-playing-agent/agent_test.py
# as of January 14, 2016, at 11:55 UTC.
# Copyright 2016 Udacity
# A claim of fair use under the copyright laws of the United States is made for the use
# of this code because:
# - It is a limited excerpt of the code from the file listed above.
# - It serves an auxiliary purpose for the code from the file listed above.
# - The code is being used for a nonprofit, educational purpose.
# - The use does not negatively affect the market for Udacity's product.

def curr_time_millis():
    return 1000 * timeit.default_timer()


def handler(obj, testcase, queue):
    try:
        queue.put((None, testcase(obj)))
    except:
        queue.put((sys.exc_info(), None))


def timeout(time_limit):
    """
    Function decorator for unittest test cases to specify test case timeout.
    It is not safe to access system resources (e.g., files) within test
    cases wrapped by this timer.
    """

    def wrapUnitTest(testcase):

        @wraps(testcase)
        def testWrapper(self):

            queue = Queue()

            try:
                p = Thread(target=handler, args=(self, testcase, queue))
                p.daemon = True
                p.start()
                err, res = queue.get(timeout=time_limit)
                p.join()
                if err:
                    raise err[0], err[1], err[2]
                return res
            except QueueEmptyError:
                raise TimeoutError("Test aborted due to timeout. Test was " +
                    "expected to finish in fewer than {} second(s).".format(time_limit))

        return testWrapper

    return wrapUnitTest


# End Udacity code.


def simulate_without_hunter(params):

    estimate_next_pos = params['student_method']

    target = robot.robot(params['target_x'],
                         params['target_y'],
                         params['target_heading'],
                         2.0 * PI / params['target_period'],
                         params['target_speed'],
			 params['target_line_length'])
    target.set_noise(0.0,
                     0.0,
                     params['noise_ratio'] * params['target_speed'])

    tolerance = params['tolerance_ratio'] * target.distance
    other_info = None
    steps = 0

    random.seed(GLOBAL_SEEDS[params['part']])
    while steps < params['max_steps']:

        target_pos = (target.x, target.y)
        target_meas = target.sense()

        estimate, other_info = estimate_next_pos(target_meas, other_info)

        target.move_in_polygon()
        target_pos = (target.x, target.y)

        separation = distance(estimate, target_pos)
        if separation < tolerance:
            return True, steps

        steps += 1

    return False, steps


def simulate_with_hunter(params):

    next_move = params['student_method']

    target = robot.robot(params['target_x'],
                         params['target_y'],
                         params['target_heading'],
                         2.0 * PI / params['target_period'],
                         params['target_speed'],
	 		 params['target_line_length'])
    target.set_noise(0.0,
                     0.0,
                     params['noise_ratio'] * params['target_speed'])

    hunter = robot.robot(params['hunter_x'],
                         params['hunter_y'],
                         params['hunter_heading'])

    tolerance = params['tolerance_ratio'] * target.distance
    max_speed = params['speed_ratio'] * params['target_speed']
    other_info = None
    steps = 0
    
    random.seed(GLOBAL_SEEDS[params['part']])
    while steps < params['max_steps']:

        hunter_pos = (hunter.x, hunter.y)
        target_pos = (target.x, target.y)

        separation = distance(hunter_pos, target_pos)
        if separation < tolerance:
            return True, steps

        target_meas = target.sense()
        turn, dist, other_info = next_move(hunter_pos, hunter.heading, target_meas, max_speed, other_info)

        dist = min(dist, max_speed)
        dist = max(dist, 0)
        turn = truncate_angle(turn)

        hunter.move(turn, dist)
        target.move_in_polygon()

        steps += 1

    return False, steps


class GenericPartTestCase(unittest.TestCase):

    params = {}
    params['tolerance_ratio'] = 0.02

    def run_with_params(self, k):
        params = self.params.copy()
        params.update(GLOBAL_PARAMETERS[k]) # how to make k vary?
        found, steps = params['test_method'](params)
        self.assertTrue(found,
            NOT_FOUND.format(params['part'], params['test_case'], steps))

    @timeout(TIME_LIMIT)
    def test_case01(self):
        self.run_with_params(1)

    @timeout(TIME_LIMIT)
    def test_case02(self):
        self.run_with_params(2)

    @timeout(TIME_LIMIT)
    def test_case03(self):
        self.run_with_params(3)

    @timeout(TIME_LIMIT)
    def test_case04(self):
        self.run_with_params(4)

    @timeout(TIME_LIMIT)
    def test_case05(self):
        self.run_with_params(5)

    @timeout(TIME_LIMIT)
    def test_case06(self):
        self.run_with_params(6)

    @timeout(TIME_LIMIT)
    def test_case07(self):
        self.run_with_params(7)

    @timeout(TIME_LIMIT)
    def test_case08(self):
        self.run_with_params(8)

    @timeout(TIME_LIMIT)
    def test_case09(self):
        self.run_with_params(9)

    @timeout(TIME_LIMIT)
    def test_case10(self):
        self.run_with_params(10)
        
    def test_case11(self):
        self.run_with_params(11)

    @timeout(TIME_LIMIT)
    def test_case12(self):
        self.run_with_params(12)

    @timeout(TIME_LIMIT)
    def test_case13(self):
        self.run_with_params(13)

    @timeout(TIME_LIMIT)
    def test_case14(self):
        self.run_with_params(14)

    @timeout(TIME_LIMIT)
    def test_case15(self):
        self.run_with_params(15)

    @timeout(TIME_LIMIT)
    def test_case16(self):
        self.run_with_params(16)

    @timeout(TIME_LIMIT)
    def test_case17(self):
        self.run_with_params(17)

    @timeout(TIME_LIMIT)
    def test_case18(self):
        self.run_with_params(18)

    @timeout(TIME_LIMIT)
    def test_case19(self):
        self.run_with_params(19)

    @timeout(TIME_LIMIT)
    def test_case20(self):
        self.run_with_params(20)
        
    @timeout(TIME_LIMIT)
    def test_case21(self):
        self.run_with_params(21)

    @timeout(TIME_LIMIT)
    def test_case22(self):
        self.run_with_params(22)

    @timeout(TIME_LIMIT)
    def test_case23(self):
        self.run_with_params(23)

    @timeout(TIME_LIMIT)
    def test_case24(self):
        self.run_with_params(24)

    @timeout(TIME_LIMIT)
    def test_case25(self):
        self.run_with_params(25)

    @timeout(TIME_LIMIT)
    def test_case26(self):
        self.run_with_params(26)

    @timeout(TIME_LIMIT)
    def test_case27(self):
        self.run_with_params(27)

    @timeout(TIME_LIMIT)
    def test_case28(self):
        self.run_with_params(28)

    @timeout(TIME_LIMIT)
    def test_case29(self):
        self.run_with_params(29)

    @timeout(TIME_LIMIT)
    def test_case30(self):
        self.run_with_params(30)
        
    def test_case31(self):
        self.run_with_params(31)

    @timeout(TIME_LIMIT)
    def test_case32(self):
        self.run_with_params(32)

    @timeout(TIME_LIMIT)
    def test_case33(self):
        self.run_with_params(33)

    @timeout(TIME_LIMIT)
    def test_case34(self):
        self.run_with_params(34)

    @timeout(TIME_LIMIT)
    def test_case35(self):
        self.run_with_params(35)

    @timeout(TIME_LIMIT)
    def test_case36(self):
        self.run_with_params(36)

    @timeout(TIME_LIMIT)
    def test_case37(self):
        self.run_with_params(37)

    @timeout(TIME_LIMIT)
    def test_case38(self):
        self.run_with_params(38)

    @timeout(TIME_LIMIT)
    def test_case39(self):
        self.run_with_params(39)

    @timeout(TIME_LIMIT)
    def test_case40(self):
        self.run_with_params(40)
        
    @timeout(TIME_LIMIT)
    def test_case41(self):
        self.run_with_params(41)

    @timeout(TIME_LIMIT)
    def test_case42(self):
        self.run_with_params(42)

    @timeout(TIME_LIMIT)
    def test_case43(self):
        self.run_with_params(43)

    @timeout(TIME_LIMIT)
    def test_case44(self):
        self.run_with_params(44)

    @timeout(TIME_LIMIT)
    def test_case45(self):
        self.run_with_params(45)

    @timeout(TIME_LIMIT)
    def test_case46(self):
        self.run_with_params(46)

    @timeout(TIME_LIMIT)
    def test_case47(self):
        self.run_with_params(47)

    @timeout(TIME_LIMIT)
    def test_case48(self):
        self.run_with_params(48)

    @timeout(TIME_LIMIT)
    def test_case49(self):
        self.run_with_params(49)

    @timeout(TIME_LIMIT)
    def test_case50(self):
        self.run_with_params(50)
        
    def test_case51(self):
        self.run_with_params(51)

    @timeout(TIME_LIMIT)
    def test_case52(self):
        self.run_with_params(52)

    @timeout(TIME_LIMIT)
    def test_case53(self):
        self.run_with_params(53)

    @timeout(TIME_LIMIT)
    def test_case54(self):
        self.run_with_params(54)

    @timeout(TIME_LIMIT)
    def test_case55(self):
        self.run_with_params(55)

    @timeout(TIME_LIMIT)
    def test_case56(self):
        self.run_with_params(56)

    @timeout(TIME_LIMIT)
    def test_case57(self):
        self.run_with_params(57)

    @timeout(TIME_LIMIT)
    def test_case58(self):
        self.run_with_params(58)

    @timeout(TIME_LIMIT)
    def test_case59(self):
        self.run_with_params(59)

    @timeout(TIME_LIMIT)
    def test_case60(self):
        self.run_with_params(60)
        
    @timeout(TIME_LIMIT)
    def test_case61(self):
        self.run_with_params(61)

    @timeout(TIME_LIMIT)
    def test_case62(self):
        self.run_with_params(62)

    @timeout(TIME_LIMIT)
    def test_case63(self):
        self.run_with_params(63)

    @timeout(TIME_LIMIT)
    def test_case64(self):
        self.run_with_params(64)

    @timeout(TIME_LIMIT)
    def test_case65(self):
        self.run_with_params(65)

    @timeout(TIME_LIMIT)
    def test_case66(self):
        self.run_with_params(66)

    @timeout(TIME_LIMIT)
    def test_case67(self):
        self.run_with_params(67)

    @timeout(TIME_LIMIT)
    def test_case68(self):
        self.run_with_params(68)

    @timeout(TIME_LIMIT)
    def test_case69(self):
        self.run_with_params(69)

    @timeout(TIME_LIMIT)
    def test_case70(self):
        self.run_with_params(70)
        
    def test_case71(self):
        self.run_with_params(71)

    @timeout(TIME_LIMIT)
    def test_case72(self):
        self.run_with_params(72)

    @timeout(TIME_LIMIT)
    def test_case73(self):
        self.run_with_params(73)

    @timeout(TIME_LIMIT)
    def test_case74(self):
        self.run_with_params(74)

    @timeout(TIME_LIMIT)
    def test_case75(self):
        self.run_with_params(75)

    @timeout(TIME_LIMIT)
    def test_case76(self):
        self.run_with_params(76)

    @timeout(TIME_LIMIT)
    def test_case77(self):
        self.run_with_params(77)

    @timeout(TIME_LIMIT)
    def test_case78(self):
        self.run_with_params(78)

    @timeout(TIME_LIMIT)
    def test_case79(self):
        self.run_with_params(79)

    @timeout(TIME_LIMIT)
    def test_case80(self):
        self.run_with_params(80)
        
    def test_case81(self):
        self.run_with_params(81)

    @timeout(TIME_LIMIT)
    def test_case82(self):
        self.run_with_params(82)

    @timeout(TIME_LIMIT)
    def test_case83(self):
        self.run_with_params(83)

    @timeout(TIME_LIMIT)
    def test_case84(self):
        self.run_with_params(84)

    @timeout(TIME_LIMIT)
    def test_case85(self):
        self.run_with_params(85)

    @timeout(TIME_LIMIT)
    def test_case86(self):
        self.run_with_params(86)

    @timeout(TIME_LIMIT)
    def test_case87(self):
        self.run_with_params(87)

    @timeout(TIME_LIMIT)
    def test_case88(self):
        self.run_with_params(88)

    @timeout(TIME_LIMIT)
    def test_case89(self):
        self.run_with_params(89)

    @timeout(TIME_LIMIT)
    def test_case90(self):
        self.run_with_params(90)
        
    def test_case91(self):
        self.run_with_params(91)

    @timeout(TIME_LIMIT)
    def test_case92(self):
        self.run_with_params(92)

    @timeout(TIME_LIMIT)
    def test_case93(self):
        self.run_with_params(93)

    @timeout(TIME_LIMIT)
    def test_case94(self):
        self.run_with_params(94)

    @timeout(TIME_LIMIT)
    def test_case95(self):
        self.run_with_params(95)

    @timeout(TIME_LIMIT)
    def test_case96(self):
        self.run_with_params(96)

    @timeout(TIME_LIMIT)
    def test_case97(self):
        self.run_with_params(97)

    @timeout(TIME_LIMIT)
    def test_case98(self):
        self.run_with_params(98)

    @timeout(TIME_LIMIT)
    def test_case99(self):
        self.run_with_params(99)

    @timeout(TIME_LIMIT)
    def test_case100(self):
        self.run_with_params(100)

class Part1TestCase(GenericPartTestCase):
    def setUp(self):
        params = self.params
        params['part'] = 1
        params['method_name'] = 'estimate_next_pos'
        params['max_steps'] = 10
        params['noise_ratio'] = 0.00
        params['test_method'] = simulate_without_hunter
        params['student_method'] = studentMain1.estimate_next_pos


class Part2TestCase(GenericPartTestCase):
    def setUp(self):
        params = self.params
        params['part'] = 2
        params['method_name'] = 'estimate_next_pos'
        params['max_steps'] = 1000
        params['noise_ratio'] = 0.05
        params['test_method'] = simulate_without_hunter
        params['student_method'] = studentMain2.estimate_next_pos


class Part3TestCase(GenericPartTestCase):
    def setUp(self):
        params = self.params
        params['part'] = 3
        params['method_name'] = 'next_move'
        params['max_steps'] = 1000
        params['noise_ratio'] = 0.05
        params['speed_ratio'] = 2.00
        params['test_method'] = simulate_with_hunter
        params['student_method'] = studentMain3.next_move


class Part4TestCase(GenericPartTestCase):
    def setUp(self):
        params = self.params
        params['part'] = 4
        params['method_name'] = 'next_move'
        params['max_steps'] = 1000
        params['noise_ratio'] = 0.05
        params['speed_ratio'] = 0.99
        params['test_method'] = simulate_with_hunter
        params['student_method'] = studentMain4.next_move




suites = map(lambda x: unittest.TestSuite(unittest.TestLoader().loadTestsFromTestCase(x)), 
    [Part1TestCase, Part2TestCase, Part3TestCase, Part4TestCase ])

total_passes = 0

for i, suite in zip(range(1,1+len(suites)),suites):
    print "====================\nTests for Part {}:".format(i)

    result = unittest.TestResult()
    suite.run(result)

    for x in result.errors:
        print x[0], x[1]
    for x in result.failures:
        print x[0], x[1]

    num_errors = len(result.errors)
    num_fails = len(result.failures)
    num_passes = result.testsRun - num_errors - num_fails
    total_passes += num_passes

    print "Successes: {}\nFailures: {}\n".format(num_passes, num_errors + num_fails)

print "====================\nOverall Score: {}".format(total_passes * CREDIT_PER_PASS)

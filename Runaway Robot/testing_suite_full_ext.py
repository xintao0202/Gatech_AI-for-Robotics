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
     'target_x': 13.6568224501,
     'target_y': 14.4023678349,
     'target_heading': -2.82776999412,
     'target_period': -37,
     'target_speed': 4.08482465454,
     'hunter_x': -0.0469496632688,
     'hunter_y': -9.30126086342,
     'hunter_heading': 2.55343469214
    },
    {'test_case': 2,
     'target_x': 13.4832074173,
     'target_y': -6.87503250032,
     'target_heading': -0.793431161677,
     'target_period': -26,
     'target_speed': 2.88640926009,
     'hunter_x': 19.869969648,
     'hunter_y': -5.48438981241,
     'hunter_heading': -2.42358801611
    },
    {'test_case': 3,
     'target_x': -9.11413428656,
     'target_y': 16.9789414518,
     'target_heading': 2.71619375048,
     'target_period': -19,
     'target_speed': 1.73482178827,
     'hunter_x': 8.22515726814,
     'hunter_y': -11.3501578969,
     'hunter_heading': -0.486725440144
    },
    {'test_case': 4,
     'target_x': -18.864323032,
     'target_y': 9.57111863941,
     'target_heading': -1.25483297647,
     'target_period': 38,
     'target_speed': 3.67136859703,
     'hunter_x': 4.87521358582,
     'hunter_y': -13.1678826637,
     'hunter_heading': 0.580286985788
    },
    {'test_case': 5,
     'target_x': 14.3195369645,
     'target_y': 18.0041425452,
     'target_heading': -1.45248026058,
     'target_period': 34,
     'target_speed': 4.01310211223,
     'hunter_x': 18.1456664076,
     'hunter_y': -1.41723841307,
     'hunter_heading': -0.314506960786
    },
    {'test_case': 6,
     'target_x': -17.2196517275,
     'target_y': 9.58857740482,
     'target_heading': -1.25565190693,
     'target_period': 29,
     'target_speed': 1.62243701148,
     'hunter_x': 10.7129632765,
     'hunter_y': 1.44004771369,
     'hunter_heading': -1.75785084304
    },
    {'test_case': 7,
     'target_x': 14.8013910627,
     'target_y': -4.81159851423,
     'target_heading': -2.61957572946,
     'target_period': -45,
     'target_speed': 1.14667769133,
     'hunter_x': -2.70744503073,
     'hunter_y': 3.09345597867,
     'hunter_heading': -2.92358197972
    },
    {'test_case': 8,
     'target_x': -8.8511198177,
     'target_y': 10.3270309991,
     'target_heading': 2.56292430514,
     'target_period': -49,
     'target_speed': 2.38215139554,
     'hunter_x': 9.60268755736,
     'hunter_y': -2.99826550072,
     'hunter_heading': -1.65575626384
    },
    {'test_case': 9,
     'target_x': -1.45506477149,
     'target_y': -18.4395890585,
     'target_heading': -0.0927845062916,
     'target_period': 44,
     'target_speed': 2.59386936428,
     'hunter_x': -7.67903372928,
     'hunter_y': 11.2232807447,
     'hunter_heading': -1.26373476847
    },
    {'test_case': 10,
     'target_x': 14.5712512563,
     'target_y': -4.85438224109,
     'target_heading': 2.66178726857,
     'target_period': -44,
     'target_speed': 4.63841702821,
     'hunter_x': 9.02817658941,
     'hunter_y': 3.10387754464,
     'hunter_heading': -2.50782822443
    },
    {'test_case': 11,
     'target_x': 4.91792517026,
     'target_y': 19.3538393378,
     'target_heading': -2.13212404179,
     'target_period': -20,
     'target_speed': 4.45367528683,
     'hunter_x': -6.90670968804,
     'hunter_y': -19.5978058227,
     'hunter_heading': 2.74349279166
    },
    {'test_case': 12,
     'target_x': -12.3791631427,
     'target_y': -18.9163538687,
     'target_heading': -2.50083694141,
     'target_period': 35,
     'target_speed': 2.18532080034,
     'hunter_x': 6.61760559749,
     'hunter_y': 8.1376886556,
     'hunter_heading': 0.93301043632
    },
    {'test_case': 13,
     'target_x': -7.88761776556,
     'target_y': 15.8255541424,
     'target_heading': -1.23722794239,
     'target_period': 16,
     'target_speed': 1.06266848381,
     'hunter_x': 0.467859598394,
     'hunter_y': -17.1904378778,
     'hunter_heading': 2.65552676439
    },
    {'test_case': 14,
     'target_x': 14.0727924684,
     'target_y': 6.65051234265,
     'target_heading': -0.244996955677,
     'target_period': -13,
     'target_speed': 3.57886696977,
     'hunter_x': -18.5744673836,
     'hunter_y': -16.7588798192,
     'hunter_heading': 0.932915895909
    },
    {'test_case': 15,
     'target_x': -9.95075409225,
     'target_y': -2.88620134401,
     'target_heading': 1.2192483929,
     'target_period': -18,
     'target_speed': 3.78898910836,
     'hunter_x': 5.53061226619,
     'hunter_y': 1.02435286488,
     'hunter_heading': -2.39790511955
    },
    {'test_case': 16,
     'target_x': 11.7649698186,
     'target_y': 9.80820843108,
     'target_heading': 2.23664603744,
     'target_period': 14,
     'target_speed': 3.08602546435,
     'hunter_x': -3.25480541466,
     'hunter_y': -12.4270679961,
     'hunter_heading': -1.71033865466
    },
    {'test_case': 17,
     'target_x': -4.01346427345,
     'target_y': 12.5164408067,
     'target_heading': -1.47487434004,
     'target_period': 50,
     'target_speed': 3.63717385579,
     'hunter_x': -11.7606234037,
     'hunter_y': 15.8958000719,
     'hunter_heading': 1.99311665992
    },
    {'test_case': 18,
     'target_x': -19.5581000951,
     'target_y': 11.7137293995,
     'target_heading': -2.65954757724,
     'target_period': 12,
     'target_speed': 3.26091654379,
     'hunter_x': -14.461222138,
     'hunter_y': -17.3827098529,
     'hunter_heading': -2.10870003256
    },
    {'test_case': 19,
     'target_x': 13.9904384514,
     'target_y': 8.42630682611,
     'target_heading': 2.59314608929,
     'target_period': 23,
     'target_speed': 2.92170192022,
     'hunter_x': -0.629161708085,
     'hunter_y': 15.714360525,
     'hunter_heading': -2.38447505718
    },
    {'test_case': 20,
     'target_x': -8.91874039896,
     'target_y': 7.44859400922,
     'target_heading': -3.0483031243,
     'target_period': 19,
     'target_speed': 4.23594649535,
     'hunter_x': -1.10344516894,
     'hunter_y': 17.9404922021,
     'hunter_heading': -0.702632221711
    },
    {'test_case': 21,
     'target_x': 14.3154586331,
     'target_y': -3.9744321515,
     'target_heading': -3.03915721139,
     'target_period': -31,
     'target_speed': 1.80527205692,
     'hunter_x': 0.10900030228,
     'hunter_y': -10.3829439538,
     'hunter_heading': 0.0998454443029
    },
    {'test_case': 22,
     'target_x': -9.05872939696,
     'target_y': -7.25944156452,
     'target_heading': -0.935380824854,
     'target_period': -11,
     'target_speed': 1.79149542293,
     'hunter_x': 2.12779376392,
     'hunter_y': 17.5923131281,
     'hunter_heading': -1.68887749601
    },
    {'test_case': 23,
     'target_x': 19.4444730983,
     'target_y': -4.02016609813,
     'target_heading': 2.68616862437,
     'target_period': 39,
     'target_speed': 1.31945413275,
     'hunter_x': -12.2621526607,
     'hunter_y': -1.03720752838,
     'hunter_heading': 1.57880443941
    },
    {'test_case': 24,
     'target_x': -10.5955775405,
     'target_y': 10.4162492694,
     'target_heading': 2.92312148249,
     'target_period': 41,
     'target_speed': 4.55843920131,
     'hunter_x': -3.88218604036,
     'hunter_y': 3.80605021302,
     'hunter_heading': 1.30723498594
    },
    {'test_case': 25,
     'target_x': -13.3456313924,
     'target_y': 16.1750901818,
     'target_heading': -1.0973551627,
     'target_period': -13,
     'target_speed': 3.72573757162,
     'hunter_x': -12.7819766361,
     'hunter_y': -2.87818609605,
     'hunter_heading': 2.46951385986
    },
    {'test_case': 26,
     'target_x': 0.51849833448,
     'target_y': -2.18782880363,
     'target_heading': -0.156364548049,
     'target_period': 45,
     'target_speed': 3.77342510967,
     'hunter_x': -4.29874805577,
     'hunter_y': -9.1463518687,
     'hunter_heading': 1.09671229742
    },
    {'test_case': 27,
     'target_x': 16.0670492298,
     'target_y': -0.933185604958,
     'target_heading': 0.485809055165,
     'target_period': -43,
     'target_speed': 3.98829335791,
     'hunter_x': 12.1363187818,
     'hunter_y': -14.7906478063,
     'hunter_heading': 1.71691184813
    },
    {'test_case': 28,
     'target_x': 1.7971618304,
     'target_y': 14.2173299809,
     'target_heading': -0.920837315785,
     'target_period': 50,
     'target_speed': 1.6001095794,
     'hunter_x': 12.1228784364,
     'hunter_y': -1.85846002903,
     'hunter_heading': 1.6677060877
    },
    {'test_case': 29,
     'target_x': -9.50856238595,
     'target_y': -13.4435895536,
     'target_heading': -2.01195633317,
     'target_period': 16,
     'target_speed': 1.78335346086,
     'hunter_x': -4.5111604671,
     'hunter_y': -12.1919819423,
     'hunter_heading': -2.02340377476
    },
    {'test_case': 30,
     'target_x': -1.97420584848,
     'target_y': 10.790028882,
     'target_heading': -0.603054028597,
     'target_period': 45,
     'target_speed': 3.43460360336,
     'hunter_x': 5.2377820297,
     'hunter_y': -6.38655828773,
     'hunter_heading': -0.770211113465
    },
    {'test_case': 31,
     'target_x': -8.36447302897,
     'target_y': -11.0536293935,
     'target_heading': -0.845166197956,
     'target_period': 38,
     'target_speed': 1.09942098546,
     'hunter_x': 9.19260880727,
     'hunter_y': 18.1173486452,
     'hunter_heading': -1.14687320431
    },
    {'test_case': 32,
     'target_x': -7.29729428113,
     'target_y': 3.21401581066,
     'target_heading': 2.23122294416,
     'target_period': -39,
     'target_speed': 3.53470774592,
     'hunter_x': -6.2743597922,
     'hunter_y': -17.1846282847,
     'hunter_heading': -0.955984426076
    },
    {'test_case': 33,
     'target_x': 17.3696255069,
     'target_y': 8.09393757905,
     'target_heading': -2.49299812556,
     'target_period': 31,
     'target_speed': 2.94237023384,
     'hunter_x': -12.7506645133,
     'hunter_y': -17.3407905491,
     'hunter_heading': -1.49786773256
    },
    {'test_case': 34,
     'target_x': -1.50206568479,
     'target_y': 15.3965276096,
     'target_heading': 0.725020370102,
     'target_period': -11,
     'target_speed': 4.99813139368,
     'hunter_x': 7.94573880741,
     'hunter_y': 9.6849607538,
     'hunter_heading': -2.70197223534
    },
    {'test_case': 35,
     'target_x': -14.9330665393,
     'target_y': 7.37762474978,
     'target_heading': 2.17122596034,
     'target_period': -20,
     'target_speed': 1.33654175516,
     'hunter_x': 9.66812876669,
     'hunter_y': 12.1781718577,
     'hunter_heading': -0.282475150055
    },
    {'test_case': 36,
     'target_x': -8.8237719999,
     'target_y': 11.7266749278,
     'target_heading': 0.829484302493,
     'target_period': 18,
     'target_speed': 2.24103277865,
     'hunter_x': -7.76196359265,
     'hunter_y': 1.52740281735,
     'hunter_heading': 1.05360656527
    },
    {'test_case': 37,
     'target_x': 3.61584585628,
     'target_y': 12.5885007477,
     'target_heading': -0.0985892497274,
     'target_period': -32,
     'target_speed': 3.46942804354,
     'hunter_x': 2.17987301034,
     'hunter_y': 17.4101102176,
     'hunter_heading': -1.51615622384
    },
    {'test_case': 38,
     'target_x': -0.0631238278023,
     'target_y': 0.141068155894,
     'target_heading': -2.00718179275,
     'target_period': -50,
     'target_speed': 2.16599401967,
     'hunter_x': 2.22480938892,
     'hunter_y': 3.77202319056,
     'hunter_heading': -2.46221537261
    },
    {'test_case': 39,
     'target_x': -11.0488954012,
     'target_y': -8.14795534927,
     'target_heading': 1.3143709083,
     'target_period': -16,
     'target_speed': 4.62534149092,
     'hunter_x': -6.57520751687,
     'hunter_y': -8.26294381943,
     'hunter_heading': -2.70138411532
    },
    {'test_case': 40,
     'target_x': 9.35824575308,
     'target_y': -0.699518753043,
     'target_heading': 0.833587963249,
     'target_period': 34,
     'target_speed': 4.51770562266,
     'hunter_x': 13.306930574,
     'hunter_y': -12.6706859044,
     'hunter_heading': -2.11160380981
    },
     {'test_case': 41,
     'target_x': -14.0170301754,
     'target_y': 16.5634416556,
     'target_heading': 1.13092649878,
     'target_period': -17,
     'target_speed': 2.38617572065,
     'hunter_x': -6.80946876625,
     'hunter_y': 15.9398274171,
     'hunter_heading': -1.51943615685
    },
    {'test_case': 42,
     'target_x': -14.9360184446,
     'target_y': 6.60908532114,
     'target_heading': -0.870239903671,
     'target_period': 15,
     'target_speed': 2.86674368277,
     'hunter_x': -13.6342875145,
     'hunter_y': -11.9708329723,
     'hunter_heading': 0.217554825315
    },
    {'test_case': 43,
     'target_x': -12.8235580845,
     'target_y': 7.38471573541,
     'target_heading': 1.77187588212,
     'target_period': 23,
     'target_speed': 3.66698259223,
     'hunter_x': 9.85054517683,
     'hunter_y': -2.26727492984,
     'hunter_heading': 1.02243224932
    },
    {'test_case': 44,
     'target_x': -18.5039048984,
     'target_y': 4.95077558959,
     'target_heading': -0.919255005875,
     'target_period': -25,
     'target_speed': 4.98928885155,
     'hunter_x': 18.1734866952,
     'hunter_y': -8.79316232752,
     'hunter_heading': -2.25009698476
    },
    {'test_case': 45,
     'target_x': -15.9100071711,
     'target_y': -14.5424052371,
     'target_heading': -1.07617405493,
     'target_period': -10,
     'target_speed': 1.33727671309,
     'hunter_x': -2.89973380914,
     'hunter_y': 13.4589932782,
     'hunter_heading': -2.32017918484
    },
    {'test_case': 46,
     'target_x': 14.9522570569,
     'target_y': 10.1664981647,
     'target_heading': -1.61483911751,
     'target_period': -48,
     'target_speed': 2.19119980779,
     'hunter_x': -5.48635546256,
     'hunter_y': 14.3399858554,
     'hunter_heading': 2.91670343034
    },
    {'test_case': 47,
     'target_x': -10.3070945826,
     'target_y': -5.8014575057,
     'target_heading': -0.77004872082,
     'target_period': -25,
     'target_speed': 1.87384502668,
     'hunter_x': -10.8838045211,
     'hunter_y': 8.87588550776,
     'hunter_heading': 0.833806318721
    },
    {'test_case': 48,
     'target_x': 4.31093930596,
     'target_y': -12.2288347867,
     'target_heading': -0.39402948313,
     'target_period': -28,
     'target_speed': 4.59207114393,
     'hunter_x': -15.7107841143,
     'hunter_y': 19.7899028249,
     'hunter_heading': 2.80149859321
    },
    {'test_case': 49,
     'target_x': -6.0109884027,
     'target_y': -16.4837230876,
     'target_heading': -2.80232173562,
     'target_period': -25,
     'target_speed': 4.35551940931,
     'hunter_x': -0.780126397098,
     'hunter_y': -19.3936873434,
     'hunter_heading': 2.48629832601
    },
    {'test_case': 50,
     'target_x': -15.015366797,
     'target_y': -15.6343531001,
     'target_heading': 3.08988879958,
     'target_period': -37,
     'target_speed': 4.11496281859,
     'hunter_x': 13.5845295988,
     'hunter_y': 12.0824976192,
     'hunter_heading': 2.99201763319
    },
    {'test_case': 51,
     'target_x': -1.94482381856,
     'target_y': -16.0328563997,
     'target_heading': -2.47123404208,
     'target_period': 36,
     'target_speed': 1.97477854908,
     'hunter_x': -16.7971781311,
     'hunter_y': -16.0342511802,
     'hunter_heading': -0.0162179451526
    },
    {'test_case': 52,
     'target_x': 5.92351185281,
     'target_y': 15.9443430958,
     'target_heading': 1.62977949931,
     'target_period': -14,
     'target_speed': 4.54159802394,
     'hunter_x': -11.2565853517,
     'hunter_y': -10.5380389868,
     'hunter_heading': 1.25735614495
    },
    {'test_case': 53,
     'target_x': 10.6946667728,
     'target_y': 0.901951540619,
     'target_heading': 0.702994498937,
     'target_period': 47,
     'target_speed': 2.3345707251,
     'hunter_x': 14.2475951373,
     'hunter_y': 18.276174708,
     'hunter_heading': 0.859176618195
    },
    {'test_case': 54,
     'target_x': 1.50193081986,
     'target_y': -3.17472704831,
     'target_heading': -0.786305690684,
     'target_period': 38,
     'target_speed': 2.51433241574,
     'hunter_x': -17.2633893225,
     'hunter_y': 8.08790548274,
     'hunter_heading': -2.86177384165
    },
    {'test_case': 55,
     'target_x': 17.4999266276,
     'target_y': 11.6063314742,
     'target_heading': -1.24442721019,
     'target_period': 40,
     'target_speed': 1.67007873571,
     'hunter_x': 6.87011996684,
     'hunter_y': -6.41233633788,
     'hunter_heading': -2.39051371245
    },
    {'test_case': 56,
     'target_x': -17.7682543761,
     'target_y': -11.9080877055,
     'target_heading': -1.14076852887,
     'target_period': -46,
     'target_speed': 1.94186268627,
     'hunter_x': -13.478150087,
     'hunter_y': -13.6775608321,
     'hunter_heading': -1.49470498236
    },
    {'test_case': 57,
     'target_x': -6.34395877421,
     'target_y': -8.85148844664,
     'target_heading': -2.97234744273,
     'target_period': -41,
     'target_speed': 3.57521888404,
     'hunter_x': 16.4964247545,
     'hunter_y': 6.5554162647,
     'hunter_heading': -0.245528396038
    },
    {'test_case': 58,
     'target_x': 0.419245288491,
     'target_y': 11.8175531162,
     'target_heading': -2.81166174906,
     'target_period': -44,
     'target_speed': 3.45688489789,
     'hunter_x': 19.3739352446,
     'hunter_y': 10.0944697344,
     'hunter_heading': -0.150576454392
    },
    {'test_case': 59,
     'target_x': 19.5701321365,
     'target_y': -17.8098302104,
     'target_heading': 0.11510663887,
     'target_period': 11,
     'target_speed': 2.60237777216,
     'hunter_x': -15.066893514,
     'hunter_y': 8.27906380529,
     'hunter_heading': 0.516735763411
    },
    {'test_case': 60,
     'target_x': -11.8865232294,
     'target_y': 5.03825102495,
     'target_heading': -0.817381400418,
     'target_period': -24,
     'target_speed': 3.13959404349,
     'hunter_x': 13.2628862205,
     'hunter_y': 19.7497209339,
     'hunter_heading': -3.07823413487
    },
    {'test_case': 61,
     'target_x': -16.6583819871,
     'target_y': -1.39902799123,
     'target_heading': -1.17724429111,
     'target_period': 20,
     'target_speed': 2.19171980485,
     'hunter_x': 1.78787995119,
     'hunter_y': -10.213986832,
     'hunter_heading': 0.487538494712
    },
    {'test_case': 62,
     'target_x': -18.2097833999,
     'target_y': 7.7357362261,
     'target_heading': 0.214535565345,
     'target_period': 39,
     'target_speed': 2.19777004173,
     'hunter_x': -18.5541562603,
     'hunter_y': 18.6794004447,
     'hunter_heading': -1.49503361941
    },
    {'test_case': 63,
     'target_x': -6.70971967133,
     'target_y': 17.3341433276,
     'target_heading': 0.091821389916,
     'target_period': 17,
     'target_speed': 3.11980266129,
     'hunter_x': 18.8372897555,
     'hunter_y': 7.37214587811,
     'hunter_heading': -1.88174191704
    },
    {'test_case': 64,
     'target_x': 19.1287409839,
     'target_y': -7.53664223791,
     'target_heading': -0.220124233402,
     'target_period': -16,
     'target_speed': 3.66024193098,
     'hunter_x': -4.49743063092,
     'hunter_y': -19.1260089724,
     'hunter_heading': -2.45903575391
    },
    {'test_case': 65,
     'target_x': -17.5923354221,
     'target_y': 15.0743538752,
     'target_heading': -2.36273703412,
     'target_period': 33,
     'target_speed': 1.68907843729,
     'hunter_x': 18.139089585,
     'hunter_y': 5.16534422703,
     'hunter_heading': -0.0597301297424
    },
    {'test_case': 66,
     'target_x': 19.3268342024,
     'target_y': -17.1147254888,
     'target_heading': -0.737523434537,
     'target_period': -13,
     'target_speed': 2.16597167429,
     'hunter_x': -5.20298816044,
     'hunter_y': 2.50626957226,
     'hunter_heading': -1.55424829354
    },
    {'test_case': 67,
     'target_x': 16.874715699,
     'target_y': 18.4758730659,
     'target_heading': 0.471783727402,
     'target_period': -12,
     'target_speed': 1.66802858315,
     'hunter_x': -0.83718437873,
     'hunter_y': 1.00410753006,
     'hunter_heading': 0.25727647133
    },
    {'test_case': 68,
     'target_x': 19.8340969863,
     'target_y': 1.54147162888,
     'target_heading': 1.93448856166,
     'target_period': -11,
     'target_speed': 2.04560678452,
     'hunter_x': -5.21066037785,
     'hunter_y': -10.2590141322,
     'hunter_heading': -0.413645890553
    },
    {'test_case': 69,
     'target_x': 3.26395927762,
     'target_y': 14.6213330423,
     'target_heading': 1.94508810198,
     'target_period': -48,
     'target_speed': 2.60012235569,
     'hunter_x': -17.6822446655,
     'hunter_y': 13.7949629795,
     'hunter_heading': -1.95999473707
    },
    {'test_case': 70,
     'target_x': -19.3889354573,
     'target_y': 9.08982062419,
     'target_heading': -0.991901864837,
     'target_period': -19,
     'target_speed': 4.53172126322,
     'hunter_x': 14.0599021771,
     'hunter_y': -1.80206510673,
     'hunter_heading': -0.978687972363
    },
    {'test_case': 71,
     'target_x': -11.3753669085,
     'target_y': 16.7287386091,
     'target_heading': -2.35378078624,
     'target_period': -36,
     'target_speed': 4.57035602934,
     'hunter_x': 13.329220663,
     'hunter_y': -18.2180738187,
     'hunter_heading': -0.0377442825299
    },
    {'test_case': 72,
     'target_x': 6.87808783317,
     'target_y': -14.2756839771,
     'target_heading': -1.62132218551,
     'target_period': -17,
     'target_speed': 2.13030349488,
     'hunter_x': 15.0211912394,
     'hunter_y': -4.69005569372,
     'hunter_heading': 1.78696116489
    },
    {'test_case': 73,
     'target_x': -17.4036440874,
     'target_y': 15.4880856979,
     'target_heading': -2.27604180565,
     'target_period': 49,
     'target_speed': 1.39630506627,
     'hunter_x': -18.7695329737,
     'hunter_y': -7.91880017675,
     'hunter_heading': -2.67644890501
    },
    {'test_case': 74,
     'target_x': 19.8633499796,
     'target_y': -2.14470525488,
     'target_heading': -0.0562786098159,
     'target_period': -45,
     'target_speed': 4.79079487451,
     'hunter_x': -13.561235043,
     'hunter_y': -19.9024654238,
     'hunter_heading': 0.190914347757
    },
    {'test_case': 75,
     'target_x': -0.675117385336,
     'target_y': -19.6698660905,
     'target_heading': 3.05817460934,
     'target_period': 45,
     'target_speed': 4.58557941497,
     'hunter_x': 8.44548087051,
     'hunter_y': -1.73451988719,
     'hunter_heading': 2.96269712611
    },
    {'test_case': 76,
     'target_x': -10.5269888204,
     'target_y': 15.140430447,
     'target_heading': -2.14881069388,
     'target_period': 45,
     'target_speed': 3.24146247393,
     'hunter_x': 5.1744704197,
     'hunter_y': 15.4153864957,
     'hunter_heading': 2.51559915268
    },
    {'test_case': 77,
     'target_x': 17.5338332736,
     'target_y': 12.9165753794,
     'target_heading': 2.29927715142,
     'target_period': 37,
     'target_speed': 4.05151377683,
     'hunter_x': -13.6628164777,
     'hunter_y': 8.9681361975,
     'hunter_heading': 1.39853388037
    },
    {'test_case': 78,
     'target_x': 1.38022617376,
     'target_y': -19.3996253747,
     'target_heading': 1.09595308827,
     'target_period': -18,
     'target_speed': 3.74374164659,
     'hunter_x': 5.08499048494,
     'hunter_y': 4.51474766481,
     'hunter_heading': 1.02884793299
    },
    {'test_case': 79,
     'target_x': -9.13467356035,
     'target_y': 6.39536606175,
     'target_heading': -1.14758212485,
     'target_period': 15,
     'target_speed': 3.34169195171,
     'hunter_x': -0.145062413866,
     'hunter_y': 1.15780943027,
     'hunter_heading': 2.93844170148
    },
    {'test_case': 80,
     'target_x': -19.2791802096,
     'target_y': -16.9677536373,
     'target_heading': 3.04265020741,
     'target_period': -27,
     'target_speed': 3.6910858954,
     'hunter_x': 17.320156382,
     'hunter_y': -12.4201356987,
     'hunter_heading': -1.71626839217
    },
     {'test_case': 81,
     'target_x': -1.93669908086,
     'target_y': 1.2654831351,
     'target_heading': 1.41112965604,
     'target_period': 39,
     'target_speed': 1.54414886338,
     'hunter_x': -0.734682570933,
     'hunter_y': -8.15382822389,
     'hunter_heading': 1.29301278789
    },
    {'test_case': 82,
     'target_x': 13.7616569736,
     'target_y': -6.03873882869,
     'target_heading': 1.25630664895,
     'target_period': -30,
     'target_speed': 3.68770567351,
     'hunter_x': 3.32878532977,
     'hunter_y': 14.0143052552,
     'hunter_heading': -1.87005896214
    },
    {'test_case': 83,
     'target_x': 0.614819895863,
     'target_y': 10.646382879,
     'target_heading': -0.0927757229437,
     'target_period': 42,
     'target_speed': 1.30485798379,
     'hunter_x': -0.414791183753,
     'hunter_y': -0.000758094440322,
     'hunter_heading': 2.19110848976
    },
    {'test_case': 84,
     'target_x': -1.07060768254,
     'target_y': -1.34423182126,
     'target_heading': -2.37084449319,
     'target_period': 49,
     'target_speed': 1.54461338195,
     'hunter_x': -6.35641812102,
     'hunter_y': -1.90246650744,
     'hunter_heading': -1.81762405132
    },
    {'test_case': 85,
     'target_x': -2.15496927696,
     'target_y': -16.3418109244,
     'target_heading': 2.43427985668,
     'target_period': 49,
     'target_speed': 1.20970532432,
     'hunter_x': 8.55587875637,
     'hunter_y': -16.1093111677,
     'hunter_heading': -1.60387889776
    },
    {'test_case': 86,
     'target_x': -14.6742487702,
     'target_y': 18.1056453987,
     'target_heading': 0.160870108379,
     'target_period': -31,
     'target_speed': 2.75533807324,
     'hunter_x': -0.339101315207,
     'hunter_y': -16.013616351,
     'hunter_heading': -2.58998546802
    },
    {'test_case': 87,
     'target_x': -16.3835114527,
     'target_y': 16.9345305183,
     'target_heading': -0.0143307771328,
     'target_period': 29,
     'target_speed': 3.66653891278,
     'hunter_x': 12.797214656,
     'hunter_y': 10.5067058486,
     'hunter_heading': -2.26495461567
    },
    {'test_case': 88,
     'target_x': -16.7364124843,
     'target_y': 8.08220955618,
     'target_heading': 2.08134087043,
     'target_period': 40,
     'target_speed': 1.89273568247,
     'hunter_x': -0.709323233106,
     'hunter_y': -17.8307764286,
     'hunter_heading': 1.50830002036
    },
    {'test_case': 89,
     'target_x': 2.07332867594,
     'target_y': -3.9763796579,
     'target_heading': -1.6628547582,
     'target_period': -20,
     'target_speed': 2.80928405705,
     'hunter_x': -1.3999184567,
     'hunter_y': 0.319981239243,
     'hunter_heading': -2.40113545403
    },
    {'test_case': 90,
     'target_x': -7.9625173076,
     'target_y': -0.249457185755,
     'target_heading': -2.67098599181,
     'target_period': -30,
     'target_speed': 3.69825012122,
     'hunter_x': -4.69395354245,
     'hunter_y': -16.2723058661,
     'hunter_heading': 2.4995115576
    },
    {'test_case': 91,
     'target_x': -9.06337452623,
     'target_y': 10.8972453823,
     'target_heading': -1.04542550423,
     'target_period': -13,
     'target_speed': 2.09030635957,
     'hunter_x': -6.26465387072,
     'hunter_y': -3.32336852286,
     'hunter_heading': 2.84974240448
    },
    {'test_case': 92,
     'target_x': -12.4428254327,
     'target_y': 17.0161950574,
     'target_heading': 2.08775124632,
     'target_period': 26,
     'target_speed': 3.72196893343,
     'hunter_x': 9.37792729864,
     'hunter_y': 8.60995766876,
     'hunter_heading': 2.88147583883
    },
    {'test_case': 93,
     'target_x': 6.80283473851,
     'target_y': -17.1986813863,
     'target_heading': -0.239509798745,
     'target_period': 31,
     'target_speed': 4.05272862117,
     'hunter_x': 12.8858681257,
     'hunter_y': 18.8965325963,
     'hunter_heading': 1.67816144993
    },
    {'test_case': 94,
     'target_x': -17.5761182726,
     'target_y': -13.9441395936,
     'target_heading': -2.3722231945,
     'target_period': -49,
     'target_speed': 1.12201662638,
     'hunter_x': -4.24847349583,
     'hunter_y': 15.2545859397,
     'hunter_heading': 1.08750381026
    },
    {'test_case': 95,
     'target_x': -13.5746677464,
     'target_y': 10.9201401287,
     'target_heading': 0.385958969985,
     'target_period': -30,
     'target_speed': 2.13638196366,
     'hunter_x': 15.5739565094,
     'hunter_y': -15.4143562256,
     'hunter_heading': -1.84967605092
    },
    {'test_case': 96,
     'target_x': 7.7902542991,
     'target_y': 12.9977310664,
     'target_heading': 2.12559124698,
     'target_period': 41,
     'target_speed': 1.505777601,
     'hunter_x': -5.5719556752,
     'hunter_y': -15.9045098421,
     'hunter_heading': -1.75196325921
    },
    {'test_case': 97,
     'target_x': 10.3317185653,
     'target_y': -18.6198362772,
     'target_heading': 0.567168809118,
     'target_period': -40,
     'target_speed': 4.21304478025,
     'hunter_x': -12.2002001677,
     'hunter_y': -2.30665633756,
     'hunter_heading': 2.19404554603
    },
    {'test_case': 98,
     'target_x': -12.22231669,
     'target_y': 11.4220661569,
     'target_heading': -1.58249346985,
     'target_period': 28,
     'target_speed': 1.8306655959,
     'hunter_x': -7.51243494915,
     'hunter_y': 2.23019430498,
     'hunter_heading': 0.628224211491
    },
    {'test_case': 99,
     'target_x': 2.03313903085,
     'target_y': -9.19424836056,
     'target_heading': -2.43450129637,
     'target_period': 40,
     'target_speed': 1.74850902006,
     'hunter_x': 0.483330891212,
     'hunter_y': -11.901677524,
     'hunter_heading': 1.61178042683
    },
    {'test_case': 100,
     'target_x': -10.527249217,
     'target_y': 10.8045881219,
     'target_heading': -0.579106527897,
     'target_period': -50,
     'target_speed': 2.51665566043,
     'hunter_x': -2.46761249173,
     'hunter_y': -1.71790230049,
     'hunter_heading': -1.33697699526
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
                         params['target_speed'])
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

        target.move_in_circle()
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
                         params['target_speed'])
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
        target.move_in_circle()

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

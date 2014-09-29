#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Retrieve the maximum timestamp for the data present in the given top level path.

Usage:

    getMaxTimeForPath.py --basepath ${PATH}

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart-Grid' \
              '-PV-Inverter/master/BSD-LICENSE.txt'

import argparse
from si_data_util import SIDataUtil
from si_util import SIUtil
from datetime import datetime

COMMAND_LINE_ARGS = None

def processCommandLineArguments():
    """
    Create command line arguments and parse them.
    """

    global COMMAND_LINE_ARGS
    parser = argparse.ArgumentParser(
        description = 'Perform insertion of data contained in multiple files '
                      'to the SI database.')
    parser.add_argument('--basepath', required = True,
                        help = 'A base path from which to process data files.')
    COMMAND_LINE_ARGS = parser.parse_args()


if __name__ == '__main__':
    processCommandLineArguments()
    siUtil = SIUtil()
    dataUtil = SIDataUtil()
    paths = siUtil.pathsToProcess(COMMAND_LINE_ARGS.basepath)
    maxTimes = []
    for p in paths:
        maxTimes.append(dataUtil.maxTimeStamp(p))

    max = datetime(1900, 1, 1)

    for t in maxTimes:
        if type(t) == type(max):
            if t > max:
                max = t

    print "max: {}".format(max)

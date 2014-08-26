#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Insert multiple data files of meter data by recursively locating available files.

Usage:

    insertMultiMeterDataFile.py --basepath ${PATH}

The naming of this script is unusual on purpose to be consistent with the
single file version.

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart-Grid' \
              '-PV-Inverter/master/BSD-LICENSE.txt'

from sek.logger import SEKLogger
import argparse
from insertSingleMeterDataFile import SingleFileLoader
import multiprocessing
import sys
from si_util import SIUtil


COMMAND_LINE_ARGS = None
MULTIPROCESSING_LIMIT = 6


def processCommandLineArguments():
    """
    Create command line arguments and parse them.
    """

    global COMMAND_LINE_ARGS
    parser = argparse.ArgumentParser(
        description = 'Perform insertion of data contained in multiple files to the SI database.')
    parser.add_argument('--basepath', help = 'A base path from which to process data files.')
    COMMAND_LINE_ARGS = parser.parse_args()


if __name__ == '__main__':
    logger = SEKLogger(__name__, 'debug')
    siUtil = SIUtil()
    processCommandLineArguments()


    paths = siUtil.pathsToProcess(COMMAND_LINE_ARGS.basepath)
    lenPaths = len(paths)
    finCnt = 0 # finished loading file count
    rowCnt = 0
    assert len(paths) >= 1


    def makeMeters():
        for name in siUtil.meters():
            logger.log('Loading multi files for meter name {}.'.format(
                SingleFileLoader().getMeterID(name)))


    def insertData(x):
        global finCnt
        global lenPaths
        logger.log('process {}'.format(str(multiprocessing.current_process())))
        # logger.log('loading {} out of {}'.format(paths.index(x), lenPaths))
        SingleFileLoader(x).insertDataFromFile()
        finCnt += 1
        logger.log('finished loading {}, total finished {}/{}'.format(x, finCnt,
                                                                      lenPaths),
                   'debug')

    makeMeters()

    # pool = multiprocessing.Pool(MULTIPROCESSING_LIMIT)
    # results = pool.map(insertData, paths)
    # pool.close()
    # pool.join()

    # Single core:
    for p in paths:
        rowCnt += SingleFileLoader(p).insertDataFromFile()
        finCnt += 1
        logger.log('finished loading {}, total finished {}/{}'.format(p, finCnt,
                                                                      lenPaths),
                   'debug')

    logger.log('row cnt {}'.format(rowCnt))


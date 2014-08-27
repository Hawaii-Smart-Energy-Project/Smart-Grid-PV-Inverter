#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Insert multiple data files of meter data by recursively locating available
files.

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
import re


COMMAND_LINE_ARGS = None
MULTIPROCESSING_LIMIT = 6
MULTICORE = True

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


def worker(path, returnDict):
    """
    This is a multiprocessing worker for inserting data.

    :param path: A path containing data to be inserted.
    :param returnDict: Process results, in the form of a log, are returned to
    the caller via this dictionary during multiprocessing.
    """

    result = SingleFileLoader(path).insertDataFromFile()
    pattern = 'Process-(\d+),'
    jobString = str(multiprocessing.current_process())
    match = re.search(pattern, jobString)
    assert match.group(1) is not None, "Process ID was matched."
    returnDict[match.group(1)] = result


if __name__ == '__main__':
    logger = SEKLogger(__name__, 'debug')
    siUtil = SIUtil()
    processCommandLineArguments()

    paths = siUtil.pathsToProcess(COMMAND_LINE_ARGS.basepath)
    lenPaths = len(paths)
    finCnt = 0  # finished loading file count
    rowCnt = 0
    assert len(paths) >= 1


    def makeMeters():
        for name in siUtil.meters(basepath = COMMAND_LINE_ARGS.basepath):
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


    if MULTICORE:

        try:
            procs = []
            manager = multiprocessing.Manager()
            returnDict = manager.dict()

            for path in paths:
                procs.append(multiprocessing.Process(target = worker,
                                                     args = (path, returnDict)))
                procs[-1].daemon = True
                procs[-1].start()

            for proc in procs:
                proc.join()

            for key in returnDict.keys():
                sys.stderr.write("Process %s results:\n" % key)
                sys.stderr.write(returnDict[key])
                sys.stderr.write("\n")

        except Exception as detail:
            logger.log("exception {}".format(detail))

    else:
        # Single core:
        for p in paths:
            rowCnt += SingleFileLoader(p).insertDataFromFile()
            finCnt += 1
            logger.log(
                'finished loading {}, total finished {}/{}'.format(p, finCnt,
                                                                   lenPaths),
                'debug')
        logger.log('row cnt {}'.format(rowCnt))


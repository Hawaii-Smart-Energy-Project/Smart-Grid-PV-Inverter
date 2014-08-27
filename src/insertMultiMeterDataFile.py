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
from si_util import SIUtil


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


def do_work(path):
    logger.log('process {}'.format(str(multiprocessing.current_process())))
    SingleFileLoader(path).insertDataFromFile()


def worker():
    for item in iter(q.get, None):
        do_work(item)
        q.task_done()
    q.task_done()


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

    makeMeters()

    if MULTICORE:

        q = multiprocessing.JoinableQueue(MULTIPROCESSING_LIMIT)

        try:
            procs = []  # process pool
            for i in range(MULTIPROCESSING_LIMIT):
                procs.append(multiprocessing.Process(target = worker))
                procs[-1].daemon = True
                procs[-1].start()

            for path in paths:
                q.put(path)

            q.join()

            for p in procs:
                q.put(None)

            q.join()

            for p in procs:
                p.join()

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


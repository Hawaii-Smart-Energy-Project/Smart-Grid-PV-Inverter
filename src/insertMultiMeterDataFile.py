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

from sek.logger import SEKLogger, CRITICAL, ERROR, WARNING, INFO, DEBUG, SILENT
import argparse
from insertSingleMeterDataFile import SingleFileLoader
import multiprocessing
from si_util import SIUtil
import sys


COMMAND_LINE_ARGS = None
MULTIPROCESSING_LIMIT = 6
MULTICORE = True
RESULT_CNTS = {}
PATHS_PROCESSED_CNT = 0
TOTAL_PATHS = 0


class RowPathCounter(object):
    """
    Counter for multiprocessing.
    """
    def __init__(self, rowValue = 0, pathValue = 0):
        """
        :param rowValue: Int count of rows
        :param pathValue: Int count of paths
        """
        self.rows = multiprocessing.Value('i', rowValue)
        self.paths = multiprocessing.Value('i', pathValue)
        self.lock = multiprocessing.Lock()


    def incrementPaths(self):
        with self.lock:
            self.paths.value += 1


    def addRows(self, count):
        with self.lock:
            self.rows.value += count


    def rowValue(self):
        with self.lock:
            return self.rows.value


    def pathValue(self):
        with self.lock:
            return self.paths.value


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
    parser.add_argument('--process_count', type = int, required = False,
                        help = 'The number of processes to use for '
                               'multiprocessing.')
    COMMAND_LINE_ARGS = parser.parse_args()


def do_work(path, counter):
    loader = SingleFileLoader(path)
    name = loader.meterName()
    logger.log('process {} for meter {} with path {}'.format(
        str(multiprocessing.current_process()), name, path), DEBUG)

    if not loader.newDataForMeterExists():
        result = 0
    else:
        result = loader.insertDataFromFile()

    if result is None:
        logger.log('SQL error occurred.', ERROR)
        sys.exit(-1)
    counter.addRows(result)
    counter.incrementPaths()
    return (result, name)


def worker(myQ, counter):
    try:
        for item in iter(myQ.get, None):
            logger.log('queue {}'.format(myQ))
            (result, name) = do_work(item, counter)
            myQ.task_done()
            logger.log(
                '{}: {}: row counter {}, path counter {} out of {}'.format(item,
                                                                           name,
                                                                           counter.rowValue(),
                                                                           counter.pathValue(),
                                                                           TOTAL_PATHS))
    except Exception as detail:
        logger.log('Exception in worker in process {} for item {}: {}'.format(
            str(multiprocessing.current_process()), item, detail), ERROR)


if __name__ == '__main__':
    logger = SEKLogger(__name__, INFO)
    siUtil = SIUtil()
    processCommandLineArguments()
    if COMMAND_LINE_ARGS.process_count:
        MULTIPROCESSING_LIMIT = COMMAND_LINE_ARGS.process_count
    paths = siUtil.pathsToProcess(COMMAND_LINE_ARGS.basepath)
    TOTAL_PATHS = len(paths)
    assert len(paths) >= 1


    def makeMeters():
        for name in siUtil.meters(basepath = COMMAND_LINE_ARGS.basepath):
            logger.log('Loading multi files for meter name {}.'.format(
                SingleFileLoader().getMeterID(name)))
            RESULT_CNTS[name] = 0

    makeMeters()

    if MULTICORE:
        counter = RowPathCounter(0, 0)
        q = None

        def multiProcess(myPaths):

            q = multiprocessing.JoinableQueue(MULTIPROCESSING_LIMIT)
            try:

                procs = []  # process pool
                for i in range(MULTIPROCESSING_LIMIT):
                    procs.append(multiprocessing.Process(target = worker,
                                                         args = (
                                                         q, counter,)))
                    procs[-1].daemon = True
                    procs[-1].start()

                for path in myPaths:
                    q.put(path)
                q.close()
                q.join()

                for i in range(len(procs)):
                    q.put('STOP')
                q.close()
                q.join()

                for p in procs:
                    p.join()

            except Exception as detail:
                logger.log("exception {}".format(detail), ERROR)

        multiProcess(paths)
        logger.log('final row count {}'.format(counter.rowValue()))
        assert counter.pathValue() == TOTAL_PATHS

    else:
        # Single core:
        for p in paths:
            loader = SingleFileLoader(p)
            name = loader.meterName()
            if name in RESULT_CNTS:
                RESULT_CNTS[name] += loader.insertDataFromFile()
            else:
                RESULT_CNTS[name] = loader.insertDataFromFile()
            PATHS_PROCESSED_CNT += 1
            logger.log('Result summary:')
            for k in RESULT_CNTS.keys():
                logger.log('key {} = {}, paths processed {} out of {}'.format(k,
                                                                              RESULT_CNTS[
                                                                                  k],
                                                                              PATHS_PROCESSED_CNT,
                                                                              TOTAL_PATHS))

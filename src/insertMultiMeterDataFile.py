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
import os
import fnmatch


COMMAND_LINE_ARGS = None
MULTIPROCESSING_LIMIT = 4
RETRY_COUNT = 2


def processCommandLineArguments():
    """
    Create command line arguments and parse them.
    """

    global COMMAND_LINE_ARGS
    parser = argparse.ArgumentParser(
        description = 'Perform insertion of data contained in multiple files to the SI database.')
    parser.add_argument('--basepath', help = 'A base path from which to process data files.')
    COMMAND_LINE_ARGS = parser.parse_args()


def pathsToProcess():
    """
    :return: List
    """
    global COMMAND_LINE_ARGS
    pathsToProcess = []
    for root, dirnames, filenames in os.walk(COMMAND_LINE_ARGS.basepath):
        for filename in fnmatch.filter(filenames, '*.csv'):
            logger.log(filename, 'debug')
            pathsToProcess.append(os.path.join(root, filename))
    return pathsToProcess


if __name__ == '__main__':
    logger = SEKLogger(__name__, 'debug')
    processCommandLineArguments()

    paths = pathsToProcess()
    assert len(paths) >= 1

    logger.log('Loading multi files for meter name {}.'.format(
        SingleFileLoader(paths[0]).meterName()))


    def insertData(x):
        logger.log('process {}'.format(str(multiprocessing.current_process())))
        SingleFileLoader(x).insertDataFromFile()
        logger.log('finished loading {}'.format(x), 'debug')


    pool = multiprocessing.Pool(MULTIPROCESSING_LIMIT)
    results = pool.map(insertData, paths)
    pool.close()
    pool.join()

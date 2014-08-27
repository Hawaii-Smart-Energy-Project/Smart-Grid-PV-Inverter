#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart-Grid' \
              '-PV-Inverter/master/BSD-LICENSE.txt'

from sek.logger import SEKLogger
import os
import fnmatch


class SIUtil(object):
    def __init__(self):
        """
        Constructor.
        """
        self.logger = SEKLogger(__name__, 'INFO')


    def pathsToProcess(self, basepath = ''):
        """
        :param basepath: String
        :return: List
        """
        pathsToProcess = []
        for root, dirnames, filenames in os.walk(basepath):
            for filename in fnmatch.filter(filenames, '*.csv'):
                pathsToProcess.append(os.path.join(root, filename))
        return pathsToProcess


    def meters(self, basepath = ''):
        """
        :param basepath: String
        :return: List
        """
        if basepath == '':
            raise Exception("Basepath not given.")

        meters = {}
        for p in self.pathsToProcess(basepath):
            meterName = os.path.basename(os.path.dirname(p))
            if meterName not in meters:
                meters[meterName] = 1
        return meters.keys()

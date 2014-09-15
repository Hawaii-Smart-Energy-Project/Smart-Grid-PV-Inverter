#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import unittest
from sek.logger import SEKLogger, CRITICAL, ERROR, WARNING, INFO, DEBUG, SILENT
from si_data_util import SIDataUtil
from datetime import datetime

class SIDataUtilTester(unittest.TestCase):
    """
    """

    def setUp(self):
        self.dataUtil = SIDataUtil()
        self.logger = SEKLogger(__name__)


    def test_find_max_timestamp(self):
        filePath = 'data/test-meter/log.csv'
        self.assertEquals(self.dataUtil.maxTimeStamp(filePath),
                          datetime.strptime('2014-03-10 23:59:00',
                                            '%Y-%m-%d %H:%M:%S'))

    def test_find_max_timestamp_db(self):
        meter = '001EC6051A0D'
        self.logger.log(self.dataUtil.maxTimeStampDB(meter))


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:

        tests = []

        # For testing:
        selected_tests = ['test_find_max_timestamp_db', 'test_find_max_timestamp']

        mySuite = unittest.TestSuite()
        if len(selected_tests) > 0:
            for t in selected_tests:
                mySuite.addTest(SIDataUtilTester(t))
        else:
            for t in tests:
                mySuite.addTest(SIDataUtilTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from insertSingleMeterDataFile import SingleFileLoader
from si_configer import SIConfiger
from sek.logger import SEKLogger


class SingleFileLoaderTester(unittest.TestCase):
    def setUp(self):
        self.logger = SEKLogger(__name__,'DEBUG')
        self.configer = SIConfiger()
        self.inserter = SingleFileLoader()
        self.data = '"2014-07-12 16:22:30",0,,,1187488464896.00,' \
                    '2322185846784.00,1134697381888.00,35184644096.00,' \
                    '290857353216.00,10133100822528.00,367.13,' \
                    '-17660932096.00,1078.01,17660934144.00,-7.86,1.80,8.06,' \
                    '-0.97,244.01,122.00,32.93,60.01,-7.09,1.42,7.24,8.06,' \
                    '3.34,8.35,-40.18,-5.68,40.52,516.72,403.12,0,' \
                    '8797179904.00,47518.67,0,86.03,50.23,4198.40,' \
                    '281475022848.00,2251868602368.00,0,6820.01,' \
                    '8796095488.00,0,178.83,188.30,0,620.07,505.19,' \
                    '288230389841920.02,12668.18,68729384.00,0,-3.68,-4.18,,' \
                    '1.00,0.79,,3.81,4.25,,-0.97,-0.98,,244.01,,,121.54,' \
                    '122.46,,31.28,34.59,'


    def test_columns(self):
        self.assertEquals(len(self.inserter.columns), 76)


    def test_insert_data(self):
        self.inserter.insertData(self.data)


    def test_sql_formatted_values(self):
        self.logger.log('data: {}'.format(self.inserter.sqlFormattedValues(self.data)))


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:

        tests = ['test_insert_data']

        # For testing:
        # selected_tests = []

        mySuite = unittest.TestSuite()
        for t in tests:
            mySuite.addTest(SingleFileLoaderTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()

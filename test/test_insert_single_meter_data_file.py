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


    def test_columns(self):
        self.assertEquals(len(self.inserter.columns), 76)


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:

        tests = ['test_columns']

        # For testing:
        # selected_tests = []

        mySuite = unittest.TestSuite()
        for t in tests:
            mySuite.addTest(SingleFileLoaderTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()

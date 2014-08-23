#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart-Grid' \
              '-PV-Inverter/master/BSD-LICENSE.txt'

import unittest
from insertSingleMeterDataFile import SingleFileLoader
from si_configer import SIConfiger
from sek.logger import SEKLogger
from sek.db_util import SEKDBUtil
from sek.db_connector import SEKDBConnector
from insertMultiMeterDataFile import MultiFileLoader


class SingleFileLoaderTester(unittest.TestCase):
    def setUp(self):
        self.logger = SEKLogger(__name__, 'DEBUG')
        self.configer = SIConfiger()
        self.conn = SEKDBConnector(
            dbName = self.configer.configOptionValue('Database', 'db_name'),
            dbHost = self.configer.configOptionValue('Database', 'db_host'),
            dbPort = self.configer.configOptionValue('Database', 'db_port'),
            dbUsername = self.configer.configOptionValue('Database',
                                                         'db_username'),
            dbPassword = self.configer.configOptionValue('Database',
                                                         'db_password')).connectDB()
        self.cursor = self.conn.cursor()
        self.dbUtil = SEKDBUtil()
        self.inserter = MultiFileLoader('data/test-meter/log.csv')

        self.testMeterName = 'test-meter'


    def test_insert_meter_data_files(self):
        pass


    def tearDown(self):
        self.logger.log('teardown', 'debug')
        sql = 'SELECT meter_id FROM "Meters" WHERE meter_name = \'{}\''.format(
            self.testMeterName)
        success = self.dbUtil.executeSQL(self.cursor, sql, exitOnFail = True)
        if success:
            result = self.cursor.fetchall()
            if len(result) == 1:
                sql = 'DELETE FROM "Meters" WHERE meter_id = {}'.format(
                    result[0][0])
                success = self.dbUtil.executeSQL(self.cursor, sql,
                                                 exitOnFail = True)
                if success:
                    self.conn.commit()
                sql = 'SELECT meter_id FROM "Meters" WHERE meter_name = \'{' \
                      '}\''.format(self.testMeterName)
                success = self.dbUtil.executeSQL(self.cursor, sql,
                                                 exitOnFail = True)
                result = self.cursor.fetchall()
                self.assertEquals(0, len(result))


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:

        tests = []

        # For testing:
        selected_tests = ['test_insert_meter_data_files']

        mySuite = unittest.TestSuite()
        if len(selected_tests) > 0:
            for t in selected_tests:
                mySuite.addTest(SingleFileLoaderTester(t))
        else:
            for t in tests:
                mySuite.addTest(SingleFileLoaderTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()

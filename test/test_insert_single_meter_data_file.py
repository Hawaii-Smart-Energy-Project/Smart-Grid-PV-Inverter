#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from insertSingleMeterDataFile import SingleFileLoader
from si_configer import SIConfiger
from sek.logger import SEKLogger
from sek.db_util import SEKDBUtil
from sek.db_connector import SEKDBConnector


class SingleFileLoaderTester(unittest.TestCase):
    def setUp(self):
        self.logger = SEKLogger(__name__,'DEBUG')
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
        self.inserter = SingleFileLoader('data/test-meter/log.csv')
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
        self.testMeterName = 'test-meter'


    def test_columns(self):
        self.assertEquals(len(self.inserter.columns), 76)


    def test_insert_data(self):
        self.logger.log('testing data insert')
        self.assertTrue(self.inserter.insertData(self.testMeterName, self.data))
        self.conn.commit()


    def test_sql_formatted_values(self):
        self.logger.log(
            'data: {}'.format(self.inserter.sqlFormattedValues(self.data)))


    def test_meter_id(self):
        self.logger.log('testing meter id')
        meter_id = self.inserter.meterID(self.testMeterName)
        self.logger.log('meter id {}'.format(meter_id))
        self.assertTrue(isinstance(meter_id, ( int, long )))
        self.logger.log('getting meter id')
        sql = 'SELECT meter_id FROM "Meters" WHERE meter_name = \'{}\''.format(
            self.testMeterName)
        success = self.dbUtil.executeSQL(self.cursor, sql, exitOnFail = True)
        if success:
            result = self.cursor.fetchall()
            self.assertEquals(1, len(result))
        else:
            self.logger.log('failed to retrieve meter id', 'error')


    def test_meter_name(self):
        """
        Test getting the meter name.
        :return:
        """
        self.logger.log(self.inserter.meterName(), 'debug')


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

        tests = ['test_insert_data', 'test_meter_id']

        # For testing:
        selected_tests = ['test_meter_name']

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

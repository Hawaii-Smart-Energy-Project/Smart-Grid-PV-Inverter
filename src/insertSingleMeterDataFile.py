#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Inserts a single file of meter data.

Usage:

    insertSingleMeterDataFile.py --filepath ${FILEPATH}

or

    from insertSingleMeterDataFile import SingleFileLoader
    loader = SingleFileLoader(${FILEPATH}).insertDataFromFile()

or for meter creation or retrieval:

    loader = SingleFileLoader().getMeterID(${METER_NAME})

The meter name is by convention the folder name in which the data is contained.

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart-Grid' \
              '-PV-Inverter/master/BSD-LICENSE.txt'

from sek.logger import SEKLogger, CRITICAL, ERROR, WARNING, INFO, DEBUG, SILENT
from si_configer import SIConfiger
from sek.db_util import SEKDBUtil
from sek.db_connector import SEKDBConnector
import argparse
import os
import sys
from si_data_util import SIDataUtil


COMMAND_LINE_ARGS = None
COMMIT_INTERVAL = 1000


def processCommandLineArguments():
    """
    Create command line arguments and parse them.
    """

    global COMMAND_LINE_ARGS
    parser = argparse.ArgumentParser(
        description = 'Perform insertion of data contained in a single file to '
                      'the SI database.')
    parser.add_argument('--filepath', required = True,
                        help = 'A filepath, including the filename, '
                               'for a file containing data to be inserted.')
    parser.add_argument('--skipNewDataCheck', action = 'store_true',
                        default = False, help = 'Skip the new data check.')
    COMMAND_LINE_ARGS = parser.parse_args()


class SingleFileLoader(object):
    """
    Perform insertion of data contained in a single file to the Smart Inverter database
    specified in the configuration file.
    """

    def __init__(self, filepath = ''):
        """
        Constructor.

        :param testing: Flag indicating if testing mode is on.
        """

        self.logger = SEKLogger(__name__, DEBUG)
        self.configer = SIConfiger()
        self.dbUtil = SEKDBUtil()
        self.dataUtil = SIDataUtil()
        self.logger.log('making new db conn for filepath {}'.format(filepath), SILENT)
        sys.stdout.flush()

        try:
            self.conn = SEKDBConnector(
                dbName = self.configer.configOptionValue('Database', 'db_name'),
                dbHost = self.configer.configOptionValue('Database', 'db_host'),
                dbPort = self.configer.configOptionValue('Database', 'db_port'),
                dbUsername = self.configer.configOptionValue('Database',
                                                             'db_username'),
                dbPassword = self.configer.configOptionValue('Database',
                                                             'db_password')).connectDB()
        except:
            raise Exception("Unable to get DB connection.")
        self.cursor = self.conn.cursor()
        self.exitOnError = False

        # An empty file path is used during creating of meter table entries.
        if filepath == '':
            self.filepath = None
            self.meterID = None
            self.meterDataTable = None
        else:
            self.filepath = filepath
            self.meterID = self.getMeterID(self.meterName())
            assert self.meterID is not None
            self.meterDataTable = "MeterData_{}".format(self.meterName())
            # @todo Test existence of meter data table.
        self.timestampColumn = 0 # timestamp col in the raw data


    def newDataForMeterExists(self):
        """
        :return: Boolean true if file has new data.
        """
        try:
            if (self.dataUtil.maxTimeStamp(
                    self.filepath) >= self.dataUtil.maxTimeStampDB(
                    self.meterName())):
                return True
            return False
        except TypeError as detail:
            # @todo Log the cause of the exception.
            self.logger.log('Exception: {}'.format(detail), CRITICAL)
            return False


    def insertDataFromFile(self):
        """
        Process input file as a stream from the object attribute's filepath.
        :return: Int count of inserted records or None on error.
        """

        insertCnt = 0
        with open(self.filepath) as dataFile:
            lineCnt = 1
            result = False

            # @todo handle io errors
            self.logger.log('loading data from {}'.format(dataFile), DEBUG)
            for line in dataFile:
                result = self.insertData(
                    line.rstrip('\n')) if lineCnt != 1 else False
                if result is None:
                    self.logger.log('Critical insert failure', CRITICAL)
                    raise Exception('Insert did not complete')
                    # self.logger.log('insert did not complete', ERROR)
                    # return None
                if insertCnt > 0 and insertCnt % COMMIT_INTERVAL == 0:
                    self.conn.commit()
                    self.logger.log('committing at {}'.format(insertCnt), DEBUG)
                    sys.stdout.flush()
                if result:
                    insertCnt += 1
                lineCnt += 1
            self.conn.commit()
            self.logger.log('final commit at {}'.format(insertCnt), DEBUG)
        return insertCnt


    def insertData(self, values, commitOnEvery = False):
        """
        Insert a row of data to the database.
        :param values: String of raw values from the source CSV files.
        :return: Boolean indicating success or failure.
        """

        if not values or self.dataUtil.badData(values):
            return False

        if self.removeDupe(values):
            self.logger.log('duplicate found', DEBUG)

        sql = 'INSERT INTO "{0}" ({1}) VALUES({2}, {3})'.format(
            self.meterDataTable,
            ','.join("\"" + c + "\"" for c in self.dataUtil.dbColumns),
            self.meterID, self.dataUtil.sqlFormattedValues(values))
        self.logger.log('sql: {}'.format(sql), DEBUG)

        if self.dbUtil.executeSQL(self.cursor, sql,
                                  exitOnFail = self.exitOnError):
            if commitOnEvery:
                self.conn.commit()
            return True
        else:
            return False


    def removeDupe(self, values):

        def deleteDupe(myMeterID, myTimeUTC):
            sql = 'DELETE FROM "{0}" WHERE meter_id = {1} AND time_utc = {' \
                  '2}'.format(self.meterDataTable, myMeterID, myTimeUTC)
            if self.dbUtil.executeSQL(self.cursor, sql,
                                  exitOnFail = self.exitOnError):
                return True
            else:
                return False


        if not values:
            return False

        timeUTC = self.timeUTC(values)

        # This is dependendent on the quote style used for time UTC in the
        # raw data.
        sql = 'SELECT time_utc FROM "{0}" WHERE meter_id = {1} AND time_utc = ' \
              '{2}'.format(
            self.meterDataTable, self.meterID, timeUTC)

        if self.dbUtil.executeSQL(self.cursor, sql,
                                  exitOnFail = self.exitOnError):
            rows = self.cursor.fetchone()

            if rows and len(rows) == 1:
                if deleteDupe(self.meterID, timeUTC):
                    return True
                else:
                    raise Exception(
                        "Unable to remove dupe for meter ID {}, time UTC {}".format(
                            self.meterID, timeUTC))
        return False


    def timeUTC(self, values):
        def makeSingleQuotes(x):
            return str(x).replace('"', "'")


        return makeSingleQuotes(values.split(',')[self.timestampColumn])


    def meterName(self):
        """
        The meter name is the name of the containing folder.
        :return:
        """
        # @todo validate meter name
        def validMeterName(name):
            pass


        return os.path.basename(os.path.dirname(self.filepath))


    def getMeterID(self, meterName):
        """
        Given a meter name, return its meter ID.
        If the meter name has no ID, create a new one and return its ID.
        :param meterName: String
        :return: Int of meter ID
        """


        def __meterID(name):
            """
            :param name: String of meter name
            :return: Int or None
            """
            sql = 'SELECT meter_id FROM "Meters" WHERE meter_name = \'{' \
                  '}\''.format(name)
            success = self.dbUtil.executeSQL(self.cursor, sql,
                                             exitOnFail = False)
            if success:
                result = self.cursor.fetchall()
                assert len(result) == 1 or len(result) == 0
                if result:
                    return int(result[0][0])
                else:
                    return None
            else:
                return None


        def __makeNewMeter(name):
            """
            :param name: String of meter name
            :return: Int or None
            """
            id = __meterID(name)
            if id:
                return id

            self.logger.log('making new meter', DEBUG)
            sql = 'INSERT INTO "Meters" (meter_name) VALUES (\'{}\')'.format(
                name)
            success = self.dbUtil.executeSQL(self.cursor, sql,
                                             exitOnFail = False)
            self.conn.commit()
            if success:
                sql = 'SELECT CURRVAL(\'meter_id_seq\')'
                success = self.dbUtil.executeSQL(self.cursor, sql,
                                                 exitOnFail = False)
                if success:
                    return int(self.cursor.fetchall()[0][0])
            else:
                return None


        id = __meterID(meterName)

        # Python 3: if isinstance( id, int ):
        if isinstance(id, ( int, long )):
            return int(id)
        else:
            return __makeNewMeter(meterName)


    def __del__(self):
        self.logger.log('Destroying single file inserter', DEBUG)
        self.conn.close()


if __name__ == '__main__':
    processCommandLineArguments()
    logger = SEKLogger(__name__)
    inserter = SingleFileLoader(COMMAND_LINE_ARGS.filepath)
    if COMMAND_LINE_ARGS.skipNewDataCheck:
        logger.log('result = {}'.format(inserter.insertDataFromFile()))
    elif inserter.newDataForMeterExists():
        logger.log('result = {}'.format(inserter.insertDataFromFile()))
    else:
        logger.log('no new data')

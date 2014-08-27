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

from sek.logger import SEKLogger
from si_configer import SIConfiger
from sek.db_util import SEKDBUtil
from sek.db_connector import SEKDBConnector
import argparse
import os
import sys


commandLineArgs = None
COMMIT_INTERVAL = 1000


def processCommandLineArguments():
    """
    Create command line arguments and parse them.
    """

    global parser, commandLineArgs
    parser = argparse.ArgumentParser(
        description = 'Perform insertion of data contained in a single file to '
                      'the SI database.')
    parser.add_argument('--filepath', required = True,
                        help = 'A filepath, including the filename, '
                               'for a file containing data to be inserted.')
    commandLineArgs = parser.parse_args()


class SingleFileLoader(object):
    """
    Perform insertion of data contained in a single file to the Smart Inverter database
    specified in the configuration file.
    """

    def __init__(self, filepath = '', testing = False):
        """
        Constructor.

        :param testing: Flag indicating if testing mode is on.
        """

        self.logger = SEKLogger(__name__, 'info')
        self.configer = SIConfiger()
        self.dbUtil = SEKDBUtil()
        self.logger.log('making new db conn for filepath {}'.format(filepath), 'debug')
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
        self.exitOnError = True
        self.dbColumns = [
            "meter_id", "time_utc", "error", "lowalarm", "highalarm",
            "Accumulated Real Energy Net (kWh)",
            "Real Energy Quadrants 1 & 4, Import (kWh)",
            "Real Energy Quadrants 2 & 3, Export (kWh)",
            "Reactive Energy Quadrant 1 (VARh)",
            "Reactive Energy Quadrant 2 (VARh)",
            "Reactive Energy Quadrant 3 (VARh)",
            "Reactive Energy Quadrant 4 (VARh)", "Apparent Energy Net (VAh)",
            "Apparent Energy Quadrants 1 & 4 (VAh)",
            "Apparent Energy Quadrants 2 & 3 (VAh)",
            "Total Net Instantaneous Real Power (kW)",
            "Total Net Instantaneous Reactive Power (kVAR)",
            "Total Net Instantaneous Apparent Power (kVA)",
            "Total Power Factor", "Voltage, L-L, 3p Ave (Volts)",
            "Voltage, L-N, 3p Ave (Volts)", "Current, 3p Ave (Amps)",
            "Frequency (Hz)", "Total Real Power Present Demand (kW)",
            "Total Reactive Power Present Demand (kVAR)",
            "Total Apparent Power Present Demand (kVA)",
            "Total Real Power Max Demand, Import (kW)",
            "Total Reactive Power Max Demand, Import (kVAR)",
            "Total Apparent Power Max Demand, Import (kVA)",
            "Total Real Power Max Demand, Export (kW)",
            "Total Reactive Power Max Demand, Export (kVAR)",
            "Total Apparent Power Max Demand, Export (kVA)",
            "Accumulated Real Energy, Phase A, Import (kW)",
            "Accumulated Real Energy, Phase B, Import (kW)",
            "Accumulated Real Energy, Phase C, Import (kW)",
            "Accumulated Real Energy, Phase A, Export (kW)",
            "Accumulated Real Energy, Phase B, Export (kW)",
            "Accumulated Real Energy, Phase C, Export (kW)",
            "Accumulated Q1 Reactive Energy, Phase A, Import (VARh)",
            "Accumulated Q1 Reactive Energy, Phase B, Import (VARh)",
            "Accumulated Q1 Reactive Energy, Phase C, Import (VARh)",
            "Accumulated Q2 Reactive Energy, Phase A, Import (VARh)",
            "Accumulated Q2 Reactive Energy, Phase B, Import (VARh)",
            "Accumulated Q2 Reactive Energy, Phase C, Import (VARh)",
            "Accumulated Q3 Reactive Energy, Phase A, Export (VARh)",
            "Accumulated Q3 Reactive Energy, Phase B, Export (VARh)",
            "Accumulated Q3 Reactive Energy, Phase C, Export (VARh)",
            "Accumulated Q4 Reactive Energy, Phase A, Export (VARh)",
            "Accumulated Q4 Reactive Energy, Phase B, Export (VARh)",
            "Accumulated Q4 Reactive Energy, Phase C, Export (VARh)",
            "Accumulated Apparent Energy, Phase A, Import (VAh)",
            "Accumulated Apparent Energy, Phase B, Import (VAh)",
            "Accumulated Apparent Energy, Phase C, Import (VAh)",
            "Accumulated Apparent Energy, Phase A, Export (VAh)",
            "Accumulated Apparent Energy, Phase B, Export (VAh)",
            "Accumulated Apparent Energy, Phase C, Export (VAh)",
            "Real Power, Phase A (kW)", "Real Power, Phase B (kW)",
            "Real Power, Phase C (kW)", "Reactive Power, Phase A (kVAR)",
            "Reactive Power, Phase B (kVAR)", "Reactive Power, Phase C (kVAR)",
            "Apparent Power, Phase A (kVA)", "Apparent Power, Phase B (kVA)",
            "Apparent Power, Phase C (kVA)", "Power Factor, Phase A",
            "Power Factor, Phase B", "Power Factor, Phase C",
            "Voltage, Phase A-B (Volts)", "Voltage, Phase B-C (Volts)",
            "Voltage, Phase A-C (Volts)", "Voltage, Phase A-N (Volts)",
            "Voltage, Phase B-N (Volts)", "Voltage, Phase C-N (Volts)",
            "Current, Phase A (Amps)", "Current, Phase B (Amps)",
            "Current, Phase C (Amps)"
        ]

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


    def insertDataFromFile(self):
        """
        Process input file as a stream from the object attribute's filepath.
        :return: Int count of inserted records.
        """
        insertCnt = 0
        with open(self.filepath) as dataFile:
            lineCnt = 1
            result = False

            # @todo handle io errors
            self.logger.log('loading data from {}'.format(dataFile), 'debug')
            for line in dataFile:
                result = self.insertData(
                    line.rstrip('\n')) if lineCnt != 1 else False
                if insertCnt > 0 and insertCnt % COMMIT_INTERVAL == 0:
                    self.conn.commit()
                    self.logger.log('committing at {}'.format(insertCnt),
                                    'debug')
                    sys.stdout.flush()
                if result:
                    insertCnt += 1
                lineCnt += 1
            self.conn.commit()
            self.logger.log('final commit at {}'.format(insertCnt), 'debug')
        return insertCnt


    def insertData(self, values, commitOnEvery = False):
        """
        Insert a row of data to the database.
        :param values: String of raw values from the source CSV files.
        :return: Boolean indicating success or failure.
        """

        def badData(values):
            # DB cols contain an extra column for the meter ID that is not
            # found in individual raw data files.
            if len(self.dbColumns) - 1 != len(values.split(',')):
                return True
            return False

        if not values or badData(values):
            return False

        if self.removeDupe(values):
            self.logger.log('duplicate found', 'debug')

        sql = 'INSERT INTO "{0}" ({1}) VALUES({2}, {3})'.format(
            self.meterDataTable,
            ','.join("\"" + c + "\"" for c in self.dbColumns),
            self.meterID, self.sqlFormattedValues(values))

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


    def sqlFormattedValues(self, values):
        """
        :param values: String of raw values from the source CSV files.
        :return: String of PostgreSQL compatible values.
        """


        def makeNULL(x):
            return x == '' and 'NULL' or str(x)


        def makeSingleQuotes(x):
            return str(x).replace('"', "'")


        return ','.join(
            map(lambda x: makeSingleQuotes(makeNULL(x)), values.split(',')))


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
        If the meter name has no ID, create a new one and return it.
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

            self.logger.log('making new meter', 'debug')
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
        self.logger.log('destroying single file inserter', 'debug')
        self.conn.close()


if __name__ == '__main__':
    processCommandLineArguments()
    inserter = SingleFileLoader(commandLineArgs.filepath)
    inserter.insertDataFromFile()

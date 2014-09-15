#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart-Grid' \
              '-PV-Inverter/master/BSD-LICENSE.txt'

from sek.logger import SEKLogger, CRITICAL, ERROR, WARNING, INFO, DEBUG, SILENT
import re
from datetime import datetime
from si_configer import SIConfiger
from sek.db_util import SEKDBUtil
from sek.db_connector import SEKDBConnector

class SIDataUtil(object):
    def __init__(self):
        self.logger = SEKLogger(__name__, DEBUG)
        self.configer = SIConfiger()
        self.dbUtil = SEKDBUtil()
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


    def badData(self, values):
        """
        :param values: String
        :return: Boolean
        """
        # DB cols contain an extra column for the meter ID that is not
        # found in individual raw data files.

        if len(self.dbColumns) - 1 != len(values.split(',')):
            return True

        if not re.match('^\"\d+-\d+-\d+\s\d+:\d+:\d+\"', values.split(',')[0]):
            self.logger.log('bad date {}'.format(values.split(',')[0]), ERROR)
            return True

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


    def maxTimeStamp(self, filepath = ''):
        """
        :param filepath: String
        :return: datetime or None
        """

        with open(filepath) as dataFile:
            max = None
            lineCnt = 1
            for line in dataFile:
                values = line.rstrip('\n') if lineCnt != 1 else False
                if values and not self.badData(values):
                    dateString = self.sqlFormattedValues(values).split(',')[0]
                    if dateString.startswith("'") and dateString.endswith("'"):
                        dateString = dateString[1:-1]
                    curr = datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
                    if not max or curr > max:
                        max = curr
                lineCnt += 1
        return max


    def maxTimeStampDB(self, meter = ''):
        sql = 'SELECT MAX(time_utc) FROM "MeterData_{}"'.format(meter)
        if self.dbUtil.executeSQL(self.cursor, sql,
                                  exitOnFail = self.exitOnError):
            row = self.cursor.fetchone()
            if row and len(row) == 1:
                self.logger.log('row {}'.format(row))
                return row[0]
        return None

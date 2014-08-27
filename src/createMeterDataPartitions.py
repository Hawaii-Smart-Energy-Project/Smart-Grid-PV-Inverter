#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart-Grid' \
              '-PV-Inverter/master/BSD-LICENSE.txt'

"""
Create meter data partitions based on meter name.
"""

import argparse
from sek.logger import SEKLogger
from si_configer import SIConfiger
from sek.db_util import SEKDBUtil
from sek.db_connector import SEKDBConnector
from si_util import SIUtil

COMMAND_LINE_ARGS = None


def processCommandLineArguments():
    """
    Create command line arguments and parse them.
    """

    global COMMAND_LINE_ARGS
    parser = argparse.ArgumentParser(
        description = 'Perform insertion of data contained in multiple files '
                      'to the SI database.')
    parser.add_argument('--basepath', required = True,
                        help = 'A base path from which to process data files.')
    COMMAND_LINE_ARGS = parser.parse_args()


if __name__ == '__main__':
    processCommandLineArguments()
    tableBase = "MeterData"
    pkey = 'meter_id, time_utc'
    logger = SEKLogger(__name__, 'debug')
    configer = SIConfiger()
    dbUtil = SEKDBUtil()
    conn = SEKDBConnector(
        dbName = configer.configOptionValue('Database', 'db_name'),
        dbHost = configer.configOptionValue('Database', 'db_host'),
        dbPort = configer.configOptionValue('Database', 'db_port'),
        dbUsername = configer.configOptionValue('Database', 'db_username'),
        dbPassword = configer.configOptionValue('Database',
                                                'db_password')).connectDB()
    cursor = conn.cursor()

    tableOwner = configer.configOptionValue('Database', 'table_owner')
    for meterName in SIUtil().meters(basepath = COMMAND_LINE_ARGS.basepath):
        logger.log('creating table {}'.format(tableBase + "_" + meterName))
        sql = 'CREATE TABLE "{1}_{0}" ( CHECK ( meter_id = meter_id(\'{' \
              '0}\'))) INHERITS ("{1}"); ALTER TABLE ONLY "{1}_{0}" ADD ' \
              'CONSTRAINT "{1}_{0}_pkey" PRIMARY KEY ({3}); ALTER TABLE ONLY ' \
              '"{1}_{0}" ADD CONSTRAINT meter_id_fkey FOREIGN KEY (meter_id) ' \
              'REFERENCES "Meters"(meter_id) ON UPDATE CASCADE ON DELETE ' \
              'CASCADE; ALTER TABLE "{1}_{0}" OWNER TO {2}'.format(
            meterName, tableBase, tableOwner, pkey)
        if dbUtil.executeSQL(cursor, sql, exitOnFail = False):
            conn.commit()
        else:
            conn.rollback()

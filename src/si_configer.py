#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart-Grid' \
              '-PV-Inverter/master/BSD-LICENSE.txt'

import ConfigParser
from sek.logger import SEKLogger
import os
import sys
from sek.file_util import SEKFileUtil
from sek.db_util import SEKDBUtil

class SIConfiger(object):
    """
    Supports site-level config for the Smart Grid PV Inverter project.
    The default path is ~/.smart-inverter.cfg.

    Usage:

        configer = SIConfiger()

    """


    def __init__(self):
        """
        Constructor.
        """

        self._config = ConfigParser.ConfigParser()
        self.logger = SEKLogger(__name__, 'INFO')
        self.fileUtil = SEKFileUtil()
        self.dbUtil = SEKDBUtil()
        self.cursor = None

        configFilePath = '~/.smart-inverter.cfg'

        if self.fileUtil.isMoreThanOwnerReadableAndWritable(
                os.path.expanduser(configFilePath)):
            self.logger.log(
                "Configuration file permissions are too permissive. Operation "
                "will not continue.", 'error')
            sys.exit()




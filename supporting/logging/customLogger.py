#  MIT License
#
#  Copyright (c) 2019 Jac. Beekers
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

##
# Supporting modules
# @Since: 22-MAR-2019
# @Author: Jac. Beekers
# @Version: 20200530.0 - JBE - now a class
# @Version: 20200610.0 - JBE - debug output to console

import datetime
import logging
import os
import sys

from supporting import generalConstants


class CustomLogger:

    def __init__(self, main_proc='default', log_on_console=True):
        self.logger = logging.getLogger(main_proc)
        self.now = datetime.datetime.now()
        self.main_proc = main_proc
        self.log_on_console = log_on_console

    def configurelogger(self):

        logdir = os.environ.get(generalConstants.varLogDir, generalConstants.DEFAULT_LOGDIR)
        logging.basicConfig(
            filename=logdir + "/" + self.now.strftime("%Y%m%d-%H%M%S.%f") + '-' + self.main_proc + '.log'
            , level=logging.DEBUG
            , format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # nice for Azure DevOps, but not for Airflow
        if self.log_on_console:
            self.console = logging.StreamHandler()
            self.console.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            # tell the handler to use this format
            self.console.setFormatter(formatter)
            # add the handler to the root logger
            # logging.getLogger('').removeHandler(console)
            self.logger.addHandler(self.console)

        ResultDir = os.environ.get(generalConstants.varResultDir, generalConstants.DEFAULT_RESULTDIR)
        ResultFileName = ResultDir + "/" + self.now.strftime("%Y%m%d-%H%M%S.%f") + '-' + self.main_proc + '.result'

        resultlogger = logging.getLogger('result_logger')
        resultlogger.setLevel(logging.INFO)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(ResultFileName)
        fh.setLevel(logging.INFO)
        # create formatter and add it to the handler
        formatter = logging.Formatter('%(message)s')
        fh.setFormatter(formatter)
        # add the handlers to logger
        resultlogger.addHandler(fh)

        return resultlogger

    def log(self, logger, level, area, message):
        if self.log_on_console:
            print(logging.getLevelName(level) + " - " + area + " - " + message)

        logger.log(level, area + " - " + message)
        return

    def writeresult(self, resultlogger, result):
        resultlogger.info('RC=' + str(result.rc))
        resultlogger.info('CODE=' + result.code)
        resultlogger.info('MSG=' + result.message)
        resultlogger.info('RESOLUTION=' + result.resolution)
        resultlogger.info('AREA=' + result.area)
        resultlogger.info('ERRLEVEL=' + str(result.level))

    def exitscript(self, resultlogger, result):
        self.writeresult(resultlogger, result)
        sys.exit(result.rc)

    def logentireenv(self):
        thisproc = "logentireenv"
        for param in os.environ.keys():
            self.log(self.logger, logging.DEBUG, thisproc, "%30s %s" % (param, os.environ[param]))

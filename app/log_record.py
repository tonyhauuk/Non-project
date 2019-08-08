# -*- coding: utf-8 -*-

import logging
from logging import handlers
import time, os


class Logger(object):
    levelDict = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, logName):
        self.timestamp = str(int(time.time()))
        self.time = time.strftime('%Y-%m-%d', time.localtime())  # time : %H:%M:%S
        self.fileName = self.time + '-' + logName

    def logger(self, level='info'):
        # self.__checkSize__()

        self.logger = logging.getLogger(self.fileName)
        format = logging.Formatter('%(asctime)s %(filename)s %(threadName)s [line:%(lineno)d] %(levelname)s %(message)s')
        self.logger.setLevel(self.levelDict.get(level))
        screenPrint = logging.StreamHandler()
        screenPrint.setFormatter(format)
        handler = handlers.TimedRotatingFileHandler(filename=self.fileName, when='D', backupCount=3, encoding='utf-8')
        handler.setFormatter(format)
        self.logger.addHandler(screenPrint)
        self.logger.addHandler(handler)


        # LOG.basicConfig(level=lev,
        #                 format='%(asctime)s %(filename)s %(threadName)s [line:%(lineno)d] %(levelname)s %(message)s',
        #                 datefmt='%a, %d %b %Y %H:%M:%S',
        #                 filename=self.fileName,
        #                 filemode='a')

    def __checkSize__(self):
        try:
            size = os.path.getsize(self.fileName)
            if size > 10000:
                with open(self.fileName, 'r+') as f:
                    f.seek(0)
                    f.truncate()
        except FileNotFoundError:
            pass

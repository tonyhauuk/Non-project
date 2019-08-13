# -*- coding:utf-8 -*-

import logging
import time, os

class Logger:
    def __init__(self):
        self.timestamp = str(int(time.time()))
        self.time = time.strftime('%Y-%m-%d', time.localtime())  # time : %H:%M:%S

    def logger(self, method, message, level='info'):
        levelDict = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'crit': logging.CRITICAL
        }

        type = levelDict[level]
        self.fileName = self.time + '_' + level + '.log'

        format1 = '%(asctime)s %(filename)s %(threadName)s : [line:%(lineno)d] %(levelname)s %(message)s'
        format2 = '%(asctime)s %(filename)s %(threadName)s : [line:%(lineno)d] %(message)s'

        logging.basicConfig(level=type,
                            format=format2,
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=self.fileName,
                            filemode='a')

        logging.error(method + ' ' + message)

        self.__checkSize__()

    def __checkSize__(self):
        try:
            size = os.path.getsize(self.fileName)
            if size > 10000:
                with open(self.fileName, 'r+') as f:
                    f.seek(0)
                    f.truncate()
        except FileNotFoundError:
            pass

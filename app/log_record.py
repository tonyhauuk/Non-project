import logging as LOG


def writeLog():
    LOG.basicConfig(level=LOG.DEBUG,
                    format='%(asctime)s %(filename)s %(threadName)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='test.log',
                    filemode='a')

    LOG.debug('This is a debug message')
    LOG.info('This is a info message')
    LOG.warning('This is a warning message')


writeLog()
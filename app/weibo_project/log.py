import logging, time, os

class Log:
    def __init__(self):
        self.path = os.getcwd()
        self.fileName = '/my.log'

    def create(self):
        file = self.path + self.fileName
        if not os.path.exists(file):
            open(file, 'w')

        return file


    def config(self):
        file = self.create()
        DATE_FORMAT = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        LOG_FORMAT = '%(asctime)s - %(levelname)s { %(message)s }'
        logging.basicConfig(level = logging.ERROR,
                            format = LOG_FORMAT,
                            datefmt = DATE_FORMAT,
                            filename = file,
                            filemode = 'a')


    def record(self, info, perfix, message):
        text = info + ' - ' + perfix + ' : ' + message
        logging.error(text)

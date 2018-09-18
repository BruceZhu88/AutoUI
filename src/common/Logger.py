import logging.config
import os

import threading


class MyLog(object):

    log = None
    mutex = threading.Lock()

    def __init__(self, log_name):
        self.log_name = log_name
        log_path = '.\\log'
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        logging.config.fileConfig("./config/logger_{}.conf".format(self.log_name))

    def get_log(self):
        MyLog.log = logging.getLogger(self.log_name)
        '''
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = logging.getLogger(self.log_name)
            MyLog.mutex.release()

        '''

        return MyLog.log

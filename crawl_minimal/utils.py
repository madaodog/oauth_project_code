import logging
import os
from logging.handlers import RotatingFileHandler


class Logger(object):
    # Copied from dnetcrawl
    __loggers = {}

    def __new__(cls, name):
        if name in Logger.__loggers:
            return Logger.__loggers[name]
        else:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            log_format = logging.Formatter("%(asctime)s - %(name)s - [%(levelname)-5.5s]  %(message)s")
            ch = logging.StreamHandler()
            ch.setFormatter(log_format)
            logger.addHandler(ch)
            dnetcrawl_path = os.path.dirname(os.path.realpath(__file__))
            logs_path = os.path.join(dnetcrawl_path, '..', 'logs')
            os.makedirs(logs_path, exist_ok=True)
            fh = RotatingFileHandler(os.path.join(logs_path, '%s.log' % name), maxBytes=(1024*1024*5), backupCount=7)
            fh.setFormatter(log_format)
            logger.addHandler(fh)
            Logger.__loggers[name] = logger
            return logger

    @staticmethod
    def get_logger(name):
        return Logger(name)

''' Logger configuration '''
import logging

class Logger(object):
    ''' Holds iRNBA logger '''
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = object.__new__(Logger)
        return cls.instance

    def __init__(self):
        self.log = None

        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger(__name__)

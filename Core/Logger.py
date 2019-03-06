# Michel Michels
# 05/03/2019
#
# Simple logger

# imports
from datetime import datetime

class Logger(object):
    def wrap(self, message):
        return '[DEBUG][' + str(datetime.now()) + '] ' + message

    def log(self, message):
        print(self.wrap(message))

    
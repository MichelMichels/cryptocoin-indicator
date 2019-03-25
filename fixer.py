import os
from fixerio.client import Fixerio

class Fixer(object):
    def __init__(self):
        self.key = open(os.path.dirname(__file__) + '/fixer.key', 'r').readline()
        fxrio = Fixerio(access_key=self.key)
        self.latest = fxrio.latest(symbols=['USD', 'GBP'])

    def convert(self, base, foreign, amount):
        base_multiplier = 1 if base is 'EUR' else 1 / self.get_multiplier(base)                  
        foreign_multiplier = 1 if foreign is 'EUR' else self.get_multiplier(foreign)
        return amount * base_multiplier * foreign_multiplier
    
    def get_multiplier(self, foreign):
        return float(self.latest['rates'].get(foreign))



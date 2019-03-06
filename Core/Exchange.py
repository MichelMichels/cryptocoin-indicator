# Exchange class module
import sys

class Exchange(object):
    def __init__(self, name, api, logger):
        self.name = name
        self.api = api
        self.logger = logger

    def __str__(self):
        return self.name
    
    def get_price(self, cryptocoin, sell_or_buy = 'sell'):
        raise NotImplementedError

    def get_supported_coins(self):
        raise NotImplementedError
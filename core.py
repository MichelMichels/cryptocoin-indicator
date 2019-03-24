import os
import sys
import requests

from abc import ABC, abstractmethod
from time import sleep
from datetime import datetime

class ApiWrapper(ABC):
    def __init__(self, base_url, logger):
        self.base_url = base_url
        self.logger = logger    
        super().__init__() 

    def get_response(self, endpoint, params = {}, headers = {}):
        response = None
        while response is None:
            try:
                self.logger.log('Initiating api request...')
                response = requests.get(self.base_url + endpoint, headers = headers, params = params)
            except TimeoutError as timeOutError:
                self.logger.log(str(timeOutError))
                self.logger.log('Trying again in 5 seconds...')
                sleep(5)
            except Exception as e:
                self.logger.log('Unexpected error: ' + str(e))
                response = 'NaN'

        return response.json()

class Cryptocoin(object):
    path = os.path.dirname(os.path.realpath(__file__)) + '/'

    def __init__(self, name, api_name, abbr = '', icon = '', round_number = 0):
        self.name = name
        self.abbr = abbr
        self.api_name = api_name
        self.icon = self.path + icon
        self.round_number = round_number

    def deep_copy(self):
        return Cryptocoin(self.name, self.api_name, self.icon, self.round_number)

class Exchange(object):
    def __init__(self, name, logger):
        self.name = name
        self.logger = logger

    def __str__(self):
        return self.name
    
    def get_price(self, cryptocoin, currency = 'USD', sell_or_buy = 'sell'):
        raise NotImplementedError

    def get_supported_coins(self):
        raise NotImplementedError

class Logger(object):
    def wrap(self, message):
        return '[DEBUG][' + str(datetime.now()) + '] ' + message

    def log(self, message):
        print(self.wrap(message))

    
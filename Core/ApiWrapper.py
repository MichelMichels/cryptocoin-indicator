from abc import ABC, abstractmethod
from time import sleep
import sys
import requests

class ApiWrapper(ABC):
    def __init__(self, base_url, logger):
        self.base_url = base_url
        self.logger = logger    
        super().__init__() 

    def get_response(self, endpoint, headers = {}, params = {}):
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


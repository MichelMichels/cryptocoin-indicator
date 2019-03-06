import os
from Core.ApiWrapper import ApiWrapper

class CoinmarketcapApi(ApiWrapper):
    def __init__(self, logger):
        super().__init__('https://pro-api.coinmarketcap.com', logger)
        self.key = open(os.path.dirname(__file__) + '/api.key', 'r').readline()
        self.default_headers = { 'X-CMC_PRO_API_KEY': self.key }
        print(self.default_headers)

    def get_latest_cryptocurrency_quotes(self, id = '', symbol = '', convert = 'EUR'):
        payload = {
            'symbol': symbol, 
            'convert': convert
        }
        return self.get_response('/v1/cryptocurrency/quotes/latest', params=payload, headers=self.default_headers)

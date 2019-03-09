import os
from Core.ApiWrapper import ApiWrapper

class CoinmarketcapApi(ApiWrapper):
    def __init__(self, logger):
        super().__init__('https://pro-api.coinmarketcap.com', logger)
        self.key = open(os.path.dirname(__file__) + '/api.key', 'r').readline()
        self.default_headers = { 'X-CMC_PRO_API_KEY': self.key }
        self.cache_dir = os.path.dirname(__file__) + '/cache'

    def get_metadata(self, symbol):
        endpoint = '/v1/cryptocurrency/info'
        payload = {
            'symbol': symbol
        }
        return self.get_response(endpoint, payload, self.default_headers) 

    def get_coinmarketcap_id_map(self, listing_status = "active", start = 1, limit = 0, symbol = ''):
        endpoint = '/v1/cryptocurrency/map'
        payload = {
            'listing_status':  listing_status,
            'start': start
        }
        if limit != 0:
            payload['limit'] = limit
        if symbol != '':
            payload['symbol'] = symbol

        response = self.get_response(endpoint, payload, self.default_headers)        
        return response

    def get_latest_cryptocurrencies(self, start = 1, limit = 100, convert = 'USD', sort = 'market_cap', sort_dir = 'asc', cryptocurrency_type = 'all'):
        endpoint = '/v1/cryptocurrency/listings/latest'
        payload = {
            'start': start,
            'limit': limit,
            'convert': convert,
            'sort': sort,
            'sort_dir': sort_dir,
            'cryptocurrency_type': cryptocurrency_type,
        }
        return self.get_response(endpoint, payload, self.default_headers)

    def get_latest_market_quotes(self, id = '', symbol = '', convert = 'USD'):
        endpoint = '/v1/cryptocurrency/quotes/latest'
        if id is '' and symbol is '':
            raise ValueError(str) 

        payload = {
            'convert': convert
        }
        if id is not '':
            payload['id'] = id
        if symbol is not '':
            payload['symbol'] = symbol

        return self.get_response(endpoint, payload, self.default_headers)

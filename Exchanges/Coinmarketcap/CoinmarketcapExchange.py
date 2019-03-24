from Exchanges.Coinmarketcap.CoinmarketcapApi import CoinmarketcapApi
from core import Exchange

class CoinmarketcapExchange(Exchange):
    def __init__(self, logger):
        super().__init__('Coinmarketcap', logger)
        self.api = CoinmarketcapApi(logger)

    def get_price(self, cryptocoin, currency):
        response = self.api.get_latest_market_quotes(symbol = cryptocoin) 
        try:
            coin_data = next(iter(response['data'].items()))
            quote_data = coin_data[1]['quote']
            price = next(iter(quote_data.items()))[1]['price']
        except KeyError as keyError:
            self.logger.log('Key not found in response, ' + str(keyError))
            price = 'NaN'
        return str(price)

    def get_supported_coins(self):        
        return []

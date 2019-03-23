from Exchanges.Coinmarketcap.CoinmarketcapApi import CoinmarketcapApi
from core import Exchange

class CoinmarketcapExchange(Exchange):
    def __init__(self, logger):
        self.api = CoinmarketcapApi(logger)
        super().__init__('Coinmarketcap', logger)

    def get_price(self, cryptocoin):
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
        
        pass

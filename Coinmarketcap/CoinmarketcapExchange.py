from Coinmarketcap.CoinmarketcapApi import CoinmarketcapApi
from Core.Exchange import Exchange

class CoinmarketcapExchange(Exchange):
    def __init__(self, logger):
        super().__init__('Coinmarketcap', CoinmarketcapApi(logger), logger)

    def get_price(self, cryptocoin):
        response = self.api.get_latest_cryptocurrency_quotes(symbol = cryptocoin) 
        try:
            coin_data = next(iter(response['data'].items()))
            quote_data = coin_data[1]['quote']
            price = next(iter(quote_data.items()))[1]['price']
        except KeyError as keyError:
            self.logger.log('Key not found in response, ' + str(keyError))
            price = 'NaN'

        return str(price)

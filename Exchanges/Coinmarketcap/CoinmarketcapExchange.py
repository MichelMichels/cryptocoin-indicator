from Exchanges.Coinmarketcap.CoinmarketcapApi import CoinmarketcapApi
from core import Exchange, Cryptocoin

class CoinmarketcapExchange(Exchange):
    def __init__(self, logger):
        super().__init__('Coinmarketcap', logger)
        self.api = CoinmarketcapApi(logger)

    def get_price(self, cryptocoin, currency='EUR'):
        response = self.api.get_latest_market_quotes(symbol = cryptocoin.abbr, convert = currency) 
        try:
            coin_data = next(iter(response['data'].items()))
            quote_data = coin_data[1]['quote']
            price = next(iter(quote_data.items()))[1]['price']            
        except KeyError as keyError:
            self.logger.log('get_price, Key not found in response, ' + str(keyError))
            price = 'NaN'
        return float(price)

    def get_supported_coins(self):  
        response = self.api.get_coinmarketcap_id_map()   
        try:
            coins = response['data']
            return [Cryptocoin(coin['name'], coin['slug'], coin['symbol']) for coin in coins[:100]]
        except KeyError as keyError:
            self.logger.log('get_supported_coins, Key not found in response, ' + str(keyError))      
        return []
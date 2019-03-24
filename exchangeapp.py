#from Exchanges.Coinmarketcap.CoinmarketcapExchange import CoinmarketcapExchange
from Exchanges.LiteBit.LiteBitExchange import LiteBitExchange

class ExchangeApp(object):   
    symbols = {
        'EUR': '€',
        'USD': '$',
        'GBP': '£'
    }

    def __init__(self, logger):
        self.logger = logger
        #self.exchanges = [ LiteBitExchange(logger), CoinmarketcapExchange(logger) ]
        self.exchanges = [ LiteBitExchange(logger) ]
        self.current_exchange = self.exchanges[0]
        self.current_coin = None
        self.current_currency = 'EUR'
        self.current_price = 0

    # Exchange getter/setter
    def set_exchange(self, exchange):
        self.current_exchange = exchange
        self.logger.log('Exchange set to ' + exchange.name)
    def get_exchange(self):
        return self.current_exchange

    # Currency getter/setter
    def set_currency(self, currency):
        self.current_currency = currency
        self.logger.log('Currency set to ' + currency)
        self.update_price()
    def get_currency(self):
        return current_currency

    # Coin getter/setter
    def set_coin(self, coin):
        self.current_coin = coin
        self.logger.log('Coin set to ' + coin.name)
        self.update_price()
    def get_coin(self):
        return self.current_coin

    # Price getter/setter
    def set_price(self, price):
        self.current_price = price
        self.logger.log('Price set to ' + str(price))
    def get_price(self):
        return self.current_price

    def get_all_coins(self):
        return self.current_exchange.get_supported_coins()

    def get_price_label(self):
        return self.get_currency_symbol() + ' ' + str(self.current_price)

    def get_currency_symbol(self):
        try:
            return self.symbols[self.current_currency]
        except KeyError:
            logger.log('Symbol not found of currency ' + self.current_currency)

    def update_price(self):
        price = self.current_exchange.get_price(self.current_coin)
        self.set_price(price)

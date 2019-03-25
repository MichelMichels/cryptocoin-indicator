from Exchanges.LiteBit.LiteBitApi import LiteBitApi
from core import Exchange, Cryptocoin
from fixer import Fixer

class LiteBitExchange(Exchange):
    def __init__(self, logger):
        super().__init__('LiteBit', logger)        
        self.api = LiteBitApi(logger)
        self.fixer = Fixer()    

    def get_price(self, cryptocoin, currency = 'EUR', sell_or_buy = 'sell'):
        response = self.api.get_market(cryptocoin.api_name)

        try:
            price = float(response['result'][sell_or_buy])
            return price if currency is 'EUR' else self.fixer.convert('EUR', currency, price)
        except KeyError as keyError:
            self.logger.log('Key not found in JSON response!' + str(keyError))
        except TypeError as typeError:
            self.logger.log('Unknown response. ' + str(typeError))
        return 0

    def get_supported_coins(self):
        response = self.api.get_markets()
        return [Cryptocoin(coin_data['name'], coin_api_code, coin_api_code.upper()) for coin_api_code, coin_data in response['result'].items()]


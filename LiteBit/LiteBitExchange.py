from LiteBit.LiteBitApi import LiteBitApi
from Core.Exchange import Exchange

class LiteBitExchange(Exchange):
    def __init__(self, logger):
        super().__init__('LiteBit', LiteBitApi(logger), logger)

    def get_price(self, cryptocoin, sell_or_buy = 'sell'):
        response = self.api.get_market(cryptocoin)

        try:
            return response['result'][sell_or_buy]
        except KeyError as keyError:
            self.logger.log('Key not found in JSON response!' + str(keyError))
        except TypeError as typeError:
            self.logger.log('Unknown response. ' + str(typeError))
        return 'NaN'

    def get_supported_coins(self):
        response = self.api.get_markets()
        return dict([(coin_data['name'], coin_api_code) for coin_api_code, coin_data in response['result'].items()])


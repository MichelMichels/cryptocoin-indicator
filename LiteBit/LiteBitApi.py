from Core.ApiWrapper import ApiWrapper

class LiteBitApi(ApiWrapper):
    def __init__(self, logger):
        super().__init__('https://api.litebit.eu/', logger)

    def get_markets(self):
        return self.get_response('markets')

    def get_market(self, cryptocoin):
        return self.get_response('market/' + cryptocoin)       
        
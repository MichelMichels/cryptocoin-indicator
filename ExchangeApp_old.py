
class ExchangeApp(object):
    #coinmarketcap = CoinmarketcapExchange("Coinmarketcap.com", "https://api.coinmarketcap.com/v1/ticker/", '/?convert=EUR')
    #litebit = LiteBitExchange("LiteBit.eu", "https://www.litebit.eu/requests/jsonp.php?call=")

    #exchange_list = []
    #exchange_list.append(coinmarketcap)
    #exchange_list.append(litebit)

    dogecoin = Cryptocoin('Dogecoin', 'dogecoin', 'icons/doge.png', 5)
    bitcoin = Cryptocoin('Bitcoin', 'bitcoin', 'icons/bitcoin.png', 2)
    navcoin = Cryptocoin('Navcoin', 'nav-coin', 'icons/navcoin.png', 4)
    litecoin = Cryptocoin('Litecoin', 'litecoin', 'icons/litecoin.png', 2)
    ethereum = Cryptocoin('Ethereum', 'ethereum', 'icons/ethereum.png', 2)
    ripple = Cryptocoin('Ripple', 'ripple', 'icons/ripple.png', 4)
    nem = Cryptocoin('NEM', 'nem', 'icons/nem.png', 4)
    ethereum_classic = Cryptocoin('Ethereum Classic', 'ethereum-classic', 'icons/etc.png', 2)
    dash = Cryptocoin('Dash', 'dash', 'icons/dash.png', 2)
    monero = Cryptocoin('Monero', 'monero', 'icons/monero.png', 2)
    stratis = Cryptocoin('Stratis', 'stratis', 'icons/stratis.png', 3)
    bytecoin = Cryptocoin('Bytecoin', 'bytecoin-bcn', 'icons/bytecoin.png', 5)
    artbyte = Cryptocoin('ArtByte', 'artbyte', 'icons/artbyte.png', 6)

    cc_list = []
    cc_list.append(artbyte)
    cc_list.append(bitcoin)
    cc_list.append(bytecoin)
    cc_list.append(dash)
    cc_list.append(dogecoin)
    cc_list.append(ethereum)
    cc_list.append(ethereum_classic)
    cc_list.append(litecoin)
    cc_list.append(monero)
    cc_list.append(navcoin)
    cc_list.append(nem)
    cc_list.append(ripple)
    cc_list.append(stratis)

    def __init__(self):
        self.current_exchange = self.coinmarketcap
        self.currency = 'EUR'
        self.current_cryptocoin = self.dogecoin

    def set_exchange(self, source, new_exchange):
        if source.get_active():
            self.current_exchange = new_exchange
            self.update_price('set_exchange()')
            print(GetDebugText() + 'Exchange changed to ' + new_exchange.name)

    def get_exchange(self):
        return self.current_exchange

    def set_currency(self, source, new_currency):
        if source.get_active():    
            print(GetDebugText() + 'Currency changed to ' + new_currency)
            self.currency = new_currency
            self.update_price('set_currency()')

    def set_cryptocoin(self, source, new_cryptocoin):
        if source.get_active():
            self.current_cryptocoin = new_cryptocoin
            indicator.set_icon(self.current_cryptocoin.icon)
            self.update_price('set_cryptocoin()')
            print(GetDebugText() + 'Cryptocoin changed to ' + self.current_cryptocoin.name)
                    
    def update_price(self, source):
        # Set menu items inactive during price update
        menu = indicator.get_menu().get_children()
        for menu_item in menu:
            if menu_item.get_label() != 'Quit':
                menu_item.set_sensitive(False)

        print(GetDebugText() + 'update_price() received call from ' + str(source))

        cc_price = self.current_exchange.get_price(self.current_cryptocoin, self.currency)
        print(GetDebugText() + 'Price updated from ' + self.current_exchange.name)

        #if self.current_cryptocoin.name == 'Dogecoin':
        #    cc_price = cc_price * 1000

        # Set the new label
        if self.currency == "EUR":
            indicator.set_label('€ ' + str(cc_price), "100%")
        elif self.currency == "USD":
            indicator.set_label('$ ' + str(cc_price), "100%")
        else:
            indicator.set_label('DOGE', "100%")

        # Reactivate menu items
        # Set menu items inactive during price update
        menu = indicator.get_menu().get_children()
        for menu_item in menu:
            if menu_item.get_label() != 'Quit':
                menu_item.set_sensitive(True)

        return True

    def first_update_price(self, source):
        self.update_price("first_update_price()")
        return False

#!/usr/bin/env python3
#title           : cryptocoin_appindicator.py
#description     : Indicator for the Unity (and gnome) shell for several cryptocoins
#author          : Michel Michels
#date            : 20170531
#version         : 1.0.2
#usage           : nohup python3 cryptocoin_appindicator.py &
#notes           : Can also be run with debug output with 'python3 cryptocoin_appindicator.py'. This project uses the litebit.eu and coinmarketcap.com API.
#python_version  : 3.5.3
#==============================================================================


# IMPORTS
import os, sys, signal
import requests
from datetime import datetime
from decimal import *
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import GObject as gobject
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'dogecoinpriceindicator'

def GetDebugText():
    return '[DEBUG][' + str(datetime.now()) + '] '

class Cryptocoin(object):
    path_of_script = os.path.dirname(os.path.realpath(__file__)) + '/'

    def __init__(self, name, api_name, icon, round_number):
        self.name = name
        self.api_name = api_name
        self.icon = self.path_of_script + icon
        self.round_number = round_number

    def deep_copy(self):
        return Cryptocoin(self.name, self.api_name, self.icon, self.round_number)

class Exchange(object):
    def __init__(self, name, api_base_url, api_end = ''):
        self.name = name
        self.api_base_url = api_base_url
        self.api_end = api_end

    def __str__(self):
        return self.name

    def get_json_object(self, cryptocoin):
        result = None
        while result is None:
            try:
                print(GetDebugText() + 'Initiating api request with timeout of 5 seconds...')
                result = requests.get(self.api_base_url + cryptocoin.api_name + self.api_end, timeout = 5)
            except:
                print(GetDebugText() + 'Unexpected error: ', sys.exc_info()[0])
                pass
        return result.json()

class LiteBitExchange(Exchange):
    supported_cc = [
        'Dogecoin', 
        'Bitcoin', 
        'Navcoin', 
        'Litecoin', 
        'Ethereum', 
        'Ripple', 
        'NEM', 
        'Ethereum Classic', 
        'Dash', 
        'Monero', 
        'Stratis',
        'ArtByte'
    ]

    def get_price(self, cryptocoin, currency):
        if cryptocoin.name in self.supported_cc:
            copycoin = cryptocoin.deep_copy()

            # Icon api name fixes
            if cryptocoin.api_name == 'nav-coin':
                copycoin.api_name = 'nav'
            elif cryptocoin.api_name == 'ethereum-classic':
                copycoin.api_name = 'etc'


            # GET response and create JSON object
            json_obj = super().get_json_object(copycoin)

            price = json_obj['sell']
            price = price.replace(',', '')

            if currency == 'USD':
                json_eur = requests.get('http://api.fixer.io/latest').json()
                return round(Decimal(float(price) * json_eur["rates"]["USD"]), cryptocoin.round_number)

            # Return eur price
            elif currency == 'EUR':
                return round(Decimal(price), cryptocoin.round_number)
        else:
            return 'CC not supported'

class CoinmarketcapExchange(Exchange):
    supported_cc = [
        'Dogecoin', 
        'Bitcoin', 
        'Navcoin', 
        'Litecoin', 
        'Ethereum', 
        'Ripple', 
        'NEM', 
        'Ethereum Classic', 
        'Dash', 
        'Monero', 
        'Stratis',
        'Bytecoin',
        'ArtByte'
    ]

    def get_price(self, cryptocoin, currency):
        if cryptocoin.name in self.supported_cc:
            copycoin = cryptocoin.deep_copy()

            # Icon api name fixes
            if cryptocoin.api_name == 'artbyte':
                copycoin.api_name = 'applebyte'

            # GET json object
            json_obj = super().get_json_object(copycoin)

            if currency == 'USD':
                return round(Decimal(json_obj[0]['price_usd']), cryptocoin.round_number)
            elif currency == 'EUR':
                return round(Decimal(json_obj[0]['price_eur']), cryptocoin.round_number)
        else:
            return 'CC not supported'

class ExchangeApp(object):
    coinmarketcap = CoinmarketcapExchange("Coinmarketcap.com", "https://api.coinmarketcap.com/v1/ticker/", '/?convert=EUR')
    litebit = LiteBitExchange("LiteBit.eu", "https://www.litebit.eu/requests/jsonp.php?call=")

    exchange_list = []
    exchange_list.append(coinmarketcap)
    exchange_list.append(litebit)

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

class Gui(object):
    # Logic
    exchange_app = ExchangeApp()

    def __init__(self):
        # Applet icon
        global indicator
        indicator = appindicator.Indicator.new(APPINDICATOR_ID, self.exchange_app.dogecoin.icon, appindicator.IndicatorCategory.SYSTEM_SERVICES)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_label('€ *.****', '100%')

        # Set the menu of the indicator (default: gtk.Menu())
        indicator.set_menu(self.build_menu())

        # Ctrl-C behaviour
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Setup the refresh every 5 minutes
        gobject.timeout_add(1000*60*5, self.exchange_app.update_price, "timeout")

        # First price update within 1 second
        gobject.timeout_add(1000, self.exchange_app.first_update_price, "first_update")

        # Main loop
        gtk.main()

    def build_menu(self):
        # Create menu object
        menu = gtk.Menu()

        # Create menuitem objects
        item_update_price = gtk.MenuItem('Update price')

        ######## CRYPTOCOINS ########
        item_radio_cc_list = []

        # Iteratie Exchange objects and make radio buttons
        for cc in self.exchange_app.cc_list:
            item_radio_cc_list.append(gtk.RadioMenuItem(cc.name))

        # Set group property for the radio buttons
        for index in range(1, len(item_radio_cc_list)):
            item_radio_cc_list[index].set_property('group', item_radio_cc_list[0])

        # Set dogecoin active
        for item_radio_cc in item_radio_cc_list:
            if item_radio_cc.get_label() == self.exchange_app.dogecoin.name:
                item_radio_cc.set_active(True)

        for x in range(0, len(item_radio_cc_list)):
            item_radio_cc_list[x].connect('activate', self.exchange_app.set_cryptocoin, self.exchange_app.cc_list[x])

        ######## EXCHANGES ########
        item_radio_exchange_list = []

        # Iteratie Exchange objects and make radio buttons
        for exchange in self.exchange_app.exchange_list:
            item_radio_exchange_list.append(gtk.RadioMenuItem(exchange.name))

        # Set group property for the radio buttons
        for index in range(1, len(item_radio_exchange_list)):
            item_radio_exchange_list[index].set_property('group', item_radio_exchange_list[0])

        # Set the first item active
        item_radio_exchange_list[0].set_active(True)

        for x in range(0, len(item_radio_exchange_list)):
            item_radio_exchange_list[x].connect('activate', self.exchange_app.set_exchange, self.exchange_app.exchange_list[x])

        ######## CURRENCY ########
        item_radio_eur = gtk.RadioMenuItem('EUR (€)')
        item_radio_usd = gtk.RadioMenuItem('USD ($)')
        item_radio_usd.set_property('group', item_radio_eur)

        # Set active radio buttons
        item_radio_eur.set_active(True)

        item_radio_eur.connect("activate", self.exchange_app.set_currency, 'EUR')
        item_radio_usd.connect("activate", self.exchange_app.set_currency, 'USD')

        ######## ABOUT ##############
        item_about = gtk.MenuItem('About')

        ######## QUIT ########
        item_quit = gtk.MenuItem('Quit')

        # Connect to quit() method
        item_update_price.connect('activate', self.exchange_app.update_price)
        item_about.connect('activate', self.about_window)
        item_quit.connect('activate', quit)


        ######## APPEND TO MENU ########
        menu.append(item_update_price)

        menu.append(gtk.SeparatorMenuItem())
        for cc in item_radio_cc_list:
            menu.append(cc)

        menu.append(gtk.SeparatorMenuItem())
        # Append all exchanges with for loop
        for exchange in item_radio_exchange_list:
            menu.append(exchange)

        menu.append(gtk.SeparatorMenuItem())
        menu.append(item_radio_eur)
        menu.append(item_radio_usd)

        menu.append(gtk.SeparatorMenuItem())
        menu.append(item_about)
        menu.append(item_quit)

        # Show menu
        menu.show_all()

        # Return the created menu object
        return menu

    def about_window(self, source):
        dialog = gtk.AboutDialog()

        dialog.set_program_name('Cryptocoin Price Indicator')
        dialog.set_version('1.0.2')
        dialog.set_copyright('Copyright 2017 Michel Michels')
        dialog.set_license('MIT License\nCopyright (c) 2017 Michel Michels\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.')
        dialog.set_wrap_license(True)
        dialog.set_comments('This application is written in Python 3.5.3 and currently tested on systems using the Unity shell.')
        dialog.set_website('https://github.com/MichelMichels/cryptocoin-indicator')
        
        dialog.run()
        dialog.destroy()

    def quit(self, source):
        gtk.main_quit()

def main():
    # Set precision
    getcontext().prec = 8

    # Launch app
    Gui()

if __name__ == "__main__":
    main()
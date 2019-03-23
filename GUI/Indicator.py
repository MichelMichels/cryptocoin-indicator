APP_NAME = "CoinIndicator"

import sys
import signal

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import AppIndicator3

from Exchanges.LiteBit.LiteBitExchange import LiteBitExchange
from Exchanges.Coinmarketcap.CoinmarketcapExchange import CoinmarketcapExchange

class Indicator(object):
    def __init__(self, logger):
        self.logger = logger
        logger.log('Indicator constructor')

        self.app = AppIndicator3.Indicator.new(APP_NAME, '', AppIndicator3.IndicatorCategory.APPLICATION_STATUS) 
        self.app.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.app.set_label('DEBUG', 'NaN') 
        
        self.exchanges = [ LiteBitExchange(logger), CoinmarketcapExchange(logger) ]
        self.current_exchange = self.exchanges[0]

        self.build_menu()
        
        # Ctrl-C behaviour        
        signal.signal(signal.SIGINT, signal.SIG_DFL)      

    def start(self):
        Gtk.main()     

    def build_menu(self):       
        self.menu = Gtk.Menu()
        
        self.add_exchanges()
        self.add_coins()
        self.add_currencies()        
        self.add_separator()
        self.add_quit()

        self.menu.show_all()
        self.app.set_menu(self.menu)
    
    def add_exchanges(self):
        self.submenu_exchanges = Gtk.Menu()
        previtem = None
        for exchange in self.exchanges:
            item = Gtk.RadioMenuItem(label=exchange.name, group=previtem)
            item.connect('activate', self.exchange_changed, exchange)
            self.submenu_exchanges.append(item)
            previtem = item

        self.item_exchange = Gtk.MenuItem('Price source')
        self.item_exchange.set_submenu(self.submenu_exchanges)
        self.menu.append(self.item_exchange)

    def add_coins(self):
        self.item_coin = Gtk.MenuItem('Cryptocoin')
        self.menu.append(self.item_coin)        

    def add_currencies(self):
        self.item_currency = Gtk.MenuItem('Currency')
        self.menu.append(self.item_currency)

    def add_quit(self):
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', quit)
        self.menu.append(item_quit)

    def add_separator(self):
        self.menu.append(Gtk.SeparatorMenuItem())    

    def exchange_changed(self, source, exchange):
        self.current_exchange = exchange
        self.logger.log('Exchange changed to ' + self.current_exchange.name + ' from ' + str(source)) 

    def quit(self):
        Gtk.main_quit()

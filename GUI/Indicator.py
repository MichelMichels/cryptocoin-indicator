APP_NAME = "CoinIndicator"

import sys, os, threading
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import AppIndicator3

from Exchanges.LiteBit.LiteBitExchange import LiteBitExchange
from Exchanges.Coinmarketcap.CoinmarketcapExchange import CoinmarketcapExchange

class Indicator(object):
    def __init__(self, logic, logger):
        self.logic = logic
        self.logger = logger
        logger.log('Indicator constructor')

        self.init_statusicon()        
        self.build_menu()
        
        self.update_coins()
        self.refresh_icon()
        self.refresh_price_label() 
        self.reset_timer()

    def init_statusicon(self):
        self.icon = AppIndicator3.Indicator.new(APP_NAME, '', AppIndicator3.IndicatorCategory.APPLICATION_STATUS) 
        self.icon.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.icon.set_label('Loading...', '')
        self.icon.set_icon('gnome-run')

    def start(self):
        Gtk.main()     

    def build_menu(self):       
        self.menu = Gtk.Menu()
        
        self.add_exchanges()
        self.add_coins()
        self.add_currencies()        
        self.add_separator()
        self.add_quit()

        self.draw_menu()
        self.icon.set_menu(self.menu)        
    
    def add_exchanges(self):
        self.submenu_exchanges = Gtk.Menu()
        previtem = None
        for exchange in self.logic.exchanges:
            item = Gtk.RadioMenuItem(label=exchange.name, group=previtem)
            item.connect('toggled', self.exchange_changed, exchange)
            self.submenu_exchanges.append(item)
            previtem = item

        self.item_exchange = Gtk.MenuItem('Price source')
        self.item_exchange.set_submenu(self.submenu_exchanges)
        self.menu.append(self.item_exchange)

    def add_coins(self):
        self.item_coin = Gtk.MenuItem('Cryptocoin')
        self.menu.append(self.item_coin)        

    def update_coins(self):
        coins = self.logic.get_all_coins()
        self.logger.log('Coins updated! ' + str(len(coins)))
        
        submenu = Gtk.Menu()
        previtem = None
        for coin in coins:
            item = Gtk.RadioMenuItem(label=coin.abbr + ' | ' + coin.name, group=previtem)
            item.connect('toggled', self.coin_changed, coin)
            submenu.append(item)
            previtem = item
        self.item_coin.set_submenu(submenu)
        self.logic.set_coin(coins[0])
        self.draw_menu()

    def add_currencies(self):
        submenu = Gtk.Menu()
        previtem = None
        #for currency in ['USD', 'EUR', 'GBP']:
        for currency in ['EUR']:
            item = Gtk.RadioMenuItem(label=currency, group=previtem)
            item.connect('toggled', self.currency_changed, currency)
            submenu.append(item)
            previtem = item

        self.item_currency = Gtk.MenuItem('Currency')
        self.item_currency.set_submenu(submenu)
        self.menu.append(self.item_currency)

    def add_quit(self):
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', quit)
        self.menu.append(item_quit)

    def add_separator(self):
        self.menu.append(Gtk.SeparatorMenuItem())    

    # Toggled signal handlers
    def exchange_changed(self, source, exchange):
        if source.get_active():
            self.logic.set_exchange(exchange)
            self.update_coins()        
    def currency_changed(self, source, currency):
        if source.get_active():
            self.logic.set_currency(currency)
            self.refresh_price_label()    
    def coin_changed(self, source, coin):
        if source.get_active():
            self.logic.set_coin(coin)
            self.refresh_icon()
            self.refresh_price_label()

    def refresh_price_label(self):
        label = self.logic.get_price_label()
        self.icon.set_label(' ' + label, '') 
        self.reset_timer()

    def refresh_icon(self):
        coin = self.logic.get_coin()
        png = str(Path(__file__).parent.parent / ('Icons/' + coin.abbr.lower() + '.png'))
        self.icon.set_icon(png)  

    def reset_timer(self):
        self.timer = threading.Timer(300.0, self.refresh_price_label)
        self.timer.start()

    def draw_menu(self):
        self.menu.show_all()

    def quit(self):
        self.timer.stop()
        Gtk.main_quit()

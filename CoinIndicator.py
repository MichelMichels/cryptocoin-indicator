#!/usr/bin/env python3
#title           : CoinIndicator.py
#description     : Price indicator for GTK3
#author          : Michel Michels
#date            : 20190306
#version         : 0.2.0
#usage           : nohup python3 cryptocoin_appindicator.py &
#notes           : Can also be run with debug output with 'python3 cryptocoin_appindicator.py'. This project uses the litebit.eu and coinmarketcap.com API.
#python_version  : 3.6.7
#==============================================================================

import os, sys, signal
import requests
#import gi
#gi.require_version('Gtk', '3.0')
#from gi.repository import Gtk as gtk
from Core.Logger import Logger
from LiteBit.LiteBitExchange import LiteBitExchange
from Coinmarketcap.CoinmarketcapExchange import CoinmarketcapExchange


def main():
    logger = Logger()
    litebit = LiteBitExchange(logger)   
    coins = litebit.get_supported_coins()
    btc_price = litebit.get_price('btc')
    logger.log('Bitcoin price: ' + btc_price + ' euro')

if __name__ == "__main__":
    main()
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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from Core.Logger import Logger
from LiteBit.LiteBitExchange import LiteBitExchange
from Coinmarketcap.CoinmarketcapExchange import CoinmarketcapExchange


def main():
    logger = Logger()
    litebit = LiteBitExchange(logger)   
    coinmarketcap = CoinmarketcapExchange(logger) 

    logger.log('Bitcoin selling price on LiteBit.eu is ' + litebit.get_price('btc') + ' euro.')
    logger.log('Bitcoin selling price on CoinmarketCap.com is ' + coinmarketcap.get_price('BTC') + ' euro.')

if __name__ == "__main__":
    main()
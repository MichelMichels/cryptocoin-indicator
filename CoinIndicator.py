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

from Core.Logger import Logger
from Exchanges.Coinmarketcap.CoinmarketcapExchange import CoinmarketcapExchange
from Exchanges.LiteBit.LiteBitExchange import LiteBitExchange
from GUI.gui import GUI
       
def main():
    logger = Logger()
    gui = GUI()
    gui.start()

if __name__ == "__main__":
    main()
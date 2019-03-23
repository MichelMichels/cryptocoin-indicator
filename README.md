# Cryptocoin price statusbar widget
## WARNING
The project is currently undergoing a lot of maintenance as I refractored the whole codebase. It will be up and running soon.

## Introduction
I was searching for an indicator on the price of several cryptocoins so I didn't need to refresh the pages of exchanges everytime I wanted to know what the value of a certain coin was. I was astounded as I found nobody had created such application, so I wrote one myself.

## The application
!['screenshot of the app indicator'](http://i.imgur.com/smxXboK.png)

The application itself is a rather simple program written in python 3.5.3. At this time, the app uses 2 APIs. One from LiteBit.eu and one from coinmarketcap.com. However, if there's interest in this application, I will add more. You have to option to manually update the price with the "Update price" menu item, but the price also refreshes every 5 minutes.

You can also run multiple instances next to eachother.

Following coins are currently supported:
+ Bitcoin
+ Dogecoin <sup>hi there fellow shibes! To the moon!</sup>
+ Ethereum
+ Litecoin
+ Navcoin

More will follow.

## Dependencies
### Python libraries
The python application uses the 'requests' library. This library can be easily installed using pip.

## Supported Linux distros
### Ubuntu 17.04 (Unity)
The appindicator runs out of the box on Ubuntu 17.04 with a Unity shell. Multiple instances can be run next to eachother without any problem.

## Running the app
You can run this application without debug messages with following command in a terminal:
```bash
nohup python3 /path/to/cryptocoin_indicator.py &
```
If you want to see the debug messages, run following command:
```bash
python3 /path/to/cryptocoin_indicator.py
```

## To Do
+ Support launch arguments (exchange, cryptocoin, refreshrate, ...)
+ Support launch variables in text file (exchange, cryptocoin, refreshrate, ...)
+ Add more coins

## Changelog
### 1.0.2 - 01/06/2017
+ Bug fix: path of icon fixed
+ Fix: Linux Mint Cinnamon update
+ Support for Ripple, NEM, Ethereum Classic, Dash, Monero, Stratis, Bytecoin
+ About dialog added
+ MIT license

### 1.0.1 - 31/05/2017
+ Bug fix: shallow copy instead of deep copy with Cryptocoin class

### 1.0.0 - 31/05/2017
+ Initial release
+ Support for BTC, ETH, DOGE, NAV, LTC
+ Support for Coinmarketcap.com, LiteBit.eu

## Donations
If one would feel so inclined to donate to me, I listed various cryptocoin addresses of mine here. This is completely optional and in no way should you feel pressured to donate.
+ Bitcoin: 1JrKqYxQY8yj4Y5XefBfXhVdbZwuKhCL9C
+ Dogecoin: DJvGm7iyhxdNrySzKK7d5kiYtKpAeYcQS7
+ Navcoin: NgiKR1b9cUTrnTJyQ8Dy4F24DECLnih3Ni

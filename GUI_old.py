
class Gui(object):
    # Logic
    exchange_app = ExchangeApp()

    def __init__(self):
        pass
        # Applet icon
        #global indicator
        #indicator = appindicator.Indicator.new(APPINDICATOR_ID, self.exchange_app.dogecoin.icon, appindicator.IndicatorCategory.SYSTEM_SERVICES)
        #indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        #indicator.set_label('€ *.****', '100%')

        # Set the menu of the indicator (default: gtk.Menu())
        #indicator.set_menu(self.build_menu())

        # Ctrl-C behaviour
        #signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Setup the refresh every 5 minutes
        #gobject.timeout_add(1000*60*5, self.exchange_app.update_price, "timeout")

        # First price update within 1 second
        #gobject.timeout_add(1000, self.exchange_app.first_update_price, "first_update")

        # Main loop
        #gtk.main()

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

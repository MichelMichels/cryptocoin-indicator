import os

class Cryptocoin(object):
    path_of_script = os.path.dirname(os.path.realpath(__file__)) + '/'

    def __init__(self, name, api_name, icon, round_number):
        self.name = name
        self.api_name = api_name
        self.icon = self.path_of_script + icon
        self.round_number = round_number

    def deep_copy(self):
        return Cryptocoin(self.name, self.api_name, self.icon, self.round_number)
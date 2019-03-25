from __future__ import unicode_literals

import datetime

try:
    from urllib.parse import urljoin
except ImportError:  # For Python 2
    from urlparse import urljoin  # noqa

import requests

from .exceptions import FixerioException

BASE_URL = 'http://data.fixer.io/api/'

LATEST_PATH = 'latest'


class Fixerio(object):
    """ A client for Fixer.io. """

    def __init__(self, access_key, symbols=None):
        """
        :param access_key: your API Key.
        :type access_key: str or unicode
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        """
        self.access_key = access_key
        self.symbols = symbols

    def _create_payload(self, symbols):
        """ Creates a payload with no none values.

        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :return: a payload.
        :rtype: dict
        """
        payload = {'access_key': self.access_key}
        if symbols is not None:
            payload['symbols'] = ','.join(symbols)

        return payload

    def latest(self, symbols=None):
        """ Get the latest foreign exchange reference rates.

        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :return: the latest foreign exchange reference rates.
        :rtype: dict
        :raises FixerioException: if any error making a request.
        """
        try:
            symbols = symbols or self.symbols
            payload = self._create_payload(symbols)

            url = BASE_URL + LATEST_PATH

            response = requests.get(url, params=payload)

            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as ex:
            raise FixerioException(str(ex))

    def historical_rates(self, date, symbols=None):
        """
        Get historical rates for any day since `date`.

        :param date: a date
        :type date: date or str
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :return: the historical rates for any day since `date`.
        :rtype: dict
        :raises FixerioException: if any error making a request.
        """
        try:
            if isinstance(date, datetime.date):
                # Convert date to ISO 8601 format.
                date = date.isoformat()

            symbols = symbols or self.symbols
            payload = self._create_payload(symbols)

            url = BASE_URL + date

            response = requests.get(url, params=payload)

            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as ex:
            raise FixerioException(str(ex))

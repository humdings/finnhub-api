import os
import pandas as pd

from finnhub_api.utils import RequestCache


class FinnHubOptionChain(RequestCache):
    """
    Wrapper class for option chain data returned
    by FinnHubs api.
    """

    def __init__(self, data):
        super(FinnHubOptionChain, self).__init__(data)
        self.chain = data['data']
        self.expirations = [i['expirationDate'] for i in self.chain]
        self._frame = None

    def __repr__(self):
        return '<{} OptionChain: {}>'.format(self.underlying_symbol, self.download_date.isoformat())

    @property
    def underlying_symbol(self):
        return self.data['code']

    @property
    def underlying_price(self):
        return self.data['lastTradePrice']

    @property
    def underlying_last_trade_date(self):
        return self.data['lastTradeDate']

    @property
    def exchange(self):
        return self.data['exchange']

    def make_unique_filename(self):
        return '_'.join([
            self.underlying_symbol,
            self.download_date.isoformat() + '.json'
        ])

    def to_json(self, filepath):
        """
        Alter this to accept a directory and generate
        a the filename on the fly.

        :param filepath: Directory or filename where the data is stored.
        :return: None
        """
        if os.path.isdir(filepath):
            filepath = os.path.join(filepath, self.make_unique_filename())
        super(FinnHubOptionChain, self).to_json(filepath)

    def to_frame(self):
        if self._frame is None:
            self._frame = pd.DataFrame(self.to_list())
        return self._frame

    def to_list(self):
        all_opts = []
        for expiry_chain in self.chain:
            opts = expiry_chain['options']
            for side in opts:
                all_opts.extend(opts[side])
        return all_opts

    def get_expiry(self, expiry):
        for opts in self.chain:
            if opts['expirationDate'] == expiry:
                return opts['options']
        raise ValueError('Invalid expiry. valid dates = {}'.format(self.expirations))

    def _get_side(self, expiry, side):
        opts = self.get_expiry(expiry)
        return opts[side]

    def get_calls(self, expiry):
        """
        Get a dataframe of calls for an expiration.
        Dataframe is indexed by strike

        :param expiry: str, date
        :return: pandas.DataFrame
        """
        opts = self._get_side(expiry, 'CALL')
        df = pd.DataFrame(opts)
        df.index = df.strike
        return df

    def get_puts(self, expiry):
        """
        Get a dataframe of puts for an expiration.
        Dataframe is indexed by strike

        :param expiry: str, date
        :return: pandas.DataFrame
        """
        opts = self._get_side(expiry, 'PUT')
        df = pd.DataFrame(opts)
        df.index = df.strike
        return df

    def all_calls(self):
        calls = []
        for expiry_chain in self.chain:
            opts = expiry_chain['options']
            if 'CALL' in opts:
                calls.extend(opts['CALL'])
        return calls

    def all_puts(self):
        puts = []
        for expiry_chain in self.chain:
            opts = expiry_chain['options']
            if 'PUT' in opts:
                puts.extend(opts['PUT'])
        return puts

    def get_option(self, expiry, side, strike):
        """ Get a single option row """
        if side.upper() == 'CALL':
            opts = self.get_calls(expiry)
        elif side.upper() == 'PUT':
            opts = self.get_puts(expiry)
        else:
            raise ValueError('Invalid Option Side: {}'.format(side))
        return opts.loc[strike]

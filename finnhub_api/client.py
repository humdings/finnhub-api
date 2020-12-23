import pandas as pd
from finnhub_api.base import FinnHubBase
from finnhub_api.options import FinnHubOptionChain
from finnhub_api.utils import multicall, get_finnhub_api_key


class FinnHubClient(FinnHubBase):

    def __init__(self, api_key=None, env=None):
        if api_key is None:
            api_key = get_finnhub_api_key(env=env)
        super(FinnHubClient, self).__init__(api_key=api_key)

    def get_stock_option_chain(self, symbol):
        opts = super(FinnHubClient, self).get_stock_option_chain(symbol)
        return FinnHubOptionChain(opts)

    def get_stock_option_chain_multi(self, symbols):
        return multicall(
            self.get_stock_option_chain,
            symbols
        )

    def get_stock_earnings(self, symbol):
        earnings = super(FinnHubClient, self).get_stock_earnings(symbol)
        df = pd.DataFrame(earnings)
        df.index = df.pop('period')
        return df.sort_index()

    def get_stock_earnings_multi(self, symbols):
        return multicall(
            self.get_stock_earnings,
            symbols
        )

    def get_stock_candles_multi(self, symbols, resolution='D', count=250):
        return multicall(
            self.get_stock_candles,
            symbols,
            resolution=resolution,
            count=count,
        )

from functools import wraps
import pandas as pd


def ohlcv_frame(func):
    """
    Decorator to return a Pandas.DataFrame for candle data.
    """

    @wraps(func)
    def _wrapper(*args, **kwargs):
        bars = func(*args, **kwargs)
        df = pd.DataFrame(bars)
        df.index = df.pop('t').apply(pd.Timestamp.fromtimestamp)
        df = df.tz_localize('utc')
        return df

    return _wrapper


def economic_data_frame(func):
    """
    Decorator to return a Pandas.DataFrame for economic data.
    """

    @wraps(func)
    def _wrapper(self, code):
        data = func(self, code)
        df = pd.DataFrame(data).set_index('date')
        df.index = pd.DatetimeIndex(df.index).tz_localize('utc')
        return df.sort_index()

    return _wrapper

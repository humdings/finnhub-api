import os
import json
import pandas as pd
import multitasking

multitasking.set_max_threads(multitasking.config["CPU_CORES"] * 5)


def multicall(func, params, *args, **kwargs):
    """
    Calls the same api function several times
    at once and waits until all tasks complete
    before returning.

    :param func: (callable) api method to call
    :param params: (iterable) list of parameters for the api call (usually symbols).
    :param args, kwargs: Additional positional and keyword args passed to func.

    :returns dictionary
        {parameter: api result}
    """

    @multitasking.task
    def _multitask(out, func, param, *args, **kwargs):
        """
        Inner function that populates the returned dictionary.
        """
        result = func(param, *args, **kwargs)
        out[param] = result

    out = {}
    for param in params:
        _multitask(
            out, func, param, *args, **kwargs
        )
    multitasking.wait_for_tasks()
    return out


def get_finnhub_api_key(env=None):
    if env is None:
        env = os.environ
    return env.get('FINNHUB_API_KEY', None)


def get_formatted_dates(start_date=None, end_date=None, lookback_days=7):
    """
    Returns start and end dates for queries with dates in the proper format
    Default dates are one week ago until today.
    """

    if end_date is None:
        end_date = pd.Timestamp.utcnow().strftime('%Y-%m-%d')
    if start_date is None:
        start_date = (
                pd.Timestamp(end_date) - pd.Timedelta(days=lookback_days)
        ).strftime('%Y-%m-%d')
    # Ensure proper date string parameters
    start_date = pd.Timestamp(start_date).strftime('%Y-%m-%d')
    end_date = pd.Timestamp(end_date).strftime('%Y-%m-%d')
    return start_date, end_date


class RequestCache(object):
    """
    Class to simplify saving and reloading requests in json format.
    """

    def __init__(self, data=None):
        if data is None:
            data = {}
        self._data = data
        # Inject the original download time if the data was not loaded from a file
        if '_download_date' not in data:
            data['_download_date'] = pd.Timestamp.utcnow().isoformat()

    @property
    def data(self):
        return self._data

    @property
    def download_date(self):
        return pd.Timestamp(self.data['_download_date'])

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls(data)

    def to_json(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self._data, f)

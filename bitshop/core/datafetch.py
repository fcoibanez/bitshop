import snippets.basic_operations as bo
import requests
import math
from random import uniform
import pandas as pd
from datetime import datetime, timedelta
import time
from tqdm import tqdm


# -----------------------------------------------------------------------
# DataFetch class
class DataFetch:
    """
    Object that handles the communication with the API to fetch historical and current data.

    :param api_keys: Dictionary containing the public key ('public'), private key ('private'), and
    the API password ('pass').
    """
    def __init__(self, api_keys):
        self.keys = api_keys
        self.auth = bo.CoinbaseExchangeAuth(
            api_key=self.keys['public'],
            secret_key=self.keys['secret'],
            passphrase=self.keys['pass']
        )
        self.meta = None
        self.response = None
        self.prices = None
        self._max_candles = 300

    def build_meta(self):
        """
        Creates table containing meta data about every currency pair (traded and referential) available on the API.
        The information includes specifics about tradablility and quote details.

        :return: Pandas DataFrame.
        """
        r = requests.get(
            url='https://api.pro.coinbase.com/products',
            auth=self.auth
        )
        self.meta = pd.DataFrame.from_dict(r.json()).set_index('id').sort_index()
        self.response = r.status_code

        pass

    def candles(self, sid, start_dt, end_dt, frequency):
        """
        Gets historical candles (maximum of 300 candles, regardless the frequency). The information retrieved from
        the API contains low, high, open, close, and volume traded with the start date of the candle as index.

        :param sid: Security id.
        :param start_dt: datetime object.
        :param end_dt: datetime object.
        :param frequency: In seconds. Possible values are 60 (1min), 300 (5min), 900 (15min), 3600 (1hr),
        21600 (6hrs), 86400 (1day).
        :return: Pandas DataFrame containing the candle data.
        """
        params = {
            'start': start_dt.isoformat(),
            'end': end_dt.isoformat(),
            'granularity': frequency
        }

        r = requests.get(
            url='https://api.pro.coinbase.com/products/' + sid + '/candles',
            auth=self.auth,
            params=params
        )
        self.response = r.status_code

        candles = pd.DataFrame(r.json(), columns=['dt', 'low', 'high', 'open', 'close', 'volume'])
        candles['dt'] = candles['dt'].apply(datetime.fromtimestamp)
        candles.set_index('dt', inplace=True)
        candles.sort_index(inplace=True)
        self.prices = candles

        return candles

    def historical(self, sid, start_dt, end_dt, frequency):
        """
        Gets historical candles for long periods of time through an iterative poll. The information retrieved from
        the API contains low, high, open, close, and volume traded with the start date of the candle as index.

        :param sid: Security id.
        :param start_dt: datetime object.
        :param end_dt: datetime object.
        :param frequency: In seconds. Possible values are 60 (1min), 300 (5min), 900 (15min), 3600 (1hr),
        21600 (6hrs), 86400 (1day).
        :return:
        """
        length = (end_dt - start_dt).total_seconds()
        pulls = math.ceil(length / (self._max_candles * frequency))  # Make sure the 300 cap is met
        step_size = math.ceil(length / pulls)
        if step_size > self._max_candles * frequency:
            pulls += 1
            step_size = math.ceil(length / pulls)

        fetch = []
        dts = [end_dt - timedelta(seconds=x * step_size) for x in range(pulls + 1)]
        dts = dts[::-1]
        dts[0] -= timedelta(seconds=frequency)
        dts[-1] = end_dt
        for i in tqdm(range(pulls)):
            prices = self.candles(
                sid=sid,
                start_dt=dts[i] + timedelta(seconds=frequency),
                end_dt=dts[i + 1],
                frequency=frequency
            )
            fetch += [prices]
            time.sleep(1 + uniform(.025, .5))

        table = pd.concat(fetch, axis=0).sort_index()
        self.prices = table

        return table
    pass

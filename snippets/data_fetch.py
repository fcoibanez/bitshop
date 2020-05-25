import snippets.basic_operations as bo
import requests
import csv
import os
import math
from random import uniform
import pandas as pd
from datetime import datetime, timedelta
import time
from tqdm import tqdm


# -----------------------------------------------------------------------
# DataFetch class
class DataFetch:
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
        r = requests.get(
            url='https://api.pro.coinbase.com/products',
            auth=self.auth
        )
        self.meta = pd.DataFrame.from_dict(r.json()).set_index('id').sort_index()
        self.response = r.status_code

        pass

    def candles(self, sid, start_dt, end_dt, frequency):
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

    def build_historical(self, sid, start_dt, end_dt, frequency):
        length = (end_dt - start_dt).total_seconds()
        pulls = math.ceil(length / (self._max_candles * frequency))  # Make sure the 300 cap is met
        step_size = math.ceil(length / pulls)
        if step_size > self._max_candles * frequency:
            pulls += 1
            step_size = math.ceil(length / pulls)

        fetch = []
        dts = [end - timedelta(seconds=x * step_size) for x in range(pulls + 1)]
        dts = dts[::-1]
        dts[0] -= timedelta(seconds=frequency)
        dts[-1] = end
        for i in tqdm(range(pulls)):
            prices = data.candles(
                sid='BTC-USD',
                start_dt=dts[i] + timedelta(seconds=frequency),
                end_dt=dts[i + 1],
                frequency=frequency
            )
            fetch += [prices]
            time.sleep(1 + uniform(.025, .5))

        self.prices = pd.concat(fetch, axis=0).sort_index()
        pass
    pass


if __name__ == '__main__':
    wd = os.getcwd()

    # Read the API Keys
    keys_dict = {}
    with open(os.getcwd() + '/snippets/keys.csv', newline='', encoding='ASCII') as f:
        reader = csv.reader(f)
        for row in reader:
            keys_dict[row[0]] = row[1]

    data = DataFetch(api_keys=keys_dict)
    req = data.candles(
        sid='BTC-USD',
        start_dt=datetime(2020, 5, 20),
        end_dt=datetime(2020, 5, 23),
        frequency=86400
    )

    # Pulling long time series
    freq = 86400
    max_candles = 300
    start = datetime(2019, 5, 24)
    end = datetime(2020, 5, 23)
    length = (end - start).total_seconds()  # in seconds

    pulls = math.ceil(length / (max_candles * freq))  # Make sure the 300 cap is met
    step_size = math.ceil(length / pulls)
    if step_size > max_candles * freq:
        pulls += 1
        step_size = math.ceil(length / pulls)

    fetch = []
    dts = [end - timedelta(seconds=x * step_size) for x in range(pulls + 1)]
    dts = dts[::-1]
    dts[0] -= timedelta(seconds=freq)
    dts[-1] = end
    for i in tqdm(range(pulls)):
        prices = data.candles(
            sid='BTC-USD',
            start_dt=dts[i] + timedelta(seconds=freq),
            end_dt=dts[i + 1],
            frequency=freq
        )
        fetch += [prices]
        time.sleep(1 + uniform(.025, .5))

    df = pd.concat(fetch, axis=0).sort_index()
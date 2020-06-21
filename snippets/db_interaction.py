import bitshop
from bitshop.pipeline import rest
from datetime import datetime
import os
import csv
wd = os.getcwd()

# Read the API Keys
keys_dict = {}
with open(os.getcwd() + '/snippets/keys.csv', newline='', encoding='ASCII') as f:
    reader = csv.reader(f)
    for row in reader:
        keys_dict[row[0]] = row[1]

data = bitshop.DataFetch(api_keys=keys_dict)
data.build_meta()
data.meta
data.candles(
    sid='BTC-USD',
    start_dt=datetime(2020, 5, 20),
    end_dt=datetime(2020, 5, 23),
    frequency=86400
)

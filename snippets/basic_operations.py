import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
import csv
import os
wd = os.getcwd()


# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


# Read the API Keys
reader = csv.reader(open(wd + '/keys.csv', encoding='ASCII'))
api_keys = {}
for row in reader:
    key = row[0]
    api_keys[key] = row[1]

api_keys = {}
with open(wd + '/keys.csv', newline='', encoding='ASCII') as f:
    reader = csv.reader(f)
    for row in reader:
        api_keys[row[0]] = row[1]

auth = CoinbaseExchangeAuth(
    api_key=api_keys['public'],
    secret_key=api_keys['secret'],
    passphrase=api_keys['pass']
)

# Get accounts
r = requests.get('https://api.pro.coinbase.com/accounts', auth=auth)
print(r.json())

# Place an order
order = {
    'size': 1.0,
    'price': 1.0,
    'side': 'buy',
    'product_id': 'BTC-USD',
}
r = requests.post('https://api.pro.coinbase.com/orders', json=order, auth=auth)
print(r.json())

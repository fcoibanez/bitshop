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

if __name__ == '__main__':
    # Read the API Keys
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
    api_url = 'https://api-public.sandbox.pro.coinbase.com/'
    # Get accounts (list)
r1 = requests.get(api_url+'accounts', auth=auth)
#https://api.pro.coinbase.com/accounts
print(r1.json())

# Get an account (just an specific account)
BTCaccount='/9fc48acb-285f-4dba-a9bb-4df958947c46'
r2 = requests.get(api_url+'accounts'+BTCaccount,auth=auth)
print(r2.json())

#Get Account History
r3 = requests.get(api_url+'accounts'+BTCaccount+'/ledger',auth=auth)
print(r3.json())

#Get Holds
r4 = requests.get(api_url+'accounts'+BTCaccount+'/holds',auth=auth)
print(r4.json())


# Place an order (limit)
order = {
    'size': 1.0,
    'price': 1.0,
    'side': 'buy',
    'product_id': 'BTC-USD',
}
r = requests.post(api_url+'orders', json=order, auth=auth)
print(r.json())

# Place an order (Market)
order = {
    'type': 'market',
    'size': 1.0, #number of bitcoins
    'side': 'buy',
    'product_id': 'BTC-USD',
}
r = requests.post(api_url + 'orders', json=order, auth=auth)
print(r.json())

#Cancel an Order (Cancel All)
r = requests.delete(api_url + 'orders', json=order, auth=auth)
print(r.json())

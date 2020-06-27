import requests

class inputs():
    def get_ccys(self):
        '''
        Retrieves all the available currencies. NOTE: not all of them are
        available for trading.

        :return: list of available currencies.
        '''

        url = 'https://api.pro.coinbase.com'
        endpoint = '/currencies'
        resp = requests.get(url + endpoint)
        ccys = resp.json()
        for i in range(len(ccys)):
            print('id:', ccys[i]['id'], ', name:', ccys[i]['name'])

    def get_channels(self, description=False):
        '''
        When description = False, prints a list containing all the available channels. When description = True, it
        prints a dict with a brief description of each channel.

        :param description: Boolean. Default False
        :return: list of available channels
        '''

        'NOTE: sequence numbers and trades ids can be used to verify no messages were missed.'

        if description == True:
            hb = 'receive messages once a second. includes sequence numbers and last trade ids.'
            st = 'will send all products and currencies on a preset interval.'
            tc = 'real-time price updates on every match. batches updates in case of cascading matches'
            l2 = 'snapshot of the order book. guarantees delivery of all updates. gives snapshot with [price, ' \
                 'size] tuples. subsequent updates will have the type l2update. l2updates is an array with ' \
                 '[side, price, size] tuples. size is the updated size at that price level, not a delta.'
            us = 'version of full channel. contains messages that include authenticated user. need authentication'
            mt = 'describes matches at market. NOTE: messages can be dropped from this channel.'
            fl = ' real-time updates on orders and trades. updates can be applied on to a level 3 order book ' \
                 'snapshot to maintain an accurate and up-to-date copy of the exchange order book'
            ch_list = dict({
                'heartbeat': hb,
                'status': st,
                'ticker': tc,
                'level2': l2,
                'user': us,
                'matches': mt,
                'full': fl
            })
            for key, value in ch_list.items():
                print(str(key) + ':', value)

        else:
            ch_list = [
                'heartbeat',
                'status',
                'ticker',
                'level2',
                'user',
                'matches',
                'full'
            ]
            for i in range(len(ch_list)):
                print(ch_list[i])



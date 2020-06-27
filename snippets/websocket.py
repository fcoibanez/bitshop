import json
from websocket import create_connection

# based on https://pypi.org/project/websocket_client/ - need to install the library
# https://pypi.org/project/websockets/
class wbsocket:
    def __init__(self, ccys, channel):
        '''

        :param self:
        :param ccys:
        :param channel:
        :return:
        '''
        self.ccys = ccys
        self.channel = channel
        # self.ws         = None

    def get_uri(self):
        '''
        Return websocket where to connect

        :return: websocket connection

        '''
        uri = 'wss://ws-feed.pro.coinbase.com'
        return uri

    def get_data(self):
        '''
        Creates a connection using websocket. Suscribe to the desired channel and the desired ccys.

        :param self:
        :return:
        '''
        uri = self.get_uri()
        ws = create_connection(uri)
        suscribe = {
            "type": "subscribe",
            "channels": [{"name": self.channel, "product_ids": self.ccys}]
        }
        ws.send(json.dumps(suscribe))
        print('Connected to', ws.recv())
        count = 0
        while count < 20:
            print(ws.recv())
            count += 1

        unsubscribe = {

            "type": "unsubscribe",
            "channels": [{"name": self.channel, "product_ids": self.ccys}]

        }

        ws.send(json.dumps(unsubscribe))


import websocket
import json
import gevent
import traceback
from pprint import pprint
from .messages import serialize, Deploy, Cancel


class WebsocketChannel(object):

    def __init__(self, address, outbox):
        self.address = address
        self.start_socket_thread()
        self.outbox = outbox

    def start_socket_thread(self):
        print(self.address)
        self.socket = websocket.WebSocketApp(self.address,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close,
                                             on_open=self.on_open)
        self.thread = gevent.spawn(self.socket.run_forever)

    def put(self, message):
        try:
            self.socket.send(json.dumps(serialize(message)))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self.thread.kill()
            self.start_socket_thread()

    def on_open(self):
        print('WebsocketChannel on_open')
        pass

    def on_message(self, message):
        print('WebsocketChannel on_message')
        message = json.loads(message)
        pprint(message)
        if message[0] == "deploy":
            self.outbox.put(Deploy(message[1]))
        elif message[0] == "cancel":
            self.outbox.put(Cancel())

    def on_close(self):
        print('WebsocketChannel on_close')
        self.thread.kill()

    def on_error(self, error):
        print('WebsocketChannel on_error', error)
        try:
            self.on_close()
        finally:
            gevent.sleep(1)
            self.start_socket_thread()

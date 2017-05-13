import json
import logging
import sys

import asyncio
import colorlog
import messages
from autobahn.asyncio.websocket import (WebSocketClientFactory,
                                        WebSocketClientProtocol)

log = logging.getLogger(__name__)
loop = asyncio.get_event_loop()


class Connection(WebSocketClientProtocol):
    def __init__(self):
        super(WebSocketClientProtocol, self).__init__()

    def onOpen(self):
        log.info("connection is open")
        self._send(messages.client_info())
        self._send(messages.player_registration('python-snake'))

    def onMessage(self, payload, isBinary):
        assert not isBinary
        if isBinary:
            log.error('Received binary message, ignoring...')
            return

        msg = json.loads(payload.decode())
        log.info("Message received: %s", msg)

        self._route_message(msg)

    def onClose(self, wasClean, code, reason):
        log.info("Socket is closed!")
        if reason:
            log.error(reason)

        loop.stop()

    def _send(self, msg):
        log.debug("Sending message: %s", msg)
        self.sendMessage(json.dumps(msg).encode(), False)

    def _route_message(self, msg):
        if msg['type'] == messages.PLAYER_REGISTERED:
            self._send(messages.start_game())
        elif msg['type'] == messages.MAP_UPDATE:
            self._send(messages.register_move('DOWN', msg))
        elif msg['type'] == messages.GAME_ENDED:
            self.sendClose()


def main():
    host = "localhost"
    port = "8080"

    factory = WebSocketClientFactory(u"ws://%s:%s/training" % (host, port))
    factory.protocol = Connection

    coro = loop.create_connection(factory, host, port)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

    sys.exit(0)


if __name__ == "__main__":
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s:%(name)s:%(message)s'))

    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    log.debug("logging is set up!")

    main()

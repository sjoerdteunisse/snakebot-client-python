import json
import logging
import sys

import asyncio
from autobahn.asyncio.websocket import (WebSocketClientFactory,
                                        WebSocketClientProtocol)
import colorlog

log = logging.getLogger(__name__)
loop = asyncio.get_event_loop()


class Connection(WebSocketClientProtocol):
    def __init__(self):
        super(WebSocketClientProtocol, self).__init__()

    def onOpen(self):
        log.info("connection is open")
        self.sendClose()

    def onMessage(self, payload, isBinary):
        assert not isBinary

        res = json.loads(payload.decode())
        log.info("Message received: %s", res)

    def onClose(self, wasClean, code, reason):
        log.info("Socket is closed!")

        assert not reason
        loop.stop()


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

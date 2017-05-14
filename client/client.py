import json
import logging
import sys
import time

import asyncio
import colorlog
import messages
import snake
from autobahn.asyncio.websocket import (WebSocketClientFactory,
                                        WebSocketClientProtocol)

log = logging.getLogger("client")
loop = asyncio.get_event_loop()


class Connection(WebSocketClientProtocol):
    def __init__(self):
        super(WebSocketClientProtocol, self).__init__()
        self.routing = {
            messages.GAME_ENDED: self._game_ended,
            messages.TOURNAMENT_ENDED: self._tournament_ended,
            messages.MAP_UPDATE: self._map_update,
            messages.SNAKE_DEAD: self._snake_dead,
            messages.GAME_STARTING: self._game_starting,
            messages.PLAYER_REGISTERED: self._player_registered,
            messages.INVALID_PLAYER_NAME: self._invalid_player_name,
            messages.HEART_BEAT_RESPONSE: self._heart_beat_response,
            messages.GAME_LINK_EVENT: self._game_link,
            messages.GAME_RESULT_EVENT: self._game_result
        }
        self.snake = snake.get_snake()

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
        log.debug("Message received: %s", msg)

        self._route_message(msg)

    def onClose(self, wasClean, code, reason):
        log.info("Socket is closed!")
        if reason:
            log.error(reason)

        self.heart_beat.cancel()

    def _done(self, task):
        loop.stop()

    def _send(self, msg):
        log.debug("Sending message: %s", msg)
        self.sendMessage(json.dumps(msg).encode(), False)

    def _route_message(self, msg):
        fun = self.routing.get(msg['type'], None)
        if fun:
            fun(msg)
        else:
            self._unrecognied_message(msg)

    def _game_ended(self, msg):
        self.snake.on_game_ended()
        self.sendClose()

    def _tournament_ended(self, msg):
        self.sendClose()

    def _map_update(self, msg):
        move = self.snake.get_next_move(msg)
        self._send(messages.register_move(move, msg))

    def _snake_dead(self, msg):
        self.snake.on_snake_dead(msg['deathReason'])

    def _game_starting(self, msg):
        self.snake.on_game_starting()

    def _player_registered(self, msg):
        self._send(messages.start_game())
        player_id = msg['receivingPlayerId']
        self.heart_beat = loop.create_task(self._send_heart_beat(player_id))
        self.heart_beat.add_done_callback(self._done)

    def _invalid_player_name(self, msg):
        self.snake.on_invalid_player_name()

    def _heart_beat_response(self, msg):
        pass

    def _game_link(self, msg):
        log.info('Watch game at: %s', msg['url'])

    def _game_result(self, msg):
        self.snake.on_game_result(msg['playerRanks'])

    def _unrecognied_message(self, msg):
        log.error('Received unrecognized message: %s', msg)

    async def _send_heart_beat(self, player_id):
        while True:
            self._send(messages.heart_beat(player_id))
            await asyncio.sleep(2)


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

    formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(asctime)s %(levelname)8s] -- %(message)s (%(filename)s:%(lineno)s)',
        datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    main()

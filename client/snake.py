import logging

log = logging.getLogger("client.snake")


class Snake(object):
    def __init__(self):
        self.name = "snake.py"

    def get_next_move(self, map):
        return 'DOWN'

    def on_game_ended(self):
        log.debug('The game has ended!')
        pass

    def on_snake_dead(self, reason):
        log.debug('Our snake died because %s', reason)

    def on_game_starting(self):
        log.debug('Game is starting!')

    def on_player_registered(self):
        log.debug('Player registered successfully')

    def on_invalid_playername(self):
        log.fatal('Player name is invalid, try another!')

    def on_game_result(self, player_ranks):
        log.info('Game result:')
        for player in player_ranks:
            is_alive = 'alive' if player['alive'] else 'dead'
            log.info('%d. %d pts\t%s\t(%s)' %
                     (player['rank'], player['points'], player['playerName'],
                      is_alive))


def get_snake():
    return Snake()

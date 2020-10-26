import logging
import util

log = logging.getLogger("client.snake")


class Snake(object):
    def __init__(self):
        self.name = "snake.py"
        self.snake_id = "abc"

    def get_next_move(self, game_map):
        v = game_map.get_snake_by_id(self.snake_id)

        print(v)
        #game_map.is_coordinate_out_of_bounds()
        cmd = game_map.can_snake_move_in_direction(self.snake_id, util.Direction.DOWN)
        cmu = game_map.can_snake_move_in_direction(self.snake_id, util.Direction.UP)
        cmr = game_map.can_snake_move_in_direction(self.snake_id, util.Direction.RIGHT)
        cml = game_map.can_snake_move_in_direction(self.snake_id, util.Direction.LEFT)

        positions = v.get("positions")
        trl = util.translate_positions(positions, 46)
        
        v = util.Direction.DOWN;

        if(cmu):
          v = util.Direction.UP
        if(cmr):
          v = util.Direction.RIGHT
        if(cml):
          v = util.Direction.LEFT
        

        return v

    def on_game_ended(self):
        log.debug('The game has ended!')

    def on_snake_dead(self, reason):
        log.debug('Our snake died because %s', reason)

    def on_game_starting(self):
        log.debug('Game is starting!')

    def on_player_registered(self, snake_id):
        log.debug('Player registered successfully')
        self.snake_id = snake_id

    def on_invalid_player_name(self):
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

from random import Random


class Board(object):
    """Board dimensions"""

    # directions enum
    N = 'n'
    S = 's'
    E = 'e'
    W = 'w'

    def __init__(self, x_dim, y_dim):
        self.x_dim = x_dim
        self.y_dim = y_dim


class Position(object):
    """0 based position on the board with origin in SW corner"""

    def __init__(self, x, y):
        self.x = x
        self.y = y


class GameParams(object):

    def __init__(self, board, human_speed, human_pos=None, zombie_pos=None):
        self.board = board
        self.human_speed = human_speed

        if human_pos:
            self.human_starting_pos = human_pos
        else:
            self.human_starting_pos = Position(0, 0)

        if zombie_pos:
            self.zombie_starting_pos = zombie_pos
        else:
            self.zombie_starting_pos = Position(board.x_dim // 2, board.y_dim // 2)


class Player(object):

    HUMAN = 'human'
    ZOMBIE = 'zombie'

    def __init__(self, player_type, board, position, speed):
        self.type = player_type
        self.board = board
        self.position = position
        self.speed = speed
        self.rng = Random()
        self.rng.seed(id(self))

    def move(self):
        """Return the new position of the player

        Override this method to implement your strategy
        """

        direction = self.rng.choice([Board.N, Board.E, Board.S, Board.W])
        distance = self.rng.choice(range(1, self.speed + 1))
        self.update(direction, distance)

        return self.position

    def update(self, direction, distance):
        """Update the player's position based on a direction and distance

        This is a convenience method that ensures the player stays inside the board
        """

        if direction == Board.N:
            self.position.y += distance
        elif direction == Board.S:
            self.position.y -= distance
        elif direction == Board.E:
            self.position.x += distance
        else:
            self.position.x -= distance

        self.position.x = self.clamp(self.position.x, 0, self.board.x_dim - 1)
        self.position.y = self.clamp(self.position.y, 0, self.board.y_dim - 1)

    @staticmethod
    def clamp(n, minimum, maximum):
        """Clamp the value within a range"""
        return max(min(maximum, n), minimum)


class Zombie(Player):

    def __init__(self, board, position):
        Player.__init__(self, Player.ZOMBIE, board, position, 1)


class Game(object):

    def __init__(self, params, human, zombie=None):
        self.params = params
        self.human = human
        if zombie:
            self.zombie = zombie
        else:
            self.zombie = Zombie(params.board, params.zombie_starting_pos)
        self.tracks = []

    def run(self):
        """Run a game to completion"""
        human_pos = self.params.human_starting_pos
        zombie_pos = self.params.zombie_starting_pos

        while True:
            self.tracks.append([
                {'type': Player.HUMAN, 'position': human_pos},
                {'type': Player.ZOMBIE, 'position': zombie_pos}
            ])

            print('Human: {}, {}  Zombie: {}, {}'.format(human_pos.x, human_pos.y, zombie_pos.x, zombie_pos.y))

            if self.is_game_over():
                break

            human_pos = self.human.move()
            zombie_pos = self.zombie.move()

    def is_game_over(self):
        """Check if game is over"""

        # extend to check if paths crossed
        human_pos = self.tracks[-1][0]['position']
        zombie_pos = self.tracks[-1][1]['position']
        return human_pos.x == zombie_pos.x and human_pos.y == zombie_pos.y


class Tournament(object):
    pass

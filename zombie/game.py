from random import Random


class Board(object):
    """Board dimensions"""

    def __init__(self, x_dim, y_dim):
        self.x_dim = x_dim
        self.y_dim = y_dim


class Position(object):
    """0 based position on the board with origin in SW corner"""

    def __init__(self, x, y):
        self.x = x
        self.y = y


class GameParams(object):

    def __init__(self, board, human_speed, human_pos, zombie_pos):
        self.board = board
        self.human_speed = human_speed
        self.human_starting_pos = human_pos
        self.zombie_starting_pos = zombie_pos


class Player(object):

    HUMAN = 0
    ZOMBIE = 1

    def __init__(self, player_type, board, position, speed):
        self.type = player_type
        self.board = board
        self.position = position
        self.speed = speed
        self.rng = Random()
        self.rng.seed(id(self))

    def move(self):
        """Return the new position of the player"""
        direction = self.rng.choice(['n', 'e', 's', 'w'])
        distance = self.rng.choice(range(1, self.speed + 1))
        self.update(direction, distance)

        return self.position

    def update(self, direction, distance):
        """Update the player's position based on a direction and distance"""
        if direction == 'n':
            self.position.y += distance
        elif direction == 's':
            self.position.y -= distance
        elif direction == 'e':
            self.position.x += distance
        else:
            self.position.x -= distance

        self.position.x = self.clamp(self.position.x, 0, self.board.x_dim - 1)
        self.position.y = self.clamp(self.position.y, 0, self.board.y_dim - 1)

    def clamp(self, n, minimum, maximum):
        """Clamp the value within a range"""
        return max(min(maximum, n), minimum)


class Zombie(Player):

    def __init__(self, board, position):
        Player.__init__(self, Player.ZOMBIE, board, position, 1)


class Game(object):

    def __init__(self, params, zombie, human):
        self.params = params
        self.zombie = zombie
        self.human = human

    def run(self):
        self.human.move()
        self.zombie.move()
        print('Human: {}, {}  Zombie: {}, {}'.format(self.human.position.x, self.human.position.y, self.zombie.position.x, self.zombie.position.y))

        if self.human.position.x == self.zombie.position.x and self.human.position.y == self.zombie.position.y:
            print 'Zombie wins'
            return False
        else:
            return True


class Tournament(object):
    pass

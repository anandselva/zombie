import pygame


class GameTrace(object):

    def __init__(self, board, positions):
        self.board = board
        self.positions = positions


class GameTraceRenderer(object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    def __init__(self, trace):
        self.trace = trace
        self.width = trace.board.x_dim
        self.height = trace.board.y_dim
        self.zoom = 25

        pygame.init()
        pygame.display.set_caption("Zombie Game Renderer")

        self.clock = pygame.time.Clock()
        self.fps = 1

        self.screen = pygame.display.set_mode((self.zoom * self.width, self.zoom * self.height))
        self.background = pygame.Surface((self.screen.get_size()))
        self.background = self.background.convert()

    def run(self):

        for positions in self.trace.positions:
            self.draw_background()
            self.draw_actors(positions)
            self.draw_screen()

            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

        pygame.quit()

    def draw_screen(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def draw_background(self):
        self.background.fill(GameTraceRenderer.BLACK)

    def draw_actors(self, positions):
        for actor in positions:
            radius = self.zoom // 2
            offset = radius

            if actor['type'] == 'human':
                color = GameTraceRenderer.RED
            else:
                color = GameTraceRenderer.GREEN
                radius -= 1

            x = self.zoom * actor['position'].x + offset
            y = self.zoom * actor['position'].y + offset
            pygame.draw.circle(self.background, color, (x, y), radius)

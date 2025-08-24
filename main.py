# Imports
import sys, pygame
import random, time

# Inits
pygame.init()

# Global variables
GRID_SIZE = 12

TILE_SIZE = 70
TILE_PADDING = 5

SCSREEN_WIDTH = GRID_SIZE * (2 * TILE_PADDING + TILE_SIZE)
SCSREEN_HEIGHT = GRID_SIZE * (2 * TILE_PADDING + TILE_SIZE)
SCREEN_SIZE = (SCSREEN_WIDTH, SCSREEN_HEIGHT)

FPS_VALUE = 60

DARK_GREEN = (35, 74, 16)

# Initial setup
screen = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption('Hide and seek')
game_icon = pygame.image.load('assets/sprites/logo.png')
pygame.display.set_icon(game_icon)

fps = pygame.time.Clock()

seeker_path = [
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 4),
    (2, 3),
    (3, 3),
    (4, 3),
    (4, 2)
]
seeker_path_index = 0

wall_list = [
    (1, 6),
    (1, 9), (2, 9), (3, 9),
    (2, 4), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
    (4, 1),
    (5, 4),
    (5, 6), (6, 6), (7, 6), (8, 6),
    (5, 9), (6, 8), (6, 9), (6, 10),
    (6, 2), (7, 2), (7, 3), (8, 3), (8, 4),
    (8, 8), (8, 9), (9, 8),
    (10, 2),
    (10, 6)
]
# Events
SECOND = 1000
MOVE_PLAYERS = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_PLAYERS, 1 * SECOND)

HUNT_HIDER = pygame.USEREVENT + 2
pygame.time.set_timer(HUNT_HIDER, 7 * SECOND)

GAME_TIME = pygame.USEREVENT + 3
pygame.time.set_timer(GAME_TIME, 15 * SECOND)

# Classes
class Grid():
    def __init__(self):
        self.grid = [['B' if i == 0 or j == 0 or i == GRID_SIZE - 1 or j == GRID_SIZE - 1 else ' ' for i in range(0,GRID_SIZE)] for j in range(0, GRID_SIZE)]

        # Populate grid with walls
        for (row, col) in wall_list:
            self.grid[row][col] = 'W'

    def print(self):
        for row in self.grid:
            print(row)

    def set_cell(self, row, col, symbol):
        self.grid[row][col] = symbol

    def draw_self(self, screen):
        for row in range(1, GRID_SIZE - 1):
            for col in range(1, GRID_SIZE - 1):
                sprite_pos_x = col * (TILE_PADDING + TILE_SIZE + TILE_PADDING) + TILE_PADDING
                sprite_pos_y = row * (TILE_PADDING + TILE_SIZE + TILE_PADDING) + TILE_PADDING

                if self.grid[row][col] == 'H':
                    screen.blit(hider.image, (sprite_pos_x, sprite_pos_y))
                elif self.grid[row][col] == 'S':
                    screen.blit(seeker.image, (sprite_pos_x, sprite_pos_y))
                elif self.grid[row][col] == 'W':
                    screen.blit(crate, (sprite_pos_x, sprite_pos_y))
                else:
                    pygame.draw.rect(screen, DARK_GREEN, (col * (TILE_PADDING + TILE_SIZE + TILE_PADDING) + TILE_PADDING, row * (TILE_PADDING + TILE_SIZE + TILE_PADDING) + TILE_PADDING, TILE_SIZE, TILE_SIZE))

class Entity():
    def __init__(self, row, col, symbol):
        # Entity position
        self.row = row
        self.col = col
        self.symbol = symbol

    # Entity moves itself
    def move_to(self, row, col, grid):
        # wants to move out of bounds, we do not allow
        if row < 1 or col < 1 or row > GRID_SIZE - 2 or col > GRID_SIZE - 2:
            print("You cannot move outside the map")
            return grid

        # empty previous
        grid.set_cell(self.row, self.col, ' ')

        # update self position
        self.row = row
        self.col = col

        # update grid
        grid.set_cell(self.row, self.col, self.symbol)

        # return new grid
        return grid

class Hider(Entity):
    def __init__(self, sprite_path):
        # Hider position
        self.row = GRID_SIZE - 2
        self.col = GRID_SIZE - 2
        self.symbol = 'H'

        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def check_for_seeker(self, grid):
        # Check the up, down, left , right and the corners for the seeker
        if grid.grid[self.row + 1][self.col] == 'S' or\
            grid.grid[self.row - 1][self.col] == 'S' or\
            grid.grid[self.row][self.col + 1] == 'S' or\
            grid.grid[self.row][self.col - 1] == 'S' or\
            grid.grid[self.row - 1][self.col - 1] == 'S' or\
            grid.grid[self.row + 1][self.col + 1] == 'S' or\
            grid.grid[self.row - 1][self.col + 1] == 'S' or\
            grid.grid[self.row + 1][self.col - 1] == 'S':
            return True
        else:
            return False

    def brain():
        # TODO move randomly to position [row][col]
        #      [ ][ ][ ]
        #      [ ][H][ ]
        #      [ ][ ][ ]
        # Move in any of the empty  places
        pass

class Seeker(Entity):
    def __init__(self, sprite_path):
        self.row = 1
        self.col = 1
        self.symbol = 'S'

        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def brain():
        # TODO DFS/BFS periodically to seeker hinted position, meanwhile random just like Hider
        pass

grid = Grid()
hider = Hider('assets/sprites/hider.png')
seeker = Seeker('assets/sprites/seeker.png')

# Place Hider and Seeker on the map
grid.set_cell(hider.row, hider.col, hider.symbol)
grid.set_cell(seeker.row, seeker.col, seeker.symbol)

background = pygame.image.load('assets/sprites/background.png')
background = pygame.transform.scale(background, SCREEN_SIZE)

crate = pygame.image.load('assets/sprites/wall.png')
crate = pygame.transform.scale(crate, (TILE_SIZE, TILE_SIZE))

while True:
    # Render background
    screen.blit(background, (0, 0))

    # handle game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == MOVE_PLAYERS:
            # TODO move hider on screen

            # move seeker on screen
            if not seeker_path or len(seeker_path) == 0 or seeker_path_index > len(seeker_path):
                # TODO seeker has no data on where the hider is, move randomly
                print('reset')
                # seeker_path_index = 0  # this one is for debug only

            grid = seeker.move_to(seeker_path[seeker_path_index][0], seeker_path[seeker_path_index][1], grid)
            seeker_path_index += 1

            # update screen
            grid.draw_self(screen)
            # check for end game condition
            if hider.check_for_seeker(grid) == True:
                print('Game Over')
            else:
                print('continuing...')

        elif event.type == HUNT_HIDER:
            # TODO run seeker bfs on the hider current position and return a list of cells to follow to the hider
            seeker_path_index = 0
            continue

        elif event.type == GAME_TIME:
            if hider.check_for_seeker(grid) == True:
                print('Game Over. You loose!')
            else:
                print('Game Over. You win! :)))')

    # draw grid
    grid.draw_self(screen)

    # move hider
    # grid = hider.move_to(2, 2, grid)

    pygame.display.update()
    fps.tick(FPS_VALUE)
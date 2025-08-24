# Imports
import sys, pygame

# Inits
pygame.init()

# Global variables
GRID_SIZE = 11

SCSREEN_WIDTH = 700
SCSREEN_HEIGHT = 700
SCREEN_SIZE = (SCSREEN_WIDTH, SCSREEN_HEIGHT)

FPS_VALUE = 60

# Initial setup
screen = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption('Hide and seek')
game_icon = pygame.image.load('assets/sprites/logo.png')
pygame.display.set_icon(game_icon)

fps = pygame.time.Clock()

# Classes
class Grid():
    def __init__(self):
        global GRID_SIZE
        self.grid = [['B' if i == 0 or j == 0 or i == GRID_SIZE - 1 or j == GRID_SIZE - 1 else ' ' for i in range(0,GRID_SIZE)] for j in range(0, GRID_SIZE)]

    def print(self):
        for row in self.grid:
            print(row)

    def set_cell(self, row, col, symbol):
        self.grid[row][col] = symbol

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
    def __init__(self):
        # Hider position
        self.row = 1
        self.col = 1
        self.symbol = 'H'

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
    def __init__(self):
        self.row = GRID_SIZE - 2
        self.col = GRID_SIZE - 2
        self.symbol = 'S'

    def brain():
        # TODO DFS/BFS periodically to seeker hinted position, meanwhile random just like Hider
        pass

grid = Grid()
hider = Hider()
seeker = Seeker()

# Place Hider and Seeker on the map
grid.set_cell(hider.row, hider.col, hider.symbol)
grid.set_cell(seeker.row, seeker.col, seeker.symbol)

background = pygame.image.load('assets/sprites/background.png')
background = pygame.transform.scale(background, SCREEN_SIZE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))
    pygame.display.update()
    fps.tick(FPS_VALUE)

# TODOs:

# TODO I need a way to move both hider and seeker to coordinates [row][col] once every 1 second or so
# TODO make the UI of my game
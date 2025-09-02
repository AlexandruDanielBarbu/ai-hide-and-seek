import pygame, random
from settings import TILE_SIZE, HIDER_LOCATIONS


class Entity():
    def __init__(self, row, col, symbol):
        # Entity position
        self.row = row
        self.col = col
        self.symbol = symbol

    # Entity moves itself
    def move_to(self, row, col, grid):

        # Moving on a wall
        if grid.grid[row][col] == 'W':
            # print('The seeker smashed a crate!')
            return grid

        if grid.grid[self.row][self.col] == 'W':
            grid.set_cell(self.row, self.col, 'W')
        else:
            grid.set_cell(self.row, self.col, ' ')

        # update self position
        self.row = row
        self.col = col

        # update grid
        grid.set_cell(self.row, self.col, self.symbol)

        # return new grid
        return grid


    def basic_brain(self, grid):
        new_row = self.row
        new_col = self.col
        return self.move_to(new_row, new_col, grid)


class Hider(Entity):
    def __init__(self, sprite_path):
        # Hider position
        my_pos = HIDER_LOCATIONS[random.randint(0, len(HIDER_LOCATIONS) - 1)]

        self.row = my_pos[0]
        self.col = my_pos[1]
        self.symbol = 'H'

        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def check_for_seeker(self, grid):
        return grid.grid[self.row][self.col] == 'S'

class Seeker(Entity):
    def __init__(self, sprite_path, q_agent):
        self.row = 1
        self.col = 1
        self.symbol = 'S'

        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

        self.q_agent = q_agent

    def advanced_brain(self, grid, hider):
        state = self.q_agent.get_state(self)
        action = self.q_agent.choose_action(state)

        moves = [(-1,0), (1,0), (0,-1), (0,1)]
        new_row = self.row + moves[action][0]
        new_col = self.col + moves[action][1]

        while grid.grid[new_row][new_col] == 'B':
            action = self.q_agent.choose_action(state)
            new_row = self.row + moves[action][0]
            new_col = self.col + moves[action][1]


        grid = self.move_to(new_row, new_col, grid)
        next_state = self.q_agent.get_state( self)

        return grid, action, state, next_state


import pygame
from settings import TILE_PADDING, TILE_SIZE, GRID_SIZE, DARK_GREEN


wall_list = [
    (1, 6), (1, 9),
    (2, 4), (2, 9),
    (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 9),
    (4, 1),
    (5, 4), (5, 6), (5, 9),
    (6, 2), (6, 6), (6, 8), (6, 9), (6, 10),
    (7, 2), (7, 3), (7, 6), 
    (8, 3), (8, 4), (8, 6), (8, 8), (8, 9),    
    (9, 8),
    (10, 2), (10, 6)
]

# Class for grid
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

    def draw_self(self, screen, hider, seeker, crate):
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

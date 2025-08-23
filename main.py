GRID_SIZE = 11
class Grid():
    def __init__(self):
        global GRID_SIZE
        self.grid = [[' ' for i in range(0,GRID_SIZE)] for j in range(0, GRID_SIZE)]

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

    # Entity move itself
    def move_to(self, row, col, grid):
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
        # DFS/BFS periodically to seeker hinted position, meanwhile random just like Hider
        pass

grid = Grid()
hider = Hider()
seeker = Seeker()

# Debuging
grid.set_cell(hider.row, hider.col, hider.symbol)
grid.set_cell(seeker.row, seeker.col, seeker.symbol)

grid.print()
grid = hider.move_to(2, 2, grid)

print()
grid.print()

print(f"\n{hider.check_for_seeker(grid)}")

grid = seeker.move_to(3, 3, grid)
grid.print()

print(f"\n{hider.check_for_seeker(grid)}")

# TODO make the UI of my game
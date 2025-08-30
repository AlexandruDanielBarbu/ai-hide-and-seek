# Imports
import sys, pygame
import random, time
from grid import Grid
from entities import Hider, Seeker
from settings import SCREEN_SIZE, TILE_SIZE, FPS_VALUE
from agent import QAgent

def run_game():
    # Initial setup
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    fps = pygame.time.Clock()


    # Window settings
    pygame.display.set_caption('Hide and seek')
    game_icon = pygame.image.load('assets/sprites/logo.png')
    pygame.display.set_icon(game_icon)


    # Events
    SECOND = 1000
    MOVE_PLAYERS = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE_PLAYERS, int(0.01 * SECOND))


    actions = [0, 1, 2, 3]  # up, down, left, right
    q_agent = QAgent(actions)

    # Assets Init
    hider = Hider('assets/sprites/hider.png')
    seeker = Seeker('assets/sprites/seeker.png', q_agent)

    background = pygame.image.load('assets/sprites/background.png')
    background = pygame.transform.scale(background, SCREEN_SIZE)

    crate = pygame.image.load('assets/sprites/wall.png')
    crate = pygame.transform.scale(crate, (TILE_SIZE, TILE_SIZE))


    # Grid Init
    grid = Grid()
    grid.set_cell(hider.row, hider.col, hider.symbol)
    grid.set_cell(seeker.row, seeker.col, seeker.symbol)



    # Game loop
    while True:
        # Render background
        screen.blit(background, (0, 0))

        # handle game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                q_agent.save_table('q_table.pkl')
                pygame.quit()
                sys.exit()
            
            elif event.type == MOVE_PLAYERS:
                
                grid, action, state = seeker.advanced_brain(grid, hider)

                if hider.check_for_seeker(grid):
                    reward = 5
                    print('Found YOU')
                    q_agent.save_table('q_table.pkl')
                    return
                elif grid.grid[seeker.row][seeker.col] == 'W':
                    print('BAD')
                    reward = -2
                else:
                    reward = 0
                
                next_state = seeker.q_agent.get_state(hider, seeker)
                seeker.q_agent.update(state, action, reward, next_state)

                # update screen 
                grid.draw_self(screen, hider, seeker, crate)


        # draw grid
        grid.draw_self(screen, hider, seeker, crate)

        pygame.display.update()
        fps.tick(FPS_VALUE)

while True:
    run_game()
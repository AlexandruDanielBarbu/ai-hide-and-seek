# Imports
import sys, pygame
import random, time
from grid import Grid
from entities import Hider, Seeker
from settings import SCREEN_SIZE, TILE_SIZE, FPS_VALUE, GOAL_REWARDS
from settings import LAMBDA, HIDER_LOCATIONS, STEP_COST, BETA, REVISIT_PENALTY, WALL_PENALTY
from agent import QAgent

def manhattan(a, b): return abs(a[0]-b[0]) + abs(a[1]-b[1])

def phi(state, goals):
    r, c = state
    d =  min(manhattan((r,c), g) for g in goals)
    return -LAMBDA * d

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
    pygame.time.set_timer(MOVE_PLAYERS, int(0.001 * SECOND))


    actions = [0, 1, 2, 3]  # up, down, left, right
    q_agent = QAgent(actions)

    # Assets Init
    hider = Hider('assets/sprites/hider.png')
    seeker = Seeker('assets/sprites/seeker.png', q_agent)

    background = pygame.image.load('assets/sprites/background.png')
    background = pygame.transform.scale(background, SCREEN_SIZE)

    crate = pygame.image.load('assets/sprites/wall.png')
    crate = pygame.transform.scale(crate, (TILE_SIZE, TILE_SIZE))

    GOALS = {(hider.row, hider.col)}

    # Grid Init
    grid = Grid()
    grid.set_cell(hider.row, hider.col, hider.symbol)
    grid.set_cell(seeker.row, seeker.col, seeker.symbol)

    visited_states = set()
    steps = 0
    max_steps = 500

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
                
                grid, action, state, next_state = seeker.advanced_brain(grid, hider)

                
                # reward system 
                env_reward = STEP_COST
                done = False

                if (next_state == state) and grid.grid[next_state[0]][next_state[1]] == 'W':
                    env_reward += WALL_PENALTY


                if next_state in GOALS or hider.check_for_seeker(grid):
                    env_reward = GOAL_REWARDS.get(next_state, 1.0)
                    done = True

                if next_state in visited_states:
                    env_reward += REVISIT_PENALTY

                visited_states.add(next_state)
                
                # potential-based shaping
                shaped = env_reward + BETA * (q_agent.gamma * phi(next_state, GOALS) - phi(state, GOALS))

                seeker.q_agent.update(state, action, shaped, next_state, done)

                steps += 1
                if done or steps >= max_steps:
                    print(f"Episode finished in {steps} steps, reward={env_reward:.2f}")
                    q_agent.save_table('q_table.pkl')
                    q_agent.decay_temperature()
                    return

                # update screen 
                grid.draw_self(screen, hider, seeker, crate)


        # draw grid
        grid.draw_self(screen, hider, seeker, crate)

        pygame.display.update()
        fps.tick(FPS_VALUE)

while True:
    run_game()
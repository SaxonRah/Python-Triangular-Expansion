import pygame
import numpy as np
import math
from collections import deque

# Constants
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def create_grid():
    """
    Creates a grid with random True (walkable) and False (blocked) values.
    """
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=bool)
    grid[:, :] = np.random.choice([True, False], size=(GRID_WIDTH, GRID_HEIGHT), p=[0.7, 0.3])
    return grid

def is_visible(grid, observer, target):
    """
    Checks if the target cell is visible from the observer's position.
    Uses a raycasting approach.
    """
    observer_x, observer_y = observer
    target_x, target_y = target
    dx, dy = target_x - observer_x, target_y - observer_y
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return True

    for i in range(steps):
        t = i / steps
        ix = int(observer_x + t * dx)
        iy = int(observer_y + t * dy)

        if ix < 0 or iy < 0 or ix >= GRID_WIDTH or iy >= GRID_HEIGHT:
            return False

        # If a wall (black square) is encountered, stop visibility and mark as a blocking wall
        if not grid[ix, iy]:
            if (ix, iy) == target:
                return True  # The wall itself is visible
            return False

    return True

def compute_visibility(grid, observer):
    """
    Computes visible cells using a BFS approach from the observer's position.
    Returns both the visible cells and the blocking walls that are visible.
    """
    visible_cells = set()
    visible_walls = set()
    queue = deque([observer])
    visited = set()

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if is_visible(grid, observer, (x, y)):
            if grid[x, y]:
                visible_cells.add((x, y))
                # Check the 4 adjacent cells (up, down, left, right)
                for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                        queue.append((nx, ny))
            else:
                visible_walls.add((x, y))

    return visible_cells, visible_walls

def draw_grid(screen, grid, visible_walls):
    """
    Draws the grid on the screen.
    """
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if (x, y) in visible_walls:
                color = GRAY
            else:
                color = WHITE if grid[x, y] else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_visible_cells(screen, visible_cells):
    """
    Highlights the visible cells on the screen.
    """
    for (x, y) in visible_cells:
        pygame.draw.rect(screen, BLUE, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_observer(screen, observer_pos):
    """
    Draws the observer on the grid as a green square.
    """
    x, y = observer_pos
    pygame.draw.rect(screen, GREEN, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    pygame.display.set_caption('Raycast Grid Visibility 3')
    clock = pygame.time.Clock()
    grid = create_grid()
    observer_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
    visible_cells = set()
    visible_walls = set()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                observer_pos = (mouse_x // GRID_SIZE, mouse_y // GRID_SIZE)
                visible_cells, visible_walls = compute_visibility(grid, observer_pos)

        screen.fill(BLACK)
        draw_grid(screen, grid, visible_walls)
        draw_visible_cells(screen, visible_cells)
        draw_observer(screen, observer_pos)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()

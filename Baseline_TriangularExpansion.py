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
GRAY = (128, 128, 128)
RED = (255, 0, 0)

def create_grid():
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=bool)
    grid[:, :] = np.random.choice([True, False], size=(GRID_WIDTH, GRID_HEIGHT), p=[0.7, 0.3])
    return grid

def draw_grid(screen, grid, visibility):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if visibility[x, y]:
                color = WHITE if grid[x, y] else RED
            else:
                color = GRAY if grid[x, y] else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def is_visible_from(grid, pos):
    """ Determine visibility using triangular expansion. """
    width, height = grid.shape
    visibility = np.zeros_like(grid, dtype=bool)

    def in_bounds(x, y):
        return 0 <= x < width and 0 <= y < height

    def add_visibility(x, y):
        if in_bounds(x, y):
            visibility[x, y] = True

    def raycast(start, angle):
        """ Raycast from a start point in a given angle and mark visibility. """
        rad = math.radians(angle)
        x, y = start
        dx = math.cos(rad)
        dy = math.sin(rad)
        step = 0
        while True:
            cx = int(x + step * dx)
            cy = int(y + step * dy)
            if not in_bounds(cx, cy):
                break
            add_visibility(cx, cy)
            if not grid[cx, cy]:
                break
            step += 1

    def expand_triangles():
        """ Expands triangles from the viewpoint to mark visibility. """
        angle_step = 1  # Angle step for raycasting
        for angle in range(0, 360, angle_step):
            raycast(pos, angle)

    expand_triangles()
    return visibility

def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    pygame.display.set_caption('Visibility Calculation')
    clock = pygame.time.Clock()
    grid = create_grid()
    running = True
    mouse_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = (event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE)

        visibility = is_visible_from(grid, mouse_pos)

        screen.fill(BLACK)
        draw_grid(screen, grid, visibility)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

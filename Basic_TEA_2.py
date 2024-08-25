import pygame
import numpy as np
from scipy.spatial import Delaunay

# Constants
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def create_grid():
    """
    Creates a grid with random True (white) and False (black) values.
    """
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=bool)
    grid[:, :] = np.random.choice([True, False], size=(GRID_WIDTH, GRID_HEIGHT), p=[0.7, 0.3])
    return grid


def get_square_polygon(x, y):
    """
    Returns the polygon (as a list of points) for a square at grid position (x, y).
    """
    return [
        (x * GRID_SIZE, y * GRID_SIZE),
        ((x + 1) * GRID_SIZE, y * GRID_SIZE),
        ((x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE),
        (x * GRID_SIZE, (y + 1) * GRID_SIZE)
    ]


def triangulate_polygon(polygon):
    """
    Manually triangulates a polygon (assumed to be a rectangle here).
    """
    p1, p2, p3, p4 = polygon
    return [(p1, p2, p3), (p1, p3, p4)]


def is_partially_visible(triangle, observer, grid):
    """
    Checks if at least one vertex of the triangle is visible from the observer's position.
    """
    for point in triangle:
        if is_visible(point, observer, grid):
            return True
    return False


def get_square_center(mouse_pos):
    """
    Returns the center of the square that the mouse is currently over.
    """
    mouse_grid_x = (mouse_pos[0] // GRID_SIZE) * GRID_SIZE
    mouse_grid_y = (mouse_pos[1] // GRID_SIZE) * GRID_SIZE
    center_x = mouse_grid_x + GRID_SIZE // 2
    center_y = mouse_grid_y + GRID_SIZE // 2
    return (center_x, center_y)


def triangulate_grid(grid):
    """
    Triangulate the walkable areas of the grid.
    """
    points = []
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y]:  # Only consider white squares
                # Add the four corners of each square as points for triangulation
                points.append((x * GRID_SIZE, y * GRID_SIZE))
                points.append(((x + 1) * GRID_SIZE, y * GRID_SIZE))
                points.append(((x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE))
                points.append((x * GRID_SIZE, (y + 1) * GRID_SIZE))

    # Perform Delaunay triangulation on the points
    tri = Delaunay(points)
    return tri


def triangular_expansion(tri, observer, grid, screen=None):
    """
    Perform the triangular expansion to determine visible areas.
    """
    visible_triangles = []
    for simplex in tri.simplices:
        triangle = [tuple(tri.points[simplex[0]]), tuple(tri.points[simplex[1]]), tuple(tri.points[simplex[2]])]
        if is_triangle_visible(triangle, observer, grid, screen):
            visible_triangles.append(triangle)
    return visible_triangles


def draw_visible_triangles(screen, triangles, observer, grid):
    """
    Draw visible triangles based on TEA.
    """
    for triangle in triangles:
        pygame.draw.polygon(screen, BLUE, triangle, 1)


def is_visible(point, observer, grid, screen=None):
    """
    Checks if a point is visible from the center of the square the mouse is on.
    Draws a line from the observer to the point for debugging purposes, but only if the point is visible.
    Blocks visibility if the line passes through the corner where two black squares meet.
    """
    observer_x, observer_y = observer
    px, py = point
    dx, dy = px - observer_x, py - observer_y
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return True

    observer_grid_x = observer_x // GRID_SIZE
    observer_grid_y = observer_y // GRID_SIZE

    for i in range(int(steps)):
        t = i / steps
        ix = int(observer_x + t * dx) // GRID_SIZE
        iy = int(observer_y + t * dy) // GRID_SIZE

        if ix < 0 or iy < 0 or ix >= GRID_WIDTH or iy >= GRID_HEIGHT or not grid[ix, iy]:
            return False

        # Check for diagonal blocking (corner case)
        if ix != observer_grid_x and iy != observer_grid_y:
            # If the line passes through a corner formed by two black squares, block visibility
            if (not grid[ix, observer_grid_y] and not grid[observer_grid_x, iy]) or not grid[ix, iy]:
                return False

        # Additional check for corner passing
        if ix != observer_grid_x and iy != observer_grid_y:
            if (not grid[observer_grid_x, iy] and not grid[ix, observer_grid_y]):
                return False

    # Draw a line for visualization if the point is visible
    if screen is not None:
        pygame.draw.line(screen, GREEN, (observer_x, observer_y), (px, py), 1)

    return True


def draw_triangles(screen, triangles, observer, grid):
    """
    Draws the triangles on the screen, coloring them based on visibility.
    Uses the center of the square the mouse is on for visibility checks.
    """
    observer_center = get_square_center(observer)

    for triangle in triangles:
        points = [(p[0], p[1]) for p in triangle]
        visible = False

        # Check visibility from the center of the observer's square
        if is_visible(points[0], observer_center, grid, screen) or \
                is_visible(points[1], observer_center, grid, screen) or \
                is_visible(points[2], observer_center, grid, screen):
            visible = True

        if visible:
            color = BLUE
        else:
            color = RED

        pygame.draw.polygon(screen, color, points, 1)


def is_triangle_visible(triangle, observer, grid, screen=None):
    """
    Determines if the triangle is visible from the observer's position.
    Draws lines from the observer to each vertex of the triangle for debugging, but only if visible.
    """
    for point in triangle:
        if is_visible(point, observer, grid, screen):
            return True
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    pygame.display.set_caption('Basic TEA 2')
    clock = pygame.time.Clock()
    grid = create_grid()
    tri = triangulate_grid(grid)  # Triangulate grid at the start
    running = True
    observer_pos = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)  # Initialize observer position

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                observer_pos = event.pos

        screen.fill(BLACK)

        # Draw the grid
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                color = WHITE if grid[x, y] else BLACK
                pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Calculate visible triangles
        visible_triangles = triangular_expansion(tri, observer_pos, grid, screen)

        # Draw the visible triangles
        draw_visible_triangles(screen, visible_triangles, observer_pos, grid)

        pygame.draw.rect(screen, GREEN,
                         pygame.Rect(observer_pos[0] // GRID_SIZE * GRID_SIZE, observer_pos[1] // GRID_SIZE * GRID_SIZE,
                                     GRID_SIZE, GRID_SIZE))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()

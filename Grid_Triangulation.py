import pygame
import numpy as np
import shapely
from shapely.geometry import Polygon
from shapely.ops import triangulate, unary_union

# Constants
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def create_grid():
    """
    Creates a grid with random True (white) and False (black) values.
    """
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=bool)
    grid[:, :] = np.random.choice([True, False], size=(GRID_WIDTH, GRID_HEIGHT), p=[0.7, 0.3])
    return grid


def get_square_polygon(x, y):
    """
    Returns the Polygon for a square at grid position (x, y).
    """
    return Polygon([
        (x * GRID_SIZE, y * GRID_SIZE),
        ((x + 1) * GRID_SIZE, y * GRID_SIZE),
        ((x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE),
        (x * GRID_SIZE, (y + 1) * GRID_SIZE)
    ])


def compute_visibility_polygon(grid):
    """
    Computes the visibility polygon based on the white squares.
    """
    polygons = []

    # Collect all white square polygons
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y]:  # White square
                polygons.append(get_square_polygon(x, y))

    # Union all white square polygons into a single (or multiple) polygons
    visibility_polygon = unary_union(polygons)

    shapely.simplify(visibility_polygon, tolerance=4, preserve_topology=True)

    return visibility_polygon


def draw_triangles(screen, triangles):
    """
    Draws the edges of the triangles on the screen.
    """
    for triangle in triangles:
        points = list(triangle.exterior.coords)
        pygame.draw.line(screen, RED, points[0], points[1], 1)
        pygame.draw.line(screen, RED, points[1], points[2], 1)
        pygame.draw.line(screen, RED, points[2], points[0], 1)


def main():
    """
    Main function to run the Pygame loop.
    """
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    pygame.display.set_caption('Grid Triangulation')
    clock = pygame.time.Clock()
    grid = create_grid()
    running = True
    observer_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)  # Initialize observer position

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                # Update observer position based on mouse movement
                mouse_x, mouse_y = event.pos
                observer_pos = (mouse_x // GRID_SIZE, mouse_y // GRID_SIZE)

        screen.fill(BLACK)  # Clear the screen

        # Compute the visibility polygon
        visibility_polygon = compute_visibility_polygon(grid)

        # Triangulate the visibility polygon
        triangles = triangulate(visibility_polygon)

        # Draw the grid
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if grid[x, y]:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the triangles within the visibility polygon
        draw_triangles(screen, triangles)

        # Highlight observer position
        pygame.draw.rect(screen, GREEN,
                         pygame.Rect(observer_pos[0] * GRID_SIZE, observer_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Limit to 30 FPS

    pygame.quit()


if __name__ == "__main__":
    main()

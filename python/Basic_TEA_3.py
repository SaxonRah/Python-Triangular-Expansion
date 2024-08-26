import pygame
import triangle
import numpy as np

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


def triangulate_grid_with_cdt(grid):
    """
    Triangulate the grid using Constrained Delaunay Triangulation (CDT).
    """
    points = []
    segments = []
    point_index = {}

    # Collect points and segments (edges) for the CDT
    index = 0
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y]:  # Only consider white squares
                # Add the four corners of each square as points for triangulation
                p1 = (x * GRID_SIZE, y * GRID_SIZE)
                p2 = ((x + 1) * GRID_SIZE, y * GRID_SIZE)
                p3 = ((x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE)
                p4 = (x * GRID_SIZE, (y + 1) * GRID_SIZE)

                for p in [p1, p2, p3, p4]:
                    if p not in point_index:
                        point_index[p] = index
                        points.append(p)
                        index += 1

                # Add segments for the edges of the square
                segments.append((point_index[p1], point_index[p2]))
                segments.append((point_index[p2], point_index[p3]))
                segments.append((point_index[p3], point_index[p4]))
                segments.append((point_index[p4], point_index[p1]))

    # Prepare data for the triangle library
    prep_data = dict(vertices=np.array(points), segments=np.array(segments))

    # Perform CDT using the triangle library
    t = triangle.triangulate(prep_data, 'p')

    return t


def triangular_expansion_cdt(cdt, observer, grid, screen=None):
    """
    Perform the triangular expansion using CDT to determine visible areas.
    Handles visibility polygons with antennae by considering extended visibility.
    """
    visible_triangles = []
    for triangle_indices in cdt['triangles']:
        temp_triangle = [tuple(cdt['vertices'][index]) for index in triangle_indices]
        if is_triangle_visible(temp_triangle, observer, grid, screen):
            visible_triangles.append(temp_triangle)
    return visible_triangles


def create_grid():
    """
    Creates a grid with random True (white) and False (black) values.
    """
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=bool)
    grid[:, :] = np.random.choice([True, False], size=(GRID_WIDTH, GRID_HEIGHT), p=[0.7, 0.3])
    return grid


def get_square_center(mouse_pos):
    """
    Returns the center of the square that the mouse is currently over.
    """
    mouse_grid_x = (mouse_pos[0] // GRID_SIZE) * GRID_SIZE
    mouse_grid_y = (mouse_pos[1] // GRID_SIZE) * GRID_SIZE
    center_x = mouse_grid_x + GRID_SIZE // 2
    center_y = mouse_grid_y + GRID_SIZE // 2
    return center_x, center_y


def is_visible(point, observer, grid, screen=None):
    """
    Checks if a point is visible from the center of the square the mouse is on.
    Draws a line from the observer to the point for debugging purposes, but only if the point is visible.
    Handles cases where the visibility polygon extends into narrow regions, creating "antennae."
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
            if not grid[observer_grid_x, iy] and not grid[ix, observer_grid_y]:
                return False

    # Handle antennae by continuing visibility along the line
    # This part ensures that if the visibility line extends into an antenna, it's still considered visible
    if grid[observer_grid_x, observer_grid_y] and grid[ix, iy]:
        return True

    # Draw a line for visualization if the point is visible
    if screen is not None:
        pygame.draw.line(screen, GREEN, (observer_x, observer_y), (px, py), 1)

    return False


def draw_triangles(screen, triangles, observer, grid):
    """
    Draws the triangles on the screen, coloring them based on visibility.
    Handles the drawing of visibility polygons with antennae.
    """
    observer_center = get_square_center(observer)

    for temp_triangle in triangles:
        points = [(p[0], p[1]) for p in temp_triangle]
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


def is_triangle_visible(given_triangle, observer, grid, screen=None):
    """
    Determines if the triangle is visible from the observer's position.
    Draws lines from the observer to each vertex of the triangle for debugging, but only if visible.
    """
    for point in given_triangle:
        if is_visible(point, observer, grid, screen):
            return True
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    pygame.display.set_caption('Basic TEA 3')
    clock = pygame.time.Clock()
    grid = create_grid()
    cdt = triangulate_grid_with_cdt(grid)  # Triangulate grid with CDT at the start
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
        visible_triangles = triangular_expansion_cdt(cdt, observer_pos, grid, screen)

        # Draw the triangles
        draw_triangles(screen, visible_triangles, observer_pos, grid)

        pygame.draw.rect(screen, GREEN,
                         pygame.Rect(observer_pos[0] // GRID_SIZE * GRID_SIZE, observer_pos[1] // GRID_SIZE * GRID_SIZE,
                                     GRID_SIZE, GRID_SIZE))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()

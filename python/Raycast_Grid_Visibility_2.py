import pygame
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


def create_grid():
    """
    Creates a grid with random True (white) and False (black) values.
    """
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=bool)
    grid[:, :] = np.random.choice([True, False], size=(GRID_WIDTH, GRID_HEIGHT), p=[0.7, 0.3])
    return grid


def is_point_in_polygon(x, y, polygon):
    """
    Checks if a point (x, y) is inside a polygon.
    Uses the ray-casting algorithm.
    """
    n = len(polygon)
    inside = False

    px, py = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(py, p2y):
            if y <= max(py, p2y):
                if x <= max(px, p2x):
                    if py != p2y:
                        xinters = (y - py) * (p2x - px) / (p2y - py) + px
                    if px == p2x or x <= xinters:
                        inside = not inside
        px, py = p2x, p2y

    return inside


def compute_visibility_polygon(grid, observer):
    """
    Computes the visibility polygon from the observer's position.
    """
    ox, oy = observer
    visibility_polygon = []

    for angle in range(0, 360, 5):  # Check every 5 degrees
        angle_rad = np.radians(angle)
        dx = np.cos(angle_rad)
        dy = np.sin(angle_rad)

        for dist in range(1, max(GRID_WIDTH, GRID_HEIGHT) * GRID_SIZE):
            x = ox * GRID_SIZE + dist * dx
            y = oy * GRID_SIZE + dist * dy
            grid_x, grid_y = int(x // GRID_SIZE), int(y // GRID_SIZE)

            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                if not grid[grid_x, grid_y]:  # Hit an obstacle
                    break
            visibility_polygon.append((x, y))

    return visibility_polygon


def draw_polygon(screen, polygon):
    """
    Draws the visibility polygon on the screen.
    """
    if len(polygon) > 2:
        pygame.draw.polygon(screen, RED, polygon, 1)


def main():
    """
    Main function to run the Pygame loop.
    """
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    pygame.display.set_caption('Raycast Grid Visibility 2')
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
        visibility_polygon = compute_visibility_polygon(grid, observer_pos)

        # Draw the grid
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if grid[x, y]:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the visibility polygon
        draw_polygon(screen, visibility_polygon)

        # Highlight observer position
        pygame.draw.rect(screen, GREEN,
                         pygame.Rect(observer_pos[0] * GRID_SIZE, observer_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit to 30 FPS
        print(clock.get_fps())

    pygame.quit()


if __name__ == "__main__":
    main()

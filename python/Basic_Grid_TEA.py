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
BLUE = (0, 0, 255)


def create_grid():
    """
    Creates a grid with random True (white) and False (black) values.
    """
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=bool)
    grid[:, :] = np.random.choice([True, False], size=(GRID_WIDTH, GRID_HEIGHT), p=[0.7, 0.3])
    return grid


def get_polygon(x, y):
    """
    Returns the corner points of the square at (x, y) as a polygon.
    """
    top_left = (x * GRID_SIZE, y * GRID_SIZE)
    top_right = ((x + 1) * GRID_SIZE, y * GRID_SIZE)
    bottom_right = ((x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE)
    bottom_left = (x * GRID_SIZE, (y + 1) * GRID_SIZE)
    return [top_left, top_right, bottom_right, bottom_left]


def draw_grid(screen, grid):
    """
    Draws the grid squares on the screen.
    """
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y]:
                color = WHITE
            else:
                color = BLACK
            pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def draw_triangles(screen, grid, mouse_pos):
    """
    Applies triangular expansion algorithm and colors visible and non-visible triangles.
    """

    def is_point_visible(point, given_mouse_pos, given_grid):
        """
        Determine if a point is visible from the mouse's position.
        """
        mouse_x, mouse_y = given_mouse_pos
        point_x, point_y = point[0] // GRID_SIZE, point[1] // GRID_SIZE

        if point_x == mouse_x and point_y == mouse_y:
            return True

        dx = point_x - mouse_x
        dy = point_y - mouse_y

        steps = max(abs(dx), abs(dy))
        for i in range(int(steps)):
            temp_x = int(mouse_x + dx * i / steps)
            temp_y = int(mouse_y + dy * i / steps)
            if (temp_x < 0 or temp_x >= GRID_WIDTH
                    or temp_y < 0 or temp_y >= GRID_HEIGHT or not given_grid[temp_x, temp_y]):
                return False
        return True

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y]:
                # Define the two triangles by splitting the square diagonally
                polygon = get_polygon(x, y)
                triangle1 = [polygon[0], polygon[1], polygon[2]]
                triangle2 = [polygon[0], polygon[2], polygon[3]]

                # Check visibility of the center of each triangle
                center1 = np.mean(triangle1, axis=0)
                center2 = np.mean(triangle2, axis=0)

                visible1 = is_point_visible(center1, mouse_pos, grid)
                visible2 = is_point_visible(center2, mouse_pos, grid)

                # Fill the square with appropriate visibility color
                square_color = GRAY if visible1 or visible2 else WHITE
                pygame.draw.rect(screen, square_color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

                # Draw the first triangle outline
                color = BLUE if visible1 else RED
                pygame.draw.polygon(screen, color, triangle1, 1)  # Outline only

                # Draw the second triangle outline
                color = BLUE if visible2 else RED
                pygame.draw.polygon(screen, color, triangle2, 1)  # Outline only


def draw_mouse(screen, mouse_pos):
    """
    Draws the green square at the mouse position.
    """
    x, y = mouse_pos
    pygame.draw.rect(screen, GREEN, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def main():
    """
    Main function to run the Pygame loop.
    """
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    pygame.display.set_caption('Basic Grid TEA')
    clock = pygame.time.Clock()
    grid = create_grid()
    running = True
    mouse_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)  # Initialize mouse position

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                # Update mouse position based on mouse movement
                mouse_x, mouse_y = event.pos
                mouse_pos = (mouse_x // GRID_SIZE, mouse_y // GRID_SIZE)

        screen.fill(BLACK)  # Clear the screen
        draw_grid(screen, grid)  # Draw the grid
        draw_triangles(screen, grid, mouse_pos)  # Draw the triangles
        draw_mouse(screen, mouse_pos)  # Draw the green square for the mouse location

        pygame.display.flip()  # Update the display
        clock.tick(60)
        print(clock.get_fps())

    pygame.quit()


if __name__ == "__main__":
    main()

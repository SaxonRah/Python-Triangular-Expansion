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


def draw_grid(screen, grid, mouse_pos):
    """
    Draws the grid squares on the screen.
    """
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if (x, y) == mouse_pos:
                color = GREEN  # Highlight the mouse position
            elif grid[x, y]:
                color = WHITE
            else:
                color = BLACK
            pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def draw_triangles(screen, grid):
    """
    Splits each white square into two triangles and draws their edges.
    Black squares are treated as holes and their triangles are not drawn.
    """
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y]:
                # Define the four corner points of the square
                top_left = (x * GRID_SIZE, y * GRID_SIZE)
                top_right = ((x + 1) * GRID_SIZE, y * GRID_SIZE)
                bottom_right = ((x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE)
                bottom_left = (x * GRID_SIZE, (y + 1) * GRID_SIZE)

                # Define two triangles by splitting the square diagonally
                triangle1 = [top_left, top_right, bottom_right]
                triangle2 = [top_left, bottom_right, bottom_left]

                # Draw edges of the first triangle
                pygame.draw.line(screen, RED, triangle1[0], triangle1[1], 1)
                pygame.draw.line(screen, RED, triangle1[1], triangle1[2], 1)
                pygame.draw.line(screen, RED, triangle1[2], triangle1[0], 1)

                # Draw edges of the second triangle
                pygame.draw.line(screen, RED, triangle2[0], triangle2[1], 1)
                pygame.draw.line(screen, RED, triangle2[1], triangle2[2], 1)
                pygame.draw.line(screen, RED, triangle2[2], triangle2[0], 1)


def main():
    """
    Main function to run the Pygame loop.
    """
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    pygame.display.set_caption('Delaunay Triangulation with Holes')
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
        draw_grid(screen, grid, mouse_pos)  # Draw the grid
        draw_triangles(screen, grid)  # Draw the triangle edges

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit to 30 FPS
        print(clock.get_fps())

    pygame.quit()


if __name__ == "__main__":
    main()

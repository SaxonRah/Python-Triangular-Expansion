import sdl2
import sdl2.ext
import numpy as np
import math

# Constants
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WHITE = sdl2.ext.Color(255, 255, 255)
BLACK = sdl2.ext.Color(0, 0, 0)
RED = sdl2.ext.Color(255, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
BLUE = sdl2.ext.Color(0, 0, 255)


# Helper Functions
def create_grid():
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=bool)
    grid[:, :] = np.random.choice([True, False], size=(GRID_WIDTH, GRID_HEIGHT), p=[0.7, 0.3])
    return grid


def get_square_polygon(x, y):
    return [
        (x * GRID_SIZE, y * GRID_SIZE),
        ((x + 1) * GRID_SIZE, y * GRID_SIZE),
        ((x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE),
        (x * GRID_SIZE, (y + 1) * GRID_SIZE)
    ]


def triangulate_polygon(polygon):
    p1, p2, p3, p4 = polygon
    return [(p1, p2, p3), (p1, p3, p4)]


# Visibility Functions
def is_visible(point, observer, grid):
    observer_x, observer_y = observer
    px, py = point
    dx, dy = px - observer_x, py - observer_y
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return True

    for i in range(steps):
        t = i / steps
        ix = int(observer_x + t * dx) // GRID_SIZE
        iy = int(observer_y + t * dy) // GRID_SIZE

        if ix < 0 or iy < 0 or ix >= GRID_WIDTH or iy >= GRID_HEIGHT or not grid[ix, iy]:
            return False

        if ix != observer_x // GRID_SIZE and iy != observer_y // GRID_SIZE:
            if (not grid[ix, observer_y // GRID_SIZE] and not grid[observer_x // GRID_SIZE, iy]) or not grid[ix, iy]:
                return False

    return True


def triangulate_walkable_area(grid):
    triangles = []
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y]:
                polygon = get_square_polygon(x, y)
                triangles.extend(triangulate_polygon(polygon))
    return triangles


def find_observer_triangle(observer_pos, triangles):
    for triangle in triangles:
        if point_in_triangle(observer_pos, triangle):
            return triangle
    return None


def point_in_triangle(point, triangle):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    d1 = sign(point, triangle[0], triangle[1])
    d2 = sign(point, triangle[1], triangle[2])
    d3 = sign(point, triangle[2], triangle[0])

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)


def recursive_visibility_expansion(observer_pos, triangle, triangles, visible_triangles, grid):
    if triangle in visible_triangles:
        return
    visible_triangles.add(triangle)

    for neighbor in find_neighbors(triangle, triangles):
        if is_visible_from_triangle(observer_pos, neighbor, triangle, grid):
            recursive_visibility_expansion(observer_pos, neighbor, triangles, visible_triangles, grid)


def find_neighbors(triangle, triangles):
    neighbors = []
    for other in triangles:
        if other != triangle and shares_edge(triangle, other):
            neighbors.append(other)
    return neighbors


def shares_edge(triangle1, triangle2):
    shared_points = set(triangle1) & set(triangle2)
    return len(shared_points) == 2


def is_visible_from_triangle(observer_pos, neighbor, current_triangle, grid):
    shared_edge = tuple(set(current_triangle) & set(neighbor))
    if len(shared_edge) == 2:
        if is_visible(shared_edge[0], observer_pos, grid) and is_visible(shared_edge[1], observer_pos, grid):
            return True
    return False


# Rendering
def draw_grid(renderer, grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y]:
                color = WHITE
            else:
                color = BLACK

            # Set the drawing color
            sdl2.SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a)

            rect = sdl2.SDL_Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            sdl2.SDL_RenderFillRect(renderer, rect)


def draw_visible_triangles(renderer, visible_triangles):
    for triangle in visible_triangles:
        p1, p2, p3 = triangle

        # Set the drawing color for lines
        sdl2.SDL_SetRenderDrawColor(renderer, RED.r, RED.g, RED.b, RED.a)

        sdl2.SDL_RenderDrawLine(renderer, p1[0], p1[1], p2[0], p2[1])
        sdl2.SDL_RenderDrawLine(renderer, p2[0], p2[1], p3[0], p3[1])
        sdl2.SDL_RenderDrawLine(renderer, p3[0], p3[1], p1[0], p1[1])


def main():
    sdl2.ext.init()
    window = sdl2.ext.Window("TEA Visibility with PySDL2", size=(GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    window.show()
    renderer = sdl2.SDL_CreateRenderer(window.window, -1, 0)

    grid = create_grid()
    triangles = triangulate_walkable_area(grid)
    visible_triangles = set()

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            elif event.type == sdl2.SDL_MOUSEMOTION:
                observer_pos = event.motion.x, event.motion.y
                visible_triangles.clear()
                observer_triangle = find_observer_triangle(observer_pos, triangles)
                if observer_triangle:
                    recursive_visibility_expansion(observer_pos, observer_triangle, triangles, visible_triangles, grid)

        sdl2.SDL_SetRenderDrawColor(renderer, BLACK.r, BLACK.g, BLACK.b, BLACK.a)
        sdl2.SDL_RenderClear(renderer)

        draw_grid(renderer, grid)
        draw_visible_triangles(renderer, visible_triangles)

        sdl2.SDL_RenderPresent(renderer)

    sdl2.SDL_DestroyRenderer(renderer)
    sdl2.ext.quit()


if __name__ == "__main__":
    main()

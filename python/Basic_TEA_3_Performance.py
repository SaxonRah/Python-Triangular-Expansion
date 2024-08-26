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
    points = []
    segments = []
    point_index = {}

    index = 0
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y]:  # Only consider white squares
                p1 = (x * GRID_SIZE, y * GRID_SIZE)
                p2 = ((x + 1) * GRID_SIZE, y * GRID_SIZE)
                p3 = ((x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE)
                p4 = (x * GRID_SIZE, (y + 1) * GRID_SIZE)

                for p in [p1, p2, p3, p4]:
                    if p not in point_index:
                        point_index[p] = index
                        points.append(p)
                        index += 1

                segments.append((point_index[p1], point_index[p2]))
                segments.append((point_index[p2], point_index[p3]))
                segments.append((point_index[p3], point_index[p4]))
                segments.append((point_index[p4], point_index[p1]))

    prep_data = dict(vertices=np.array(points), segments=np.array(segments))
    t = triangle.triangulate(prep_data, 'p')

    return t


def precompute_triangle_adjacencies(cdt):
    adjacencies = {}
    for triangle_index, temp_triangle in enumerate(cdt['triangles']):
        for i in range(3):
            edge_start = tuple(cdt['vertices'][temp_triangle[i]])
            edge_end = tuple(cdt['vertices'][temp_triangle[(i + 1) % 3]])
            edge = frozenset([edge_start, edge_end])
            if edge in adjacencies:
                adjacencies[edge].append(triangle_index)
            else:
                adjacencies[edge] = [triangle_index]
    return adjacencies


def iterative_visibility_expansion(cdt, observer_triangle_index, observer, grid, adjacencies, screen=None):
    visible_triangles = []
    stack = [observer_triangle_index]
    visited_triangles = set()

    while stack:
        triangle_index = stack.pop()
        if triangle_index in visited_triangles:
            continue
        visited_triangles.add(triangle_index)

        current_triangle = [tuple(cdt['vertices'][index]) for index in cdt['triangles'][triangle_index]]
        if not is_triangle_visible(current_triangle, observer, grid, screen):
            continue

        visible_triangles.append(current_triangle)

        for i in range(3):
            edge_start = current_triangle[i]
            edge_end = current_triangle[(i + 1) % 3]
            adjacent_triangles = get_adjacent_triangles(adjacencies, triangle_index, edge_start, edge_end)
            stack.extend(adjacent_triangles)

    return visible_triangles


def get_adjacent_triangles(adjacencies, current_triangle_index, edge_start, edge_end):
    edge = frozenset([edge_start, edge_end])
    return [index for index in adjacencies.get(edge, []) if index != current_triangle_index]


def triangular_expansion_cdt(cdt, observer, grid, adjacencies, screen=None):
    visible_triangles = []
    observer_triangle_index = find_observer_triangle(cdt, observer)
    if observer_triangle_index is not None:
        visible_triangles = iterative_visibility_expansion(cdt, observer_triangle_index, observer, grid, adjacencies,
                                                           screen)

    return visible_triangles


def find_observer_triangle(cdt, observer):
    for triangle_index, temp_triangle in enumerate(cdt['triangles']):
        vertices = [tuple(cdt['vertices'][index]) for index in temp_triangle]
        if is_point_in_triangle(observer, vertices):
            return triangle_index
    return None


def is_point_in_triangle(pt, tri):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    d1 = sign(pt, tri[0], tri[1])
    d2 = sign(pt, tri[1], tri[2])
    d3 = sign(pt, tri[2], tri[0])

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)


def create_grid():
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=bool)
    grid[:, :] = np.random.choice([True, False], size=(GRID_WIDTH, GRID_HEIGHT), p=[0.7, 0.3])
    return grid


def get_square_center(mouse_pos):
    mouse_grid_x = (mouse_pos[0] // GRID_SIZE) * GRID_SIZE
    mouse_grid_y = (mouse_pos[1] // GRID_SIZE) * GRID_SIZE
    center_x = mouse_grid_x + GRID_SIZE // 2
    center_y = mouse_grid_y + GRID_SIZE // 2
    return center_x, center_y


def is_visible(point, observer, grid, screen=None):
    observer_x, observer_y = observer
    px, py = point
    dx, dy = px - observer_x, py - observer_y
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return True

    observer_grid_x = observer_x // GRID_SIZE
    observer_grid_y = observer_y // GRID_SIZE

    ix, iy = 0, 0

    for i in range(int(steps)):
        t = i / steps
        ix = int(observer_x + t * dx) // GRID_SIZE
        iy = int(observer_y + t * dy) // GRID_SIZE

        if ix < 0 or iy < 0 or ix >= GRID_WIDTH or iy >= GRID_HEIGHT or not grid[ix, iy]:
            return False

        if ix != observer_grid_x and iy != observer_grid_y:
            if (not grid[ix, observer_grid_y] and not grid[observer_grid_x, iy]) or not grid[ix, iy]:
                return False

        if ix != observer_grid_x and iy != observer_grid_y:
            if not grid[observer_grid_x, iy] and not grid[ix, observer_grid_y]:
                return False

    if grid[observer_grid_x, observer_grid_y] and grid[ix, iy]:
        return True

    if screen is not None:
        pygame.draw.line(screen, GREEN, (observer_x, observer_y), (px, py), 1)

    return False


def draw_triangles(screen, triangles, observer, grid):
    observer_center = get_square_center(observer)

    for temp_triangle in triangles:
        points = [(p[0], p[1]) for p in temp_triangle]
        visible = False

        if is_visible(points[0], observer_center, grid, screen) or \
                is_visible(points[1], observer_center, grid, screen) or \
                is_visible(points[2], observer_center, grid, screen):
            visible = True

        color = BLUE if visible else RED
        pygame.draw.polygon(screen, color, points, 1)


def is_triangle_visible(given_triangle, observer, grid, screen=None):
    for point in given_triangle:
        if is_visible(point, observer, grid, screen):
            return True
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    pygame.display.set_caption('Basic TEA 3 Performance')
    clock = pygame.time.Clock()
    grid = create_grid()
    cdt = triangulate_grid_with_cdt(grid)
    adjacencies = precompute_triangle_adjacencies(cdt)
    running = True
    observer_pos = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                observer_pos = event.pos

        screen.fill(BLACK)

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                color = WHITE if grid[x, y] else BLACK
                pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        visible_triangles = triangular_expansion_cdt(cdt, observer_pos, grid, adjacencies, screen)
        draw_triangles(screen, visible_triangles, observer_pos, grid)

        pygame.draw.rect(screen, GREEN,
                         pygame.Rect(observer_pos[0] // GRID_SIZE * GRID_SIZE, observer_pos[1] // GRID_SIZE * GRID_SIZE,
                                     GRID_SIZE, GRID_SIZE))
        pygame.display.flip()
        clock.tick(60)
        print(clock.get_fps())

    pygame.quit()


if __name__ == "__main__":
    main()

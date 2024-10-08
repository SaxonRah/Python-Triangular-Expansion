import pygame
import sys
from math import sqrt
import random

# Constants
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 128, 128  # Grid size
CELL_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)


class Triangle:
    def __init__(self, vertices, is_obstacle=False):
        self.vertices = vertices
        self.edges = [(tuple(vertices[i]), tuple(vertices[(i + 1) % 3])) for i in range(3)]
        self.neighbors = [None, None, None]
        self.is_obstacle = is_obstacle

    def draw(self, screen, color, fill=False):
        if fill:
            pygame.draw.polygon(screen, color, self.vertices)
        pygame.draw.polygon(screen, color, self.vertices, 1)

    def contains_point(self, point):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(point, self.vertices[0], self.vertices[1]) < 0.0
        b2 = sign(point, self.vertices[1], self.vertices[2]) < 0.0
        b3 = sign(point, self.vertices[2], self.vertices[0]) < 0.0

        return (b1 == b2) and (b2 == b3)


def bounding_box(vertices):
    x_coords, y_coords = zip(*vertices)
    return min(x_coords), max(x_coords), min(y_coords), max(y_coords)


def box_intersects_line(p, q, box):
    (min_x, max_x, min_y, max_y) = box
    return not (q[0] < min_x and p[0] < min_x or
                q[0] > max_x and p[0] > max_x or
                q[1] < min_y and p[1] < min_y or
                q[1] > max_y and p[1] > max_y)


def line_intersects_triangle(p, q, vertices):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    edges = [(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices))]

    for edge in edges:
        temp_a, temp_b = edge
        temp_c, temp_d = p, q
        if (ccw(temp_a, temp_c, temp_d) != ccw(temp_b, temp_c, temp_d) and
                ccw(temp_a, temp_b, temp_c) != ccw(temp_a, temp_b, temp_d)):
            return True
    return False


def generate_grid(rows, cols, cell_size):
    grid = []
    holes = []
    hole_boxes = []
    for row in range(rows):
        for col in range(cols):
            x = col * cell_size
            y = row * cell_size
            vertices = [(x, y), (x + cell_size, y), (x, y + cell_size), (x + cell_size, y + cell_size)]

            if random.random() < 0.2:  # 20% chance to be a hole
                holes.append(vertices)
                hole_boxes.append(bounding_box(vertices))
                # Mark these vertices as obstacles
                tri1 = Triangle([vertices[0], vertices[1], vertices[3]], is_obstacle=True)
                tri2 = Triangle([vertices[0], vertices[3], vertices[2]], is_obstacle=True)
            else:
                tri1 = Triangle([vertices[0], vertices[1], vertices[3]])
                tri2 = Triangle([vertices[0], vertices[3], vertices[2]])
            grid.append(tri1)
            grid.append(tri2)

    return grid, holes, hole_boxes


def d_TEA(triangle, point, visibility_range, visited_triangles, obstacles, obstacle_boxes):
    visible_triangles = []

    def expand(given_triangle):
        if given_triangle in visited_triangles or given_triangle.is_obstacle:
            return
        visited_triangles.add(given_triangle)
        visible_triangles.append(given_triangle)

        for i, edge in enumerate(given_triangle.edges):
            neighbor = given_triangle.neighbors[i]
            if not neighbor or neighbor.is_obstacle:
                continue

            edge_midpoint = ((edge[0][0] + edge[1][0]) / 2, (edge[0][1] + edge[1][1]) / 2)

            # First filter obstacles using bounding boxes for a quick rejection test
            if any(box_intersects_line(point, edge_midpoint, box) and
                   line_intersects_triangle(point, edge_midpoint, obs)
                   for obs, box in zip(obstacles, obstacle_boxes)):
                continue

            distance = sqrt((point[0] - edge_midpoint[0]) ** 2 + (point[1] - edge_midpoint[1]) ** 2)

            if distance <= visibility_range:
                expand(neighbor)

    expand(triangle)
    return visible_triangles


def assign_neighbors(triangles):
    edge_to_triangle = {}

    for tri in triangles:
        for i, edge in enumerate(tri.edges):
            edge_key = tuple(sorted(edge))
            if edge_key in edge_to_triangle:
                other_tri, other_edge_index = edge_to_triangle[edge_key]
                tri.neighbors[i] = other_tri
                other_tri.neighbors[other_edge_index] = tri
            else:
                edge_to_triangle[edge_key] = (tri, i)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Optimized d-TEA on Grid 2')

    clock = pygame.time.Clock()
    grid, holes, hole_boxes = generate_grid(ROWS, COLS, CELL_SIZE)
    assign_neighbors(grid)

    visibility_range = 200

    while True:
        screen.fill(WHITE)

        # Get mouse position for moving the query point
        query_point = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Find the current triangle the query point is in
        current_triangle = None
        for triangle in grid:
            if triangle.contains_point(query_point):
                current_triangle = triangle
                break

        # Draw the grid (all triangles)
        for triangle in grid:
            triangle.draw(screen, BLACK)

        # Draw the visible triangles in blue
        if current_triangle:
            visited_triangles = set()
            visible_triangles = d_TEA(current_triangle, query_point, visibility_range, visited_triangles, holes,
                                      hole_boxes)
            for triangle in visible_triangles:
                triangle.draw(screen, BLUE, fill=True)

        # Draw the triangle containing the query point in green
        if current_triangle:
            current_triangle.draw(screen, GREEN, fill=True)

        # Draw the holes (blocking polygons)
        for hole in holes:
            pygame.draw.polygon(screen, ORANGE, hole)

        # Draw the query point
        pygame.draw.circle(screen, RED, query_point, 5)

        pygame.display.flip()
        clock.tick(60)
        print(clock.get_fps())


if __name__ == "__main__":
    main()

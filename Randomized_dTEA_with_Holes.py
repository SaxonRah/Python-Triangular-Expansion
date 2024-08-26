import pygame
import sys
import random
from math import sqrt, cos, sin, pi
import triangle as tr
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)


class Triangle:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = [(tuple(vertices[i]), tuple(vertices[(i + 1) % 3])) for i in range(3)]
        self.neighbors = [None, None, None]

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

        return ((b1 == b2) and (b2 == b3))


def random_polygon(center, radius, num_vertices):
    angle_step = 2 * pi / num_vertices
    vertices = []
    for i in range(num_vertices):
        angle = angle_step * i + random.uniform(-angle_step / 4, angle_step / 4)
        r = radius * random.uniform(0.7, 1.0)
        x = center[0] + r * cos(angle)
        y = center[1] + r * sin(angle)
        vertices.append((x, y))
    return vertices


def triangulate_with_holes(bounding_polygon, holes):
    points = bounding_polygon
    segments = [(i, (i + 1) % len(points)) for i in range(len(points))]

    for hole in holes:
        hole_start_index = len(points)
        points.extend(hole)
        segments.extend([(hole_start_index + i, hole_start_index + (i + 1) % len(hole)) for i in range(len(hole))])

    input_data = {
        'vertices': np.array(points),
        'segments': np.array(segments),
        'holes': np.array([np.mean(hole, axis=0) for hole in holes])
    }

    triangulated_data = tr.triangulate(input_data, 'p')

    triangles = []
    for tri_indices in triangulated_data['triangles']:
        vertices = [tuple(triangulated_data['vertices'][i]) for i in tri_indices]
        triangles.append(Triangle(vertices))

    return triangles, holes


def generate_random_level_with_holes(num_holes):
    bounding_polygon = [(50, 50), (WIDTH - 50, 50), (WIDTH - 50, HEIGHT - 50), (50, HEIGHT - 50)]
    holes = []

    for _ in range(num_holes):
        center = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))
        radius = random.randint(30, 100)
        num_vertices = random.randint(3, 8)
        hole = random_polygon(center, radius, num_vertices)
        holes.append(hole)

    triangles, holes = triangulate_with_holes(bounding_polygon, holes)
    return triangles, holes


def d_TEA(triangle, point, visibility_range, visited_triangles):
    visible_triangles = []

    def expand(triangle):
        if triangle in visited_triangles:
            return
        visited_triangles.add(triangle)
        visible_triangles.append(triangle)

        for i, edge in enumerate(triangle.edges):
            neighbor = triangle.neighbors[i]
            if not neighbor:
                continue
            edge_midpoint = ((edge[0][0] + edge[1][0]) / 2, (edge[0][1] + edge[1][1]) / 2)
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
    pygame.display.set_caption('Random d-TEA Visualization with Holes')

    clock = pygame.time.Clock()
    level, holes = generate_random_level_with_holes(5)
    assign_neighbors(level)

    visibility_range = 200
    query_point = (300, 300)
    current_triangle = None

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
        for triangle in level:
            if triangle.contains_point(query_point):
                current_triangle = triangle
                break

        # Draw the level (all triangles)
        for triangle in level:
            triangle.draw(screen, BLACK)

        # Draw the visible triangles in blue
        if current_triangle:
            visited_triangles = set()
            visible_triangles = d_TEA(current_triangle, query_point, visibility_range, visited_triangles)
            for triangle in visible_triangles:
                triangle.draw(screen, BLUE, fill=True)

        # Draw the triangle containing the query point in green
        if current_triangle:
            current_triangle.draw(screen, GREEN, fill=True)

        # Draw the holes (blocking polygons) last to prevent them from affecting the colors of triangles
        for hole in holes:
            pygame.draw.polygon(screen, ORANGE, hole)

        # Draw the query point
        pygame.draw.circle(screen, RED, query_point, 5)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

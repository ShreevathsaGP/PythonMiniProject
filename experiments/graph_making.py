import json
import time
import math
import pygame
import random
from collections import deque

dims = (800, 500)
FPS = 60
no_nodes = 1000
node_radius = 3
min_distance_nodes = 2.5 * node_radius
min_edges = 3

# drawing
node_colour = pygame.Color(230, 230, 230)
line_colour = pygame.Color(100, 50, 50)
line_width = 2

pygame.init()
window = pygame.display.set_mode(dims)
pygame.display.set_caption("Random Graph")
clock = pygame.time.Clock()

def generate_nodes(no_nodes, node_radius, min_distance_nodes):
    nodes = []

    generated = 0
    while generated < no_nodes:
        x = random.randint(node_radius, dims[0] - node_radius)
        y = random.randint(node_radius, dims[1] - node_radius)

        flag = False

        # check if node doesnt impede others
        for x1, y1 in nodes:
            distance = math.sqrt(((x - x1) ** 2) + ((y - y1) ** 2))
            if distance < min_distance_nodes:
                flag = True
                break

        if flag:
            continue

        nodes.append((x,y))
        generated += 1
        print("nodes created: ({} / {})".format(generated, no_nodes))

    return nodes

def generate_edges(nodes, min_edges, no_nodes):
    graph = [[] for _ in range(no_nodes)] # adjacency list for graph

    edges = []
    for i, node in enumerate(nodes):
        x, y = node
        # gives the closest nodes to the current node
        sorted_nodes = [a[0] for a in sorted(enumerate(nodes), key = lambda b: math.sqrt( ((b[1][0] - x) ** 2) + ((b[1][1] - y) ** 2) ))]

        j = 1

        edges_needed = min_edges - len(graph[i])

        while edges_needed > 0:
            if sorted_nodes[j] not in graph[i]:
                edge = tuple(sorted((i, sorted_nodes[j])))
                if edge not in edges:
                    edges.append(edge)

                # add to adjacency list
                graph[i].append(sorted_nodes[j])
                graph[sorted_nodes[j]].append(j)
                edges_needed -= 1

            j += 1

        print("nodes processed for edges: ({} / {})".format(i, no_nodes))

    return edges

def tick():
    fps = clock.tick(FPS) / 1000.0 # convert ot ms

if __name__ == "__main__":
    # game loop
    running = True

    nodes = generate_nodes(no_nodes, node_radius, min_distance_nodes)
    edges = generate_edges(nodes, min_edges, no_nodes)

    previous_time = 0

    while running:
        tick()

        # calculate fps
        # current_time = time.time()
        # print("fps:", round(1 / (current_time - previous_time), 2))
        # previous_time = current_time
        print("fps:", str(round(clock.get_fps(), 2)).ljust(5, str(0)))

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # render edges
        for a, b in edges:
            p1 = nodes[a]
            p2 = nodes[b]

            pygame.draw.line(window, line_colour, p1, p2, line_width)

        # render nodes
        for node in nodes:
            pygame.draw.circle(window, node_colour, node, node_radius)

        pygame.display.update()

    # clean up
    pygame.quit()


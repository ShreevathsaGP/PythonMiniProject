# graph_tools.py

# imports
import os
import math
import time
import json
import pickle
import random
import pygame
from collections import deque

# globals
from ui import UI
from globy import *

# pygame gui
import pygame_gui
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIImage
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton
from pygame_gui.elements import UITextBox
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.windows import UIMessageWindow
from pygame_gui.elements import UISelectionList
from pygame_gui.elements import UITextEntryLine
from pygame_gui import UIManager, PackageResource
from pygame_gui.elements import UIHorizontalSlider
from pygame_gui.elements import UIScreenSpaceHealthBar

# visual graph (number of rows)
class VG:
    def __init__(self, no_rows, node_percentage = Options.node_percentage):
        self.size = 0
        self.node_percentage = node_percentage

        # visual structures
        self.vertices = {}
        self.edges = []

        no_cols = math.ceil(no_rows * Options.graph_col_factor)

        self.no_rows = no_rows
        self.no_cols = no_cols

        # calculate radius
        vbr = Options.vertex_buffer_percentage 
        r_height = (Options.main_height - 2 * Options.graph_buffer) / ((2 + vbr) * no_rows - vbr)
        r_width = (Options.main_width - 2 * Options.graph_buffer) / ((2 + vbr) * no_cols - vbr)
        self.radius = min(r_height, r_width)

        if r_width < r_height:
            self.vertex_buffer_x = vbr * self.radius
            self.vertex_buffer_y = (Options.main_height - 2 * Options.graph_buffer - 2 * no_rows * self.radius) / (no_rows - 1)
        else:
            self.vertex_buffer_x = (Options.main_width - 2 * Options.graph_buffer - 2 * no_cols * self.radius) / (no_cols - 1)
            self.vertex_buffer_y = vbr * self.radius

        # calculate vertex buffer
        self.vertex_buffer = vbr * self.radius

        self.draw_array = [[0 for i in range(no_cols)] for j in range(no_rows)]

        for col in range(no_cols):
            no_vertices = random.randint(1, math.ceil(self.node_percentage * no_cols))
            c = [-1 for k in range(no_vertices)] + [0 for j in range(no_rows - no_vertices)]

            random.shuffle(c)
            # print(c)

            if self.node_percentage != 1:
                # print("vertical filter")
                # print(c)
                for y in range(no_rows - 1):
                    if c[y] == c[y + 1] == -1:
                        c[y + 1] = 0
                # print(c)
            
            # copy over the colummn
            for row in range(no_rows):
                self.draw_array[row][col] = c[row]

        if self.node_percentage != 1:
            # print("horizontal filter")
            for i in range(no_rows):
                for j in range(no_cols - 2):
                    if self.draw_array[i][j] == self.draw_array[i][j + 1] == -1:
                        self.draw_array[i][j + 1] = 0

        # number the vertices
        vertex = 1
        for j in range(no_cols):
            for i in range(no_rows):
                if self.draw_array[i][j] == -1:
                    self.draw_array[i][j] = vertex 
                    self.vertices[vertex] = (i, j)
                    vertex += 1
                    self.size += 1
        
        # show draw array
        for row in self.draw_array:
            # print(row)
            pass

        # make empty adjacency list
        self.adjacency_list = [[False for j in range(self.size)] for i in range(self.size)]

        # graph is NOT 0 INDEXED, IT IS 1 INDEXED
    
    def __len__(self):
        return self.size

    def __str__(self):
        return_string = ""
        return_string += f"VisualGraph(size = {self.size},\n"
        for i in range(self.size):
            return_string += "  [ "
            for j in range(self.size):
                return_string += str(int(self.adjacency_list[i][j]))
                return_string += ' '
            return_string += "]\n"
        return_string += ")\n"

        return return_string

    def __repr__(self):
        return str(self)

    def delete_random(self, regular_prob, boring_prob):
        for i, j in self.edges:
            c1 = self.get_vertex_center(i)
            c2 = self.get_vertex_center(j)

            if c1[0] == c2[0] or c1[1] == c2[1]:
                if random.random() < boring_prob:
                    self.set_edge(i, j, False)

                continue

            if random.random() < regular_prob:
                self.set_edge(i, j, False)

        self.update_edges()

    def get_radius(self):
        return self.radius

    def get_vertex_center(self, vertex):
        i, j = self.get_vertex_pos(vertex)

        x = Options.main_x + Options.graph_buffer + j * (2 * self.radius + self.vertex_buffer_x) + self.radius

        if Options.graph_do_offset:
            if j % 2 == 0:
                y = (Options.graph_offset * Options.graph_buffer) + (i * (2 * self.radius + self.vertex_buffer_y)) + self.radius
            else:
                y = ((2 - Options.graph_offset) * Options.graph_buffer) + (i * (2 * self.radius + self.vertex_buffer_y)) + self.radius
        else:
            y = Options.graph_buffer + (i * (2 * self.radius + self.vertex_buffer_y)) + self.radius

        return (x, y)

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def get_vertex_pos(self, i):
        return self.vertices[i]

    def connect_all(self):
        self.adjacency_list = [[True for j in range(self.size)] for i in range(self.size)]

    def get_edge(self, i, j):
        return self.adjacency_list[i - 1][j - 1]

    def set_edge(self, i, j, val):
        self.adjacency_list[i - 1][j - 1] = val

    def update_edges(self):
        # make edges list
        self.edges.clear()
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.get_edge(i, j):
                    self.edges.append((i, j))

# check if line(p1, p2) & circle(center, radius) overlap
def check_overlap(p1, p2, center, radius):
    # circle values: (x - h)^2 + (y - k)^2 = r^2
    h = center[0]
    k = center[1]
    r = radius

    # m = infinite
    if p1[0] == p2[0]:
        higher_y = min(p1[1], p2[1])
        lower_y = max(p1[1], p2[1])

        return ((h - r) <= p1[0] <= (h + r)) and (higher_y <= k <= lower_y)

    # m = 0
    if p1[1] == p2[1]:
        higher_x = max(p1[0], p2[0])
        lower_x = min(p1[0], p2[0])

        return ((k - r) <= p1[1] <= (k + r)) and (lower_x <= h <= higher_x)

    # circle mask
    circle_surface = pygame.Surface((2 * r, 2 * r))
    pygame.draw.circle(circle_surface, pygame.Color(255, 255, 255), (r, r), r)
    circle_mask = pygame.mask.from_surface(circle_surface)

    # make relative
    # print(p1, p2)
    min_x = min(p1[0], p2[0])
    min_y = min(p1[1], p2[1])
    p1 = [p1[0] - min_x, p1[1] - min_y]
    p2 = [p2[0] - min_x, p2[1] - min_y]
    # print(p1, p2)

    # line mark
    line_surface = pygame.Surface((abs(p2[0] - p1[0]), abs(p2[1] - p1[1])))
    pygame.draw.line(line_surface, pygame.Color(255, 255, 255), p1, p2)
    line_mask = pygame.mask.from_surface(line_surface)

    # offset
    cm_pos = (h - r, k - r)
    lm_pos = (min_x, min_y)
    offset = (lm_pos[0] - cm_pos[0], lm_pos[1] - cm_pos[1])

    # mask overlap
    return (circle_mask.overlap(line_mask, offset) != None)

# make non-overlapping graphs of different sizes
if __name__ == "__main__":
    # initialize pygame
    pygame.init()
    pygame.display.set_mode(Options.resolution)


    file_name = "stored_graphs.pickle"
    store = {}

    lower = Options.slider_range[0]
    higher = Options.slider_range[1] + 1
    
    for size in range(lower, higher):
        graph = VG(size)
        print(f"size {size}:")

        edges_done = 0
        total_possible_edges = (len(graph) - 1) * (len(graph)) // 2
        update_string = "\tfiltered edge ({} / {}): {}"

        for i in range(1, len(graph) + 1):
            for j in range(1 + i, len(graph) + 1):
                p1 = graph.get_vertex_center(i)
                p2 = graph.get_vertex_center(j)

                graph.set_edge(i, j, True)
                for k in range(1, len(graph) + 1):
                    if k == i or k == j:
                        continue

                    center = graph.get_vertex_center(k)

                    if check_overlap(p1, p2, center, graph.radius):
                        graph.set_edge(i, j, False)
                        break

                edges_done += 1
                print(update_string.format(edges_done, total_possible_edges, graph.get_edge(i, j)))
        
        graph.update_edges()
        store[size] = graph
    
    with open(file_name, "wb") as f:
        # pickle.dump(store, f)
        pickle.dump(store, f, protocol = pickle.HIGHEST_PROTOCOL)


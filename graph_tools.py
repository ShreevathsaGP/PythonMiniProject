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


class VG:
    def __init__(self, no_vertices):
        # graph is 1-indexed not 0-indexed
        self.size = no_vertices

        self.radius = math.ceil(Options.resolution[1] * Options.radius_height_ratio)
        self.min_distance = 2.5 * self.radius
        self.min_edges = 3

        # visual structures
        self.vertices = []
        self.edges = []
        self.adjacency_list = [[] for _ in range(len(self))]

        # generate graph
        self.generate_vertices()
        self.generate_edges()

        # get start and stop vertices
        self.sorted_indices = [v[0] for v in sorted(enumerate(self.vertices), key = lambda b: math.sqrt(((b[1][0] - Options.main_x) ** 2) + ((b[1][1] - 0) ** 2)))]
        self.start_vertex = self.sorted_indices[0] + 1
        self.end_vertex = self.sorted_indices[-1] + 1

    def __len__(self):
        return self.size

    def __str__(self):
        return_string = ""
        return_string += f"VisualGraph(size = {self.size})"
        # for i in range(self.size):
        #     return_string += "  [ "
        #     adjacent = self.get_adjacent(j)
        #     for j in range(s):
        #         return_string += str(int(self.adjacency_list[i][j]))
        #         return_string += ' '
        #     return_string += "]\n"
        # return_string += ")\n"

        return return_string

    def __repr__(self):
        return str(self)

    def get_radius(self):
        return self.radius

    def get_vertex_center(self, i):
        return self.vertices[i - 1]

    def set_vertex_center(self, i, value):
        self.vertices[i - 1] = value

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def get_adjacent(self, v):
        return self.adjacency_list[v - 1]

    def add_adjacent(self, v, a):
        self.adjacency_list[v - 1].append(a)

    def generate_vertices(self):
        self.vertices = []

        generated = 0
        while generated < len(self):
            x = Options.main_x + Options.graph_buffer + random.randint(self.radius, int(Options.main_width) - self.radius - (2 * Options.graph_buffer))
            y = Options.graph_buffer + random.randint(self.radius, Options.main_height - self.radius - (2 * Options.graph_buffer))

            overlap = False
            
            for x1, y1 in self.vertices:
                distance = math.sqrt(((x - x1) ** 2) + ((y - y1) ** 2))
                if distance < self.min_distance:
                    overlap = True
                    break

            if overlap:
                continue

            generated += 1
            self.vertices.append((x,y))
            print("\tnodes created: ({} / {})".format(generated, len(self)))

    def generate_edges(self):
        self.edges = []

        for z, vertex in enumerate(self.vertices):
            i = z + 1 # graph is 1-indexed
            x, y = vertex

            # a[0] + 1 cause graph is 1-indexed
            sorted_vertices = [a[0] + 1 for a in sorted(enumerate(self.vertices), key = lambda b: math.sqrt(((b[1][0] - x) ** 2) + ((b[1][1] - y) ** 2)))]

            j = 1 # 1 because 0 is the vertex i itself
            
            edges_needed = self.min_edges - len(self.get_adjacent(i))

            while edges_needed > 0:
                if sorted_vertices[j] not in self.get_adjacent(i):
                    edge = tuple(sorted((i, sorted_vertices[j]))) 
                    if edge not in self.edges:
                        self.edges.append(edge)
                    
                    # add to to adjacency list
                    self.add_adjacent(i, sorted_vertices[j])
                    self.add_adjacent(sorted_vertices[j], i)
                    edges_needed -= 1

                j += 1

            print("\tnodes processed for edges: ({} / {})".format(i, len(self)))

if __name__ == "__main__":
    save_file = "storage/stored_graphs.pickle"

    s = {}
    for size in range(Options.slider_range[0], Options.slider_range[1] + 1):
        print("size ({size} / {Options.slider_range[1]})")
        s[size] = VG(size * 100)

    with open(save_file, "wb") as f:
        pickle.dump(s, f, protocol = pickle.HIGHEST_PROTOCOL)


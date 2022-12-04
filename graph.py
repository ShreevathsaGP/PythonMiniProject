# graph.py

# imports
import os
import math
import time
import json
import pickle
import random
import pygame
from collections import deque
import copy

# globals
from ui import UI
from globy import *

# graph tools
from graph_tools import *

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

class GraphSearch:
    def __init__(self, ui, s = Options.slider_default):
        self.ui = ui
        self.size = s

        self.stored_graphs = None
        with open(Options.graph_storage_file, "rb") as f:
            self.stored_graphs = pickle.load(f)

        self.running = True
        self.delay = 0

        # drawing
        self.radius = 0
        self.draw_array = []
        
        # for drawing
        self.current_vertices = {}
        self.current_edges = {}

        self.set_size(s)

        # bfs
        self.parents = {}

    def set_size(self, s):
        self.size = s
        self.reset()
    
    def reset_vertices(self):
        for vertex in self.current_vertices:
            self.current_vertices[vertex] = 0

        self.current_vertices[self.graph.start_vertex] = 1
        self.current_vertices[self.graph.end_vertex] = 2

    def reset_edges(self):
        self.current_edges = {e: 0 for e in self.graph.get_edges()}

    def reset_colours(self):
        self.reset_vertices()
        self.reset_edges()

    def reset(self):
        self.graph = self.stored_graphs[self.size]

        self.current_vertices = {vertex: 0 for vertex in range(len(self.graph))}
        self.current_edges = {e: 0 for e in self.graph.get_edges()}

        self.current_vertices[self.graph.start_vertex] = 1
        self.current_vertices[self.graph.end_vertex] = 2

    def render(self):
        # print edges
        for edge in self.current_edges:
            colour = Options.edge_c_map[self.current_edges[edge]]

            i, j = edge
            p1 = self.graph.get_vertex_center(i)
            p2 = self.graph.get_vertex_center(j)
            pygame.draw.line(self.ui.get_window(), colour, p1, p2)

        # print vertices
        for vertex in self.current_vertices:
            colour = Options.vertex_c_map[self.current_vertices[vertex]]
            pygame.draw.circle(self.ui.get_window(), colour,
                    self.graph.get_vertex_center(vertex), self.graph.get_radius())

        pygame.display.update()
        if self.delay != 0: pygame.time.delay(self.delay)

    def process_slider(self, x):
        new_size = x

        if self.size != new_size:
            self.set_size(new_size)

    def process_button(self, state):
        if state == True:
            self.ui.disable()
            self.ui.disable_extras()
            self.start = True

    def process_compute(self, state):
        # if state == True:
        #     self.ui.enable_start()
        #     self.reset_vertices()
        #     self.current_vertices[self.from_vertex] = 1
        #     self.current_vertices[self.to_vertex] = 2
        pass

    def process_inputs(self, input_1, input_2):
        # if input_1.strip() == "" or input_2.strip() == "":
        #     self.ui.disable_compute()
        #     self.ui.disable_start()
        #     # print(1)
        #     return

        # a = int(input_1)
        # b = int(input_2)
        
        # if a == b:
        #     self.ui.disable_compute()
        #     self.ui.disable_start()
        #     # print(2)
        #     return

        # if a not in self.current_vertices or b not in self.current_vertices:
        #     self.ui.disable_compute()
        #     self.ui.disable_start()
        #     # print(3)
        #     return

        # if a != self.from_vertex or b != self.to_vertex:
        #     self.ui.disable_start()
        #     # print(4)
        
        # self.from_vertex = a
        # self.to_vertex = b
        # self.ui.enable_compute()
        pass

    def update(self):
        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()

            self.ui.manager.process_events(event)

        # process ui events
        self.process_slider(self.ui.get_slider_value())
        self.process_inputs(self.ui.get_input_1(), self.ui.get_input_2())
        self.process_button(self.ui.button_pressed())
        self.process_compute(self.ui.compute_pressed())

        # update-render
        self.ui.update()
        self.ui.render()

    def update_render(self):
        self.update()
        self.render()

    def bfs(self):
        self.parents = {self.graph.start_vertex: None}
        visited = {self.graph.start_vertex}
        queue = [self.graph.start_vertex]

        while len(queue) > 0:
            vertex = queue.pop(0)

            # visualize
            self.current_vertices[vertex] = 3
            self.update_render()

            for adjacent in self.graph.get_adjacent(vertex):
                if adjacent not in visited:
                    visited.add(adjacent)

                    # visualize
                    self.current_vertices[adjacent] = 4
                    self.current_edges[(vertex, adjacent)] = 1
                    self.update_render()

                    self.parents[adjacent] = vertex
                    queue.append(adjacent)

            if vertex == self.graph.start_vertex:
                self.current_vertices[vertex] = 1
            elif vertex == self.graph.end_vertex:
                self.current_vertices[vertex] = 2
                break
            else:
                self.current_vertices[vertex] = 5
            self.update_render()

        # show shortest path
        current_vertex = self.graph.end_vertex

        while current_vertex != None and current_vertex != self.graph.start_vertex:
            # visualize
            edge = tuple(sorted((current_vertex, self.parents[current_vertex])))
            self.current_edges[(self.parents[current_vertex], current_vertex)] = 2

            if current_vertex != self.graph.end_vertex:
                self.current_vertices[current_vertex] = 6

            self.update_render()

            current_vertex = self.parents[current_vertex]

    def dfs(self):
        visited = {self.graph.start_vertex}
        stack = [self.graph.start_vertex]
        self.parents = {self.graph.start_vertex: None}

        while len(stack) > 0:
            # visualize
            vertex = stack.pop() # pop -1
            visited.add(vertex)

            self.current_vertices[vertex] = 3
            self.update_render()

            for adjacent in reversed(self.graph.get_adjacent(vertex)):
                if adjacent not in visited:

                    # visualize
                    self.current_vertices[adjacent] = 4
                    self.current_edges[(vertex, adjacent)] = 1
                    self.update_render()

                    self.parents[adjacent] = vertex
                    stack.append(adjacent)

            # visualize
            if vertex == self.graph.start_vertex:
                self.current_vertices[vertex] = 1
            elif vertex == self.graph.end_vertex:
                self.current_vertices[vertex] = 2
                break
            else:
                self.current_vertices[vertex] = 5
            self.update_render()


        # show found path
        current_vertex = self.graph.end_vertex

        while current_vertex != None and current_vertex != self.graph.start_vertex:
            # visualize
            edge = tuple(sorted((current_vertex, self.parents[current_vertex])))
            self.current_edges[(self.parents[current_vertex], current_vertex)] = 2

            if current_vertex != self.graph.end_vertex:
                self.current_vertices[current_vertex] = 6

            self.update_render()

            current_vertex = self.parents[current_vertex]

        # https://www.baeldung.com/cs/dfs-vs-bfs-vs-dijkstra#tracing-the-path-in-iterative-depth-first-search


    def run(self) -> bool:
        self.running = True
        self.start = False
        self.ui.disable_extras()

        while self.running and self.ui.get_dropdown_topic() == Options.topics[1]:
            self.update()

            # visualize
            if not self.start:
                self.render()
            else:
                if self.ui.get_dropdown_algo() == Options.graph_options[0]:
                    self.reset_colours()
                    # self.delay = int((Options.frame_rate // Options.graph_fps_delay_ratio) * (1))

                    self.dfs()

                elif self.ui.get_dropdown_algo() == Options.graph_options[1]:
                    self.reset_colours()
                    # self.delay = int((Options.frame_rate // Options.graph_fps_delay_ratio) * (1))

                    self.bfs()

                self.delay = 0

                # restart ui
                self.ui.enable()
                self.start = False
                self.running = True

        return self.running

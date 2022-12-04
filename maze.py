# maze.py

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

# maze tools
from maze_tools import *

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

class MazeSolve:
    def __init__(self, ui, s = 20):
        self.ui = ui
        self.size = s
        self.set_size(s)

        self.delay = 0
        self.running = True
        self.x_buffer = self.y_buffer = Options.maze_buffer

    def set_size(self, s):
        self.size = s
        self.reset()

    def reset(self):
        n = self.size
        w = math.floor(Options.main_width  / self.size) - 1
        h = math.floor(Options.main_height / self.size) - 1

        self.maze = Maze(n, w, h)

        self.x_buffer = (Options.main_width - self.maze.draw_width) / 2
        self.y_buffer = (Options.main_height - self.maze.draw_height) / 2

    def process_slider(self, x):
        x = 5 + (Options.slider_range[1] - x)
        new_size = math.ceil(x * 2.25)

        if self.size != new_size:
            self.set_size(new_size)

    def process_button(self, state):
        if state == True:
            self.ui.disable()
            self.start = True

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
        self.process_button(self.ui.button_pressed())

        # update-render
        self.ui.update()
        self.ui.render()

    def generate_maze(self):
        self.edges = []

        # horizontal edges
        for i in range(self.maze.height):
            for j in range(self.maze.width - 1):
                current = (self.maze.width * i) + j
                right = current + 1

                self.edges.append((current, right))

        # vertical edges
        for i in range(self.maze.height - 1):
            for j in range(self.maze.width):
                current = (self.maze.width * i) + j
                down = current + self.maze.width

                self.edges.append((current, down))

        # shuffle edges
        random.shuffle(self.edges)
        
        # kruskals mst
        mst_length = len(self.maze) - 1
        no_edges = 0
        while no_edges < mst_length:
            x, y = self.edges.pop()

            if not self.maze.are_connected(x, y):
                self.maze.connect_nodes(x, y)
                no_edges += 1

            self.update_render()

    def update_render(self):
        self.update()
        self.render()

    def render(self):
        self.ui.get_window().blit(self.maze.get_surface(), (Options.main_x + self.x_buffer, self.y_buffer))

        pygame.display.update()
        if self.delay != 0: pygame.time.delay(self.delay)

    def run(self) -> bool:
        self.running = True
        self.start = False
        self.ui.disable_extras()

        while self.running and self.ui.get_dropdown_topic() == Options.topics[2]:
            self.update()

            # visualize
            if not self.start:
                self.render()
            else:
                # self.delay = int((Options.frame_rate // Options.maze_fps_delay_ratio) * (1))
                # self.delay = 10000
                self.generate_maze()

                self.delay = 0

                # restart ui
                self.ui.enable()
                self.start = False
                self.running = True # cannot close the program

        return self.running


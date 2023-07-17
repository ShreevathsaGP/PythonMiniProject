# maze_tools.py

# imports
import os
import math
import time
import json
import copy
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

def make_string_array(array):
    string_array = [str(x) for x in array]
    return string_array

def array_to_string(array):
    return ''.join(make_string_array(array))

def bin_to_string(x: bin):
    return str(x)[2:].rjust(4, '0')

def get_opposite_direction(d):
    if d == 0:
        return 1

    if d == 1:
        return 0

    if d == 2:
        return 3

    if d == 3:
        return 2

class Node:
    def __init__(self, v, t = 0):
        self.value = v
        self.type = t # ex: 0 = not discovered | 1 = in shortest path etc.
        self.walls = [1, 1, 1, 1] # U D L R => 0: not-present | 1 = present

        self.parent = None
        self.rank = 0

    def __str__(self):
        return f"N({self.value}, [{array_to_string(self.walls)}])"

    def __repr__(self):
        return str(self)

    def set_parent(self, p):
        self.parent = p

    def get_parent(self):
        return self.parent

    def get_root(self):
        if self.parent == None:
            return self

        return self.parent.get_root()

    def get_rank(self):
        return self.get_root().rank

    def is_connected(self, node):
        return self.get_root() == node.get_root()

    def connect(self, node, direction):
        self.walls[direction] = 0
        node.walls[get_opposite_direction(direction)] = 0

        if self.get_rank() < node.get_rank():
            self.get_root().set_parent(node)
        elif self.get_rank() > node.get_rank():
            node.get_root().set_parent(self)
        else:
            node.get_root().set_parent(self)
            self.get_root().rank += 1

        # print(node, node.get_root())

class Maze:
    def __init__(self, n, w, h):
        # h => rows
        # w => cols
        # array[row][col]

        # directions => 0 = U | 1 = D | 2 = L | 3 = R

        self.node_size = n
        self.width = w
        self.height = h
        self.array = [[Node((j * self.width) + i) for i in range(w)] for j in range(h)]

        self.draw_width = w * n
        self.draw_height = h * n

        self.background = pygame.Surface((self.draw_width + Options.maze_thick, self.draw_height + Options.maze_thick))
        self.background.fill(Options.maze_bg_colour)

        # initial background
        for i in range(self.height + 1):
            pygame.draw.line(self.background, Options.maze_colour,
                    (0, i * self.node_size), (self.draw_width, i * self.node_size), Options.maze_thick)

        for j in range(self.width + 1):
            pygame.draw.line(self.background, Options.maze_colour,
                    (j * self.node_size, 0), (j * self.node_size, self.draw_height), Options.maze_thick)

        # [U D L R] => [U L]
        self.draw_dict = {(0, 0): pygame.Surface((self.node_size, self.node_size)), 
                (0, 1): pygame.Surface((self.node_size, self.node_size)),
                (1, 0): pygame.Surface((self.node_size, self.node_size)),
                (1, 1): pygame.Surface((self.node_size, self.node_size)),
                }

        # (0, 0)
        current = (0,0)
        base_rect = pygame.Rect(0, 0, Options.maze_thick, Options.maze_thick)
        pygame.draw.rect(self.draw_dict[current], Options.maze_colour, base_rect)

        # (0, 1)
        current = (0,1)
        pygame.draw.line(self.draw_dict[current], Options.maze_colour, (0,0), (0, self.node_size), Options.maze_thick)

        # (1, 0)
        current = (1, 0)
        pygame.draw.line(self.draw_dict[current], Options.maze_colour, (0,0), (self.node_size, 0), Options.maze_thick)

        # (1, 1)
        current = (1, 1)
        pygame.draw.line(self.draw_dict[current], Options.maze_colour, (0,0), (self.node_size, 0), Options.maze_thick)
        pygame.draw.line(self.draw_dict[current], Options.maze_colour, (0,0), (0, self.node_size), Options.maze_thick)

    def __len__(self):
        return self.width * self.height

    def __str__(self):
        return_string = ""
        for row in self.array:
            return_string += (str(row) + '\n')

        return return_string[:-1]

    def __repr__(self):
        return str(self)

    # returns row, col
    def get_indices(self, x):
        return x // self.width, x % self.width

    def get_surface(self):
        return self.background

    def are_connected(self, x, y):
        row_x, col_x = self.get_indices(x)
        row_y, col_y = self.get_indices(y)

        return self.array[row_x][col_x].is_connected(self.array[row_y][col_y])

    def connect_nodes(self, x, y):
        row_x, col_x = self.get_indices(x)
        row_y, col_y = self.get_indices(y)

        if col_x == col_y:
            direction = 0 if (row_y < row_x) else 1 # vertical
        elif row_x == row_y:
            direction = 2 if (col_y < col_x) else 3 # horizontal

        self.array[row_x][col_x].connect(self.array[row_y][col_y], direction)

        w1 = tuple(self.array[row_x][col_x].walls[0::2]) # [U D L R] => [U L]
        w2 = tuple(self.array[row_y][col_y].walls[0::2]) # [U D L R] => [U L]

        self.background.blit(self.draw_dict[w1], (col_x * self.node_size, row_x * self.node_size))
        self.background.blit(self.draw_dict[w2], (col_y * self.node_size, row_y * self.node_size))

    def redo_background(self):
        for row in range(self.height):
            for col in range(self.width):
                w = tuple(self.array[row][col].walls[0::2]) # [U D L R] => [U L]

                self.background.blit(self.draw_dict[w], (col * self.node_size, row * self.node_size))

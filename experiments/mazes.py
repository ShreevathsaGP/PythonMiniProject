# imports
import os
import json
import math
import time
import pickle
import pygame
import random

node_size = 15
line_thickness = 1

maze_height = 30
maze_width = 30

# pygame 
buff = 0
width = (maze_width * node_size) + buff
height = (maze_height * node_size) + buff

node_type = {}

def make_string_array(array):
    string_array = [str(x) for x in array]
    return string_array

def array_to_string(array):
    return ''.join(make_string_array(array))

def bin_to_string(x: bin):
    return str(x)[2:].rjust(4, '0')

class Node:
    def __init__(self, t = 0):
        self.type = t
        self.walls = [1, 1, 1, 1] # U D L R => 0: not-present | 1 = present
        self.parent = None

    def __str__(self):
        return f"Node({self.type}, [{array_to_string(self.walls)}])"

    def __repr__(self):
        return str(self)

    def set_parent(self, p):
        self.parent = p

    def get_parent(self):
        return self.parent

    def get_root(self):
        return self.parent.get_root() if self.parent != None else self

    def connect(self, tree):
        tree.get_root().set_parent(self)

class Maze:
    def __init__(self, w, h):
        # h => rows
        # w => cols
        # array[row][col]
        self.width = w
        self.height = h
        self.array = [[Node() for i in range(w)] for j in range(h)]

    def __str__(self):
        return_string = ""
        for row in self.array:
            return_string += (str(row) + '\n')

        return return_string[:-1]

    def __repr__(self):
        return str(self)

def render_maze(background, maze):
    for r in range(maze.height):
        for c in range(maze.width):
            if not all(maze.array[r][c].walls):
                w = node_size
                h = node_size
                line_colour = pygame.Color(200, 200, 200)
                new_surface = pygame.Surface((w, h))
                

                base_rect = pygame.Rect(0, 0, line_thickness, line_thickness)
                pygame.draw.rect(new_surface, line_colour, base_rect)

                rect = pygame.Rect(line_thickness, line_thickness, w, h)
                pygame.draw.rect(new_surface, pygame.Color(90, 90, 90), rect)

                # pygame.draw.line(new_surface, line_colour, (0,0), (node_size, 0), line_thickness)
                # pygame.draw.line(new_surface, line_colour, (0,0), (0, node_size), line_thickness)

                background.blit(new_surface, ((c + 1) * node_size, (r + 1) * node_size))

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Maze Generation")
    window = pygame.display.set_mode((width, height))
    background = pygame.Surface((width, height))
    background.fill(pygame.Color(20, 20, 20))
    clock = pygame.time.Clock()

    # draw background
    for i in range(height - 1):
        pygame.draw.line(background, pygame.Color(200, 200, 200), 
                (node_size, (i + 1) * node_size), 
                (width - node_size, (i + 1) * node_size),
                line_thickness)

    for j in range(width - 1):
        pygame.draw.line(background, pygame.Color(200, 200, 200),
                ((j + 1) * node_size, node_size),
                ((j + 1) * node_size, height - node_size),
                line_thickness)

    maze = Maze(maze_width, maze_height)
    maze.array[4][3].walls = [1,1,1,0]

    running = True

    while running:
        clock.tick(60)

        # update
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

        window.blit(background, (0,0))

        # render
        render_maze(background, maze)

        pygame.display.update()

    print(maze)

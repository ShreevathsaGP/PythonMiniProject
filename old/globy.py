# imports
import os
import sys
import random
import pygame

# global options
class Options:
    # resolution
    res_factor = 600 # ie. height
    # res_factor = 900 # when on monitor
    res_ratio = 1.9 # length / width
    resolution = (round(res_factor * res_ratio), res_factor) # width x height

    # frame rate
    frame_rate = 60

    # colours
    background_colour = (11, 11, 11)
    background_colour = (1, 1, 1)
    line_colour = (163, 163, 163)
    line_width = 2

    # menu ui
    menu_ratio = 0.18
    menu_width = menu_ratio * resolution[0]
    menu_height = resolution[1]
    menu_x_buffer = 0.05
    menu_y_buffer = 0.5
    ui_height = 0.06
    slider_height = 0.9

    # topics
    available_topics = ["Sorting", "Graph Search", "Maze Solving"]
    start_topic = 0

    # drawing area
    main_x = menu_width + line_width
    main_width = resolution[0] - menu_width - line_width
    main_height = resolution[1]
    
    # sorting
    sorting_c_map = {0: pygame.Color((255, 252, 252)), 1: pygame.Color((230, 37, 37)), 2: pygame.Color((41, 227, 146))}
    # sorting c_map => 0: regular | 1: engaged | 2: sorted
    default_sorting_size = 100
    sorting_shuffle = True
    bar_gap = 0.6
    

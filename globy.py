# globy.py

# imports
import os
import sys
import random
import pygame

class Options:
    # resolution
    res_factor = 600 # ie. height
    res_factor = 900 # for monitor
    res_ratio = 1.9 # length / width
    resolution = (round(res_factor * res_ratio), res_factor) # width x height

    # frame rate
    frame_rate = 60

    # execution preferenes
    ui_only_mode = False
    # ui_only_mode = True
    show_fps = False
    show_fps = True

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

    # topic
    topics = ["Sorting", "Graph Search", "Maze Solving"]
    start_topic = 0

    # visualization area
    main_x = menu_width + line_width
    main_width = resolution[0] - menu_width - line_width
    main_height = resolution[1]
    
    # sorting
    sorting_options = ["Merge Sort", "Heap Sort"]
    sorting_c_map = {0: pygame.Color((255, 252, 252)), 1: pygame.Color((230, 37, 37)), 
            2: pygame.Color((41, 227, 146)), 3: pygame.Color((0, 174, 255))}
    # sorting c_map => 0: regular | 1: being compared | 2: being copied into local sorted array | 3: fully sorted
    default_sorting_size = 100
    sorting_shuffle = True
    bar_gap = 0.6
    sorting_fps_delay_ratio = 2.4

    heap_sort_colours = [pygame.Color((235, 183, 52)), pygame.Color((186, 235, 52)), pygame.Color((128, 166, 106)),
            pygame.Color((92, 202, 242)), pygame.Color((14, 143, 230)), pygame.Color((93, 115, 240)), 
            pygame.Color((167, 92, 242)), pygame.Color((219, 121, 188))]
        

    # graph search
    graph_options = ["Depth First", "Breadth First"]

    # maze solve
    maze_options = ["Dijkstra", "A* Search"]

    # algo topics
    option_dict = {"Sorting": sorting_options, "Graph Search": graph_options, "Maze Solving": maze_options}

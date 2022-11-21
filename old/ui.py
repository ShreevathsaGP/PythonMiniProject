# imports
import os
import json
import random
import pygame
from collections import deque

# gloabals
from globy import *
# pygame gui
import pygame_gui
from pygame_gui import UIManager, PackageResource
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton
from pygame_gui.elements import UIHorizontalSlider
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UITextBox
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.elements import UIScreenSpaceHealthBar
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIImage
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UISelectionList
from pygame_gui.windows import UIMessageWindow

# info json
with open("info.json", 'r') as f:
    info = json.load(f)

class UI:
    def __init__(self):
        # setup pygame
        pygame.init()
        pygame.display.set_caption("Algorithm Visualizer")
        self.window_surface = pygame.display.set_mode(Options.resolution)
        self.clock = pygame.time.Clock()

        # static background
        self.background = pygame.Surface(Options.resolution)
        self.background.fill(pygame.Color(*Options.background_colour))

        # setup pygame-gui
        self.ui_manager = UIManager(Options.resolution)
        self.running = True

        # y-axis buffer
        self.menu_y_buffer = Options.menu_x_buffer * Options.menu_width

        # toppic mappings
        self.topics = Options.available_topics
        self.topic_objects = {self.topics[Options.start_topic]: Sorting(), self.topics[1]: GraphSearch(), self.topics[2]: MazeSolve()}
    
        # first dropdown
        self.drop_rect = pygame.Rect(Options.menu_width * Options.menu_x_buffer, self.menu_y_buffer, 
                Options.menu_width * (1 - Options.menu_x_buffer * 2), Options.resolution[1] * Options.ui_height)
        self.algo_dropdown = UIDropDownMenu(self.topics, self.topics[Options.start_topic], self.drop_rect, self.ui_manager)

        # second dropdown
        self.option_rect = pygame.Rect(self.drop_rect.left, 
                self.drop_rect.top + self.drop_rect.height + Options.line_width + (2 * self.menu_y_buffer),
                self.drop_rect.width, self.drop_rect.height)
        options = self.topic_objects[self.topics[Options.start_topic]].get_options()
        self.options = UIDropDownMenu(options, options[0], self.option_rect, self.ui_manager)
        self.base_option = options[0]

        # start stop button
        button_height = Options.resolution[1] * Options.ui_height
        button_width = Options.menu_width - (2 * (Options.menu_x_buffer * Options.menu_width))
        self.button_rect = pygame.Rect(Options.menu_width * Options.menu_x_buffer, 
                Options.menu_height - button_height - self.menu_y_buffer, button_width, button_height)
        self.button = UIButton(self.button_rect, "Start", self.ui_manager)
        
        # universal slider
        slider_height = Options.slider_height * Options.ui_height * Options.menu_height
        slider_width = Options.menu_width - (2 * (Options.menu_x_buffer * Options.menu_width))
        self.slide_rect = pygame.Rect(Options.menu_width * Options.menu_x_buffer, 
                self.button_rect.top - (2 * self.menu_y_buffer )- Options.line_width - slider_height, 
                slider_width, slider_height)
        self.slider = UIHorizontalSlider(self.slide_rect, 15, (5, 25), self.ui_manager)

        # info box (gives information topic & algo specific information) 
        info_width = button_width
        info_height = (self.slide_rect.top - (self.option_rect.top + self.option_rect.height)) - (2 * self.menu_y_buffer)
        self.info_rect = pygame.Rect(self.drop_rect.left, self.option_rect.top + self.option_rect.height + self.menu_y_buffer,
                info_width, info_height)
        self.info_box = UITextBox(info[self.topics[0]][self.base_option], self.info_rect, self.ui_manager)

        # reset the UI
        self.reset_ui()

    def reset_topics(self):
        # reset the options dropdown (it is topic specific)
        new_topic = self.algo_dropdown.selected_option
        self.options.kill()
        options = self.topic_objects[new_topic].get_options()
        self.options = UIDropDownMenu(options, options[0], self.option_rect, self.ui_manager)

        self.options.rebuild()

    def reset_info(self):
        new_text = info[self.algo_dropdown.selected_option][self.options.selected_option]
        self.info_box.kill()
        self.info_box = UITextBox(new_text, self.info_rect, self.ui_manager)

    def process_events(self):
        # process the universal slider value
        self.topic_objects[self.algo_dropdown.selected_option].process_slider(self.slider.get_current_value())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui_manager.process_events(event)

    def reset_ui(self):
        pygame.draw.line(self.background, Options.line_colour, (Options.menu_width, 0), 
                (Options.menu_width, Options.resolution[1]), Options.line_width)

        y = self.drop_rect.top + self.drop_rect.height + self.menu_y_buffer
        pygame.draw.line(self.background, Options.line_colour, (0, y), (Options.menu_width, y), Options.line_width)
        y = self.button_rect.top - self.menu_y_buffer - Options.line_width
        pygame.draw.line(self.background, Options.line_colour, (0, y), (Options.menu_width, y), Options.line_width)

    def update(self, dt):
        self.ui_manager.update(d1)



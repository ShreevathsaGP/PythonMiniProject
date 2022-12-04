# ui.py

# imports
import os
import math
import json
import pickle
import random
import pygame
from collections import deque

# globals
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

class UI:
    def __init__(self):
        # info json
        with open("info.json", 'r') as f:
            self.info = json.load(f)

        # initialize pygame

        # 4: UserWarning: Finding font with id: fira_code_italic_14 that is not already loaded.
        # Preload this font with {'name': 'fira_code', 'point_size': 14, 'style': 'italic'}
        # warnings.warn(warning_string, UserWarning)

        pygame.init()
        pygame.display.set_caption("Algorithm Visualizer")
        self.clock = pygame.time.Clock()

        # window and static background
        self.window_surface = pygame.display.set_mode(Options.resolution)
        self.background = pygame.Surface(Options.resolution)

        # initialize pygame-gui
        self.manager = UIManager(Options.resolution)

        # axis buffer spaces
        self.x_buffer = Options.menu_x_buffer
        self.y_buffer = Options.menu_x_buffer * Options.menu_width

        # topics and algorithms
        self.topics = Options.topics

        # dropdown I
        self.drop_rect = pygame.Rect(Options.menu_width * self.x_buffer, self.y_buffer,
        Options.menu_width * (1 - self.x_buffer * 2), Options.resolution[1] * Options.ui_height)
        self.algo_dropdown = UIDropDownMenu(self.topics, self.topics[Options.start_topic], self.drop_rect, self.manager)

        # dropdown II
        self.option_rect = pygame.Rect(self.drop_rect.left, 
                self.drop_rect.top + self.drop_rect.height + Options.line_width + (2 * self.y_buffer),
                self.drop_rect.width, self.drop_rect.height)
        options = Options.option_dict[Options.topics[Options.start_topic]]
        self.options = UIDropDownMenu(options, options[1], self.option_rect, self.manager)
        self.base_option = options[1]

        # start-stop button
        button_height = Options.resolution[1] * Options.ui_height
        button_width = Options.menu_width - (2 * (self.x_buffer * Options.menu_width))
        self.button_rect = pygame.Rect(Options.menu_width * self.x_buffer,
                Options.menu_height - button_height - self.y_buffer, button_width, button_height)
        self.button = UIButton(self.button_rect, "Start", self.manager)

        # universal slider
        slider_height = Options.slider_height * Options.ui_height * Options.menu_height
        slider_width = Options.menu_width - (2 * (self.x_buffer * Options.menu_width))
        self.slide_rect = pygame.Rect(Options.menu_width * Options.menu_x_buffer, 
                self.button_rect.top - (2 * self.y_buffer )- Options.line_width - slider_height, 
                slider_width, slider_height)
        self.slider = UIHorizontalSlider(self.slide_rect, Options.slider_default, Options.slider_range, self.manager)

        # text box 1
        box_percentage = 0.3
        input_width = button_width
        input_height = button_height
        self.input_1_rect = pygame.Rect(
                Options.menu_width * self.x_buffer,
                self.slide_rect.top - self.y_buffer - input_height,
                input_width * box_percentage, input_height)
        self.input_1 = UITextEntryLine(self.input_1_rect, self.manager)

        # text box 2
        self.input_2_rect = pygame.Rect(
                (Options.menu_width * self.x_buffer) + input_width * (1 - box_percentage),
                self.input_1_rect.top,
                input_width * box_percentage, input_height)
        self.input_2 = UITextEntryLine(self.input_2_rect, self.manager)

        # compute button
        compute_width = button_width
        self.compute_rect = pygame.Rect(
                Options.menu_width * self.x_buffer, self.input_1_rect.top - button_height - self.y_buffer,
                button_width, button_height)
        self.compute_button = UIButton(self.compute_rect, "Compute", self.manager)

        # fps label
        self.fps_rect = pygame.Rect(
                Options.menu_width * self.x_buffer, self.compute_rect.top - button_height,
                button_width, button_height
                )
        self.fps_counter = UILabel(self.fps_rect, "FPS: 0", self.manager)

        # set input conditions
        self.input_1.set_text_length_limit(3)
        self.input_1.set_allowed_characters("numbers")
        self.input_2.set_text_length_limit(3)
        self.input_2.set_allowed_characters("numbers")

        # info box (gives information topic & algo specific information)
        info_width = button_width
        info_height = ((self.fps_rect.top - (self.option_rect.top + self.option_rect.height)) - (1 * self.y_buffer))

        self.info_rect = pygame.Rect(self.drop_rect.left, 
                self.option_rect.top + self.option_rect.height + self.y_buffer, info_width, info_height)
        text = self.info[Options.topics[Options.start_topic]][self.base_option]
        self.info_box = UITextBox(text, self.info_rect, self.manager)

        # draw static background
        self.draw_background()

        # for the update functions
        self.previous_topic = self.topics[Options.start_topic]
        self.previous_algo_option = self.base_option
        self.button_text = "Start"

    def draw_background(self):
        self.background.fill(pygame.Color(*Options.background_colour))
        pygame.draw.line(self.background, Options.line_colour, (Options.menu_width, 0),
                (Options.menu_width, Options.resolution[1]), Options.line_width)

        y = self.drop_rect.top + self.drop_rect.height + self.y_buffer
        pygame.draw.line(self.background, Options.line_colour, (0, y), (Options.menu_width, y), Options.line_width)
        y = self.button_rect.top - self.y_buffer - Options.line_width
        pygame.draw.line(self.background, Options.line_colour, (0, y), (Options.menu_width, y), Options.line_width)

        # text box line
        pygame.draw.line(self.background, Options.line_colour,
                (self.input_1_rect.right - 20, self.input_1_rect.top + (self.input_1_rect.height * 0.5)),
                (self.input_2_rect.left + 20, self.input_1_rect.top + (self.input_1_rect.height * 0.5)),
                Options.line_width // 2)

    def get_window(self):
        return self.window_surface

    def get_input_1(self):
        return self.input_1.get_text()

    def get_input_2(self):
        return self.input_2.get_text()

    def get_slider_value(self):
        return self.slider.get_current_value()

    def get_dropdown_topic(self):
        return self.algo_dropdown.selected_option

    def get_dropdown_algo(self):
        return self.options.selected_option

    def update_algo_dropdown(self):
        topic = self.get_dropdown_topic()
        if self.previous_topic != topic:
            self.options.kill()
            options = Options.option_dict[topic]
            self.options = UIDropDownMenu(options, options[1], self.option_rect, self.manager)
            self.options.rebuild()

            self.previous_topic = topic

    def update_info_box(self):
        topic = self.get_dropdown_topic()
        algo_option = self.get_dropdown_algo()

        if self.previous_algo_option != algo_option:
            new_text = self.info[topic][algo_option]
            self.info_box.kill()
            self.info_box = UITextBox(new_text, self.info_rect, self.manager)

            self.previous_algo_option = algo_option

    def button_pressed(self):
        return self.button.check_pressed()

    def compute_pressed(self):
        return self.compute_button.check_pressed()

    def set_button_text(self, text):
        self.button.set_text(text)
        self.button_text = text

    def enable_extras(self):
        self.compute_button.enable()
        self.input_1.enable()
        self.input_2.enable()

    def disable_start(self):
        self.button.disable()

    def enable_start(self):
        self.button.enable()

    def disable_compute(self):
        self.compute_button.disable()

    def enable_compute(self):
        self.compute_button.enable()

    def disable_extras(self):
        self.compute_button.disable()
        self.input_1.disable()
        self.input_2.disable()

    def enable(self):
        self.algo_dropdown.enable()
        self.options.enable()
        self.slider.enable()

        self.button.enable()

        self.set_button_text("Start")

    def disable(self):
        self.algo_dropdown.disable()
        self.options.disable()
        self.slider.disable()

        self.set_button_text("Running")
        self.button.disable()

        self.disable_extras()

    def tick(self):
        return self.clock.tick(Options.frame_rate) / 1000.0 # convert ms to s
        # return self.clock.tick() / 1000.0 # no frame rate

    def update(self):
        delta_time = self.tick()
        self.manager.update(delta_time)
        self.update_algo_dropdown()
        self.update_info_box()

        if Options.show_fps:
            # print("FPS:", round(self.clock.get_fps(), 2))
            fps = str(self.clock.get_fps())
            fps = fps.ljust(10, '0') if len(fps) < 10 else fps[:11]
            self.fps_counter.set_text(f"FPS: {fps}")

    def background_blit(self):
        self.window_surface.blit(self.background, (0,0)) 

    def render(self):
        self.background_blit()
        self.manager.draw_ui(self.window_surface)

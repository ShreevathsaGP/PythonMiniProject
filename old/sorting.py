# imports
import os
import math
import random
import pygame
from collections import deque

# gloabals
from globy import *
from ui import UI

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

class Sorting:
    def __init__(self, s = Options.default_sorting_size):
        self.set_size(s) # changing the size is equivalent to re initializing

    def get_options(self):
        return ["Merge Sort", "Shell Sort"]

    def process_slider(self, x):
        # print(x)
        new_size = (x * 10) - 30
        new_size = 2 ** (math.floor(((8 - 3) * (x - 5))/(25 - 5)) + 3)
        if self.size != new_size:
            self.set_size(new_size)

    def reset(self):
        self.fill_colours = [Options.sorting_c_map[0] for _ in range(self.size)]
        self.bar_width = Options.main_width / self.size

        heights = [(i + 1) * (Options.main_height / self.size) for i in range(self.size)]
        if Options.sorting_shuffle: random.shuffle(heights)
        self.bars = [None] * self.size
        self.bars = [pygame.Rect(Options.main_x + (i * self.bar_width), 
            Options.main_height - h, self.bar_width, h) for i, h in zip(range(self.size), heights)]
        
        # adjust widths to make it look better
        for i in range(self.size - 1):
            if (self.bars[i].left + self.bars[i].width) != self.bars[i + 1].left:
                diff =  self.bars[i + 1].left - (self.bars[i].left + self.bars[i].width)
                self.bars[i].width += diff

            self.bars[i].width -= Options.bar_gap

            if (self.bars[i].top + self.bars[i].height) != Options.main_height:
                diff = Options.main_height - (self.bars[i].top + self.bars[i].height)
                self.bars[i].height += diff

        # adjust right most bar
        self.bars[-1].width += Options.resolution[0] - (self.bars[-1].left + self.bars[-1].width)
        self.bars[-1].height += Options.resolution[1] - (self.bars[-1].top + self.bars[-1].height)
        
    def set_size(self, s):
        self.size = s # number of elements (ie. number of bars)
        self.reset()

    def switch_bar(self, p1, p2):
        pass

    # called every frame, computes and visualizes one step in the sorting algorithm
    def step(self):
        pass

    def render(self, window):
        for colour, bar in zip(self.fill_colours, self.bars):
            pygame.draw.rect(window, colour, bar)


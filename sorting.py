# sorting.py

# imports
import os
import math
import time
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

class Sorting:
    def __init__(self, ui, s = Options.default_sorting_size):
        self.ui = ui
        self.size = s
        self.set_size(s)

        self.delay = 0
        self.running = False

        # merge sort
        self.merge_array = []

        # heap sort
        self.heap = []
        self.heap_last = -1

    def set_size(self, s):
        self.size = s
        self.reset()

    def reset(self):
        self.fill_colours = [Options.sorting_c_map[0] for _ in range(self.size)]
        self.temp_colours = [None for _ in range(self.size)]
        self.bar_width = Options.main_width / self.size

        self.heights = [(i + 1) * (Options.main_height / self.size) for i in range(self.size)]
        if Options.sorting_shuffle: 
            random.shuffle(self.heights)

    def process_slider(self, x):
        new_size = (x * 10) - 30

        # condition
        if new_size > 256:
            new_size = 256

        if self.size != new_size:
            self.set_size(new_size)

    def process_button(self, state):
        if state == True:
            self.ui.disable()
            self.start = True

    def render(self):
        # self.ui.draw_background()
        for i, colour, height in zip(range(self.size), self.fill_colours, self.heights):
            bar = pygame.Rect(Options.main_x + (i * self.bar_width), Options.main_height - height,
                    self.bar_width, height)

            # adjust bar in x
            next_left = Options.main_x + (i + 1) * self.bar_width if i != self.size - 1 else Options.resolution[0]
            diff = next_left - (bar.left + bar.width)
            bar.width += diff
            bar.width -= Options.bar_gap

            # adjust bar in y
            diff = Options.main_height - (bar.top + bar.height)
            bar.height += diff

            pygame.draw.rect(self.ui.get_window(), colour, bar)

        pygame.display.update()
        if self.delay != 0: pygame.time.delay(self.delay)

    def heap_sort(self):
        self.heap = [-1] * self.size
        self.heap_last = -1

        # initial heapify
        self.heapify()

        # show actual colour order
        for i in range(self.size - 1, -1, -1):
            self.fill_colours[i] = Options.sorting_c_map[1]
            self.update_render()
            self.fill_colours[i] = self.temp_colours[i]
            self.update_render()

        # remove n times
        removed = []
        for i in range(self.size):
            removed.append(self.heap_remove(v = True)) # remove with visualization

            self.fill_colours[i] = Options.sorting_c_map[0]
            self.update_render()

        # show fully sorted
        for i in range(self.size - 1, -1, -1):
            self.fill_colours[i] = Options.sorting_c_map[3]
            self.update_render()

    def heapify(self):
        for i in range(self.size - 1, -1, -1):
            self.heap_add(self.heights[i], i)

        # assign actual colours
        for h in range(self.size):
            current_height = int(math.ceil(math.log(h + 2, 2.0)))
            colour = Options.heap_sort_colours[current_height - 1]
            self.temp_colours[self.heap[h][1]] = colour

    def heap_add(self, x, index):
        self.heap_last += 1

        self.heap[self.heap_last] = [x, index]
        self.heap_trickle_up(self.heap_last, True)

    def heap_remove(self, v = False):
        if self.heap_last == -1:
            return 

        return_value = self.heap[0]
        self.heap_swap(0, self.heap_last, v, r = True)
        self.heap_last -= 1

        self.heap_trickle_down(0, v)

        return return_value

    def heap_trickle_up(self, pos, v = False):
        if pos == 0:
            return

        parent = (pos - 1) // 2
        if self.heap[pos][0] > self.heap[parent][0]:
            self.heap_swap(pos, parent, v)

            return self.heap_trickle_up(parent, v)
        
    def heap_trickle_down(self, parent, v = False):
        left = (2 * parent) + 1
        right = (2 * parent) + 2

        # check leaf (no children)
        if left > self.heap_last and right > self.heap_last:
            return

        # no right child
        if right > self.heap_last:
            if self.heap[parent][0] < self.heap[left][0]:
                self.heap_swap(parent, left, v)
                return self.heap_trickle_down(left, v)
            else:
                return

        # has both children
        if self.heap[parent][0] < self.heap[left][0] or self.heap[parent][0] < self.heap[right][0]:

            if self.heap[left][0] > self.heap[right][0]:
                self.heap_swap(parent, left, v)
                self.heap_trickle_down(left, v)
            else:
                self.heap_swap(parent, right, v)
                self.heap_trickle_down(right, v)

    def heap_swap(self, p1, p2, v = False, r = False):
        self.heap[p1], self.heap[p2] = self.heap[p2], self.heap[p1]
        self.heap[p1][1], self.heap[p2][1] = self.heap[p2][1], self.heap[p1][1] # switch indices

        # swap in bars
        temp_1 = self.fill_colours[self.heap[p1][1]]
        temp_2 = self.fill_colours[self.heap[p2][1]] if not r else Options.sorting_c_map[2]

        self.fill_colours[self.heap[p1][1]] = Options.sorting_c_map[1]
        self.fill_colours[self.heap[p2][1]] = Options.sorting_c_map[1]

        self.update_render()

        # switch heights
        self.heights[self.heap[p1][1]], self.heights[self.heap[p2][1]], = self.heights[self.heap[p2][1]], self.heights[self.heap[p1][1]]
        self.update_render()

        self.fill_colours[self.heap[p1][1]] = temp_1
        self.fill_colours[self.heap[p2][1]] = temp_2
        self.update_render()

    def merge(self, a, b, c, d):
        i = a
        j = c
        merge_array = []

        while i <= b and j <= d:
            self.fill_colours[i] = Options.sorting_c_map[1]
            self.fill_colours[j] = Options.sorting_c_map[1]
            self.update_render()
            self.fill_colours[i] = Options.sorting_c_map[0]
            self.fill_colours[j] = Options.sorting_c_map[0]

            # merge in ascending
            if self.heights[i] < self.heights[j]:
                merge_array.append(self.heights[i])
                i += 1
            else:
                merge_array.append(self.heights[j])
                j += 1

        # append remaining from left
        while i <= b:
            self.fill_colours[i] = Options.sorting_c_map[1]
            self.update_render()
            self.fill_colours[i] = Options.sorting_c_map[0]
            merge_array.append(self.heights[i])
            i += 1

        # append remaining from right
        while j <= d:
            self.fill_colours[j] = Options.sorting_c_map[1]
            self.update_render()
            self.fill_colours[j] = Options.sorting_c_map[0]
            merge_array.append(self.heights[j])
            j += 1

        j = 0
        for i in range(a, d + 1):
            self.heights[i] = merge_array[j]
            j += 1
            self.fill_colours[i] = Options.sorting_c_map[2]
            self.update_render()

            # final show
            if d - a == self.size - 1:
                self.fill_colours[i] = Options.sorting_c_map[3]
            else:
                self.fill_colours[i] = Options.sorting_c_map[0]

    # recursive merge sort
    def merge_sort(self, l, r):
        mid = (l + r) // 2

        if l < r:
            self.merge_sort(l, mid)
            self.merge_sort(mid + 1, r)
            self.merge(l, mid, mid + 1, r)

    def update(self):
        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                exit() # relevant for sorting but not in some other places

            self.ui.manager.process_events(event)

        # process ui events
        self.process_slider(self.ui.get_slider_value())
        self.process_button(self.ui.button_pressed())

        # update-render
        self.ui.update()
        self.ui.render()

    def update_render(self):
        self.update()
        self.render()

    def reset_colours(self):
        self.fill_colours = [Options.sorting_c_map[0]] * self.size

    def run(self) -> bool:
        self.running = True
        self.start = False
        self.ui.disable_extras()

        while self.running and self.ui.get_dropdown_topic() == Options.topics[0]:
            self.update()

            # visualize
            if not self.start:
                self.render()
            else:
                if self.ui.get_dropdown_algo() == Options.sorting_options[0]:
                    self.reset_colours()
                    self.delay = int((Options.frame_rate // Options.sorting_fps_delay_ratio) * (1))

                    # merge sort
                    self.merge_sort(0, self.size - 1)

                    # # do a final show (as sanjay said)
                    # for i in range(self.size):
                    #     self.fill_colours[i] = Options.heap_sort_colours[-1]

                    self.delay = 0

                    # restart ui
                    self.ui.enable()
                    self.start = False
                    self.running = True # cannot close the program
                
                elif self.ui.get_dropdown_algo() == Options.sorting_options[1]:
                    self.reset_colours()
                    self.delay = int((Options.frame_rate // Options.sorting_fps_delay_ratio) * (0.5))

                    # heap sort
                    self.heap_sort()

                    self.delay = 0

                    # restart ui
                    self.ui.enable()
                    self.start = False
                    self.running = True # cannot close the program

        return self.running



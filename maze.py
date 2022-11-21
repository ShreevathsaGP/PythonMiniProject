# maze.py

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

class MazeSolve:
    def __init__(self, ui):
        self.ui = ui
        self.running = True

    def process_slider(self, x):
        pass

    def render(self):

        pygame.display.update()


    def run(self) -> bool:
        self.running = True
        while self.running and self.ui.get_dropdown_topic() == Options.topics[2]:
            # process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.ui.manager.process_events(event)

            # process slider
            self.process_slider(self.ui.get_slider_value())

            # update-render
            self.ui.update()
            self.ui.render()

            # visualize
            self.render()

        return self.running


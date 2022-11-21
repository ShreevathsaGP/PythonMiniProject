# imports
import os
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

class GraphSearch:
    def __init__(self):
        pass

    def get_options(self):
        return ["Depth First", "Breadth First"]

    def process_slider(self, x):
        pass

    def render(self, window):
        pass

    def step(self):
        pass


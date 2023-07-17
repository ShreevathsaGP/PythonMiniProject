# main.py

# imports
import os
import math
import json
import pickle
import random
import pygame
from collections import deque

# globals
from ui import UI
from globy import *

# sub classes
from maze import MazeSolve
from sorting import Sorting
from graph import GraphSearch
from graph_tools import *

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

class AlgorithmVisualizer:
    def __init__(self):
        self.running = True

        self.ui = UI()

        self.new_topic = None
        self.current_topic = Options.topics[Options.start_topic]
        self.topic_objects = {Options.topics[0]: Sorting(self.ui), Options.topics[1]: GraphSearch(self.ui), Options.topics[2]: MazeSolve(self.ui)}


    def run(self):
        """
        This run function calls the run function of the topic classes. [ex: Sorting(self.ui).run()]

        Whenever there is a change in the topic, the topic class returns to this function's while 
        loop and this function redirects it to the new topics topic-class and its run function.
        """

        if Options.ui_only_mode:
            while self.running:
                # process events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    self.ui.manager.process_events(event)

                # update-render
                self.ui.update()
                self.ui.render()

                pygame.display.update()
            
        else:
            while self.running:
                self.ui.enable_start()
                self.running = self.topic_objects[self.current_topic].run()
                self.current_topic = self.ui.get_dropdown_topic()

if __name__ == "__main__":
    app = AlgorithmVisualizer()
    app.run()

################################ Sudoku Project ################################
# Author:      Victor Espinoza
# Created:     Mid-November / December 2021
# Project:     Sudoku
#
# File Name:   button_class.py
#
# Description: This file contains all of the necessary components that make up
#              a button. This includes the button position, surface, text,
#              width, height, color, etc...
#
################################################################################

import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text = None, color = (73, 73, 73),
     background_color = (189, 189, 189), function = None, params = None):
        self.surface = pygame.Surface((width, height)) # button surface
        self.pos = (x,y) # position of the button
        self.rect = self.surface.get_rect() # rectangle encompassing the button
        # set the top-left of rectangle to coinside with the button position
        self.rect.topleft = self.pos
        self.text = text # text displayed inside of the button
        self.color = color # primary color of the button
        self.background_color = background_color # background color of button
        self.function = function # function executed when button is pressed
        self.params = params # parameters passed into the function
        self.selected = False # keeps track of whether button was selected
        self.width = width # width of the button
        self.height = height # height of the button


    ################### update function ##################
    # Keeps track of whether the mouse and button postions intersect
    def update(self, mouse):
        # switch selected flag if the mouse and button postions intersect
        if self.rect.collidepoint(mouse):
            self.selected = True
        else:
            # positions don't intersect, so set selected to False
            self.selected = False


    #################### draw function ###################
    # Draws the button on the provided window
    def draw(self, window):
        # Display the correct color based on whether the mouse position
        # intersects with the inside of the button
        self.surface.fill(self.background_color if self.selected else
         self.color)
        if self.text:
            # Adds the buttons text (if applicable) to the surface
            self.add_text_to_surface(self.text)
        # Blit the button and its text to the window
        window.blit(self.surface, self.pos)


    ################### click function ###################
    # Executes the desired function whenever the mouse is clicked anywhere
    # inside of the button
    def click(self):
        # Include any available parameters when executing the function
        if self.params:
            self.function(self.params)
        else:
            # If no parameters are present, then just execute the function
            self.function()


    ############ add_text_to_surface function ############
    # Add the button text to the surface of the surface
    def add_text_to_surface(self, text):
        # Create a font for the button text
        font = pygame.font.SysFont("arial", 20, bold=1)
        # Render the font with the button text
        text = font.render(text, True, BLACK)
        # Find the center of the button (make sure to subtract the text-width
        # and text-height so that it will be correctly centered in the button)
        x = (self.width - text.get_width())//2
        y = (self.height - text.get_height())//2
        # Add the text to the center of the button
        self.surface.blit(text, (x, y))

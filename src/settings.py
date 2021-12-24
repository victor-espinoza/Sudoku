################################ Sudoku Project ################################
# Author:      Victor Espinoza
# Created:     Mid-November / December 2021
# Project:     Sudoku
#
# File Name:   settings.py
#
# Description: This file contains all of the constant variables that are used
#              throughout the project.
#
################################################################################

############################### GENERAL CONSTANTS ##############################
# General window/sudoku-related constants
WIDTH = 600 # width of the window
HEIGHT = 600 # height of the window
GRID_POS = (75, 75) # position of the Sudoku grid on the screen
CELL_SIZE = 50 # size of each cell on the Sudoku grid
GRID_SIZE = CELL_SIZE * 9 # size of the entire Sudoku grid
SUBGRID_WIDTH = 3 # width of each subgrid on the Sudoku
SUBGRID_HEIGHT = 3 # height of each subgrid on the Sudoku
ROWS = 9 # number of rows in the Sudoku
COLS = 9 # number of columns in the Sudoku
NUMS = 9 # number of digits available to input into the Sudoku  (1-9)

# Padding-related constants
BTN_PADDING = 5 # padding used between each button
NOTES_PADDING = 2 # padding used between each note on the Sudoku board

# Button-related constants
BTN_WIDTH = 100 # width of a standard button
BIG_BTN_WIDTH = 150 # width of a larger button
BTN_HEIGHT = 40 # height of a standard button

# This variable calculates the total width of the playing buttons displayed
# under the Sudoku board (also includes the padding between the buttons)
PLAYING_BTN_WIDTH = (BTN_WIDTH * 3) + BIG_BTN_WIDTH + BTN_PADDING * 3
# This variable calculates the center point of the playing buttons under the
# Sudoku board and the window (with respect to the width of the window)
PLAY_BTN_DIFF = (WIDTH - PLAYING_BTN_WIDTH)//2

# This variable calculates the total width of the finished buttons displayed
# under the Sudoku board (also includes the padding between the buttons)
FINISHED_BTN_WIDTH = (BTN_WIDTH * 2) + BIG_BTN_WIDTH + (BTN_PADDING * 2)
# This variable calculates the center point of the playing buttons under the
# Sudoku board and the window (with respect to the width of the window)
FIN_BTN_DIFF = (WIDTH - FINISHED_BTN_WIDTH)//2

# This variable calculates the total height of the change difficulty buttons
# and the prompt text (also includes the padding between the buttons and prompt)
CHANGE_BTN_HEIGHT = (BTN_HEIGHT * 5) + (BTN_PADDING * 4)
# This variable calculates the center point of the change difficulty buttons and
# the prompt text
CHANGE_BTN_DIFF = (HEIGHT - CHANGE_BTN_HEIGHT)//2


############################# GAME TESTING BOARDS ##############################
# Sudoku boards used for testing various aspects of the project
# completely empty board
EMPTY_BOARD = [[0 for x in range(9)] for x in range(9)]
# valid sudoku board
VALID_SUDOKU_BOARD = [[0, 0, 8, 9, 0, 0, 0, 0, 6],
                      [0, 1, 0, 0, 4, 3, 0, 9, 0],
                      [0, 0, 7, 5, 0, 0, 1, 0, 4],
                      [0, 0, 4, 8, 9, 0, 0, 5, 0],
                      [8, 0, 3, 1, 0, 4, 2, 0, 9],
                      [0, 9, 0, 0, 3, 6, 4, 0, 0],
                      [4, 0, 9, 0, 0, 5, 6, 0, 0],
                      [0, 3, 0, 4, 2, 0, 0, 1, 0],
                      [2, 0, 0, 0, 0, 7, 9, 0, 0]]
# almost-finished sudoku board
ALMOST_FINISHED_BOARD = [[1, 6, 3, 9, 7, 2, 5, 4, 8],
                         [8, 9, 7, 5, 6, 4, 2, 3, 1],
                         [4, 5, 2, 1, 3, 8, 9, 6, 7],
                         [6, 2, 5, 3, 8, 9, 1, 7, 4],
                         [3, 8, 4, 7, 2, 1, 6, 9, 5],
                         [9, 7, 1, 4, 5, 6, 3, 8, 2],
                         [5, 4, 6, 2, 9, 7, 8, 1, 3],
                         [2, 1, 9, 8, 4, 3, 7, 5, 6],
                         [7, 3, 8, 6, 1, 5, 4, 2, 0]]
# board that is unsolvable (edge case where only last cell is unfilled)
UNSOLVABLE_BOARD = [[1, 6, 3, 9, 7, 2, 5, 4, 8],
                   [8, 9, 7, 5, 6, 4, 2, 3, 1],
                   [4, 5, 2, 1, 3, 8, 9, 6, 7],
                   [6, 2, 5, 3, 8, 9, 1, 7, 4],
                   [3, 8, 4, 7, 2, 1, 6, 9, 5],
                   [9, 7, 1, 4, 5, 6, 3, 8, 2],
                   [5, 4, 6, 2, 9, 7, 8, 1, 3],
                   [2, 1, 9, 8, 4, 3, 7, 5, 6],
                   [7, 3, 8, 6, 1, 5, 4, 3, 0]]
# general unsolvable board
UNSOLVABLE_BOARD2 = [[9, 8, 3, 1, 7, 5, 2, 4, 6],
                     [1, 5, 2, 6, 9, 4, 8, 7, 3],
                     [7, 6, 4, 8, 3, 2, 9, 1, 5],
                     [0, 0, 4, 8, 9, 0, 0, 5, 0],
                     [8, 0, 3, 1, 0, 4, 2, 0, 9],
                     [0, 9, 0, 0, 3, 6, 4, 0, 0],
                     [4, 0, 9, 0, 0, 5, 6, 0, 0],
                     [0, 3, 0, 4, 2, 0, 0, 1, 0],
                     [2, 0, 0, 0, 0, 7, 9, 0, 0]]

#################################### COLORS ####################################
# Different colors used throughout the project
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OFF_BLACK= (64, 64, 64)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (96, 216, 232)
STEEL_BLUE = (176,196,222)
LOCKED_GRAY = (170, 170, 170)
OLD_ROSE = (195, 121, 121)
GRAY = (205, 205, 205)
SKY_BLUE = (27, 142, 207)
GREEN = (117,172, 112)
MUSTARD = (204,197,110)
ORANGE = (199,129,48)
WARM_RED = (207,68,68)
DK_GRAY = (105,105,105)

############################### STRING CONSTANTS ###############################
# String constants used throughout the project
PROMPT_TEXT = "Please Choose A Difficulty:"
ELAPSED_TIME_TEXT = "Elapsed Time:"
TOTAL_TIME_TEXT = "Total Time:"

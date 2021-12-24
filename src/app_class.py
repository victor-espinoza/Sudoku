################################ Sudoku Project ################################
# Author:      Victor Espinoza
# Created:     Mid-November / December 2021
# Project:     Sudoku
#
# File Name:   app_class.py
#
# Description: This file contains all of the game and drawing logic that makes
#              up the Sudoku game. It also handles all of the user input and
#              displays any changes in the game logic to the user.
#
################################################################################

import pygame, sys
import pygame.freetype
from pygame.locals import *
import requests
from bs4 import BeautifulSoup
from settings import *
import button_class as btn


class App:

    def __init__(self):
        pygame.init() # initializes pygame
        self.window = pygame.display.set_mode((WIDTH, HEIGHT)) # project window
        self.running = True # tells program when to stop running the project
        self.solving_board = False # used to show user their correct cells
        self.selected = None # the mouse position in relation to the Sudoku
        self.mouse_pos = None # the raw mouse position
        self.state = "CHANGE_DIFFICULTY" # the current game state
        self.cell_changed = False # tracks if a cell's contents have changed
        self.hints_enabled = True # enables or disables game hints
        self.correct_cells = [] # list holding the correct cell indices
        self.conflicting_cells = [] # list holding conflicting cell indices
        self.playing_buttons = [] # list holding the playing state buttons
        self.notes_button = None # notes button
        self.hints_button = None # hints button
        self.difficulty_buttons = [] # list holding the difficulty buttons
        self.finished_buttons = [] # list holding the finished state buttons
        self.difficulty = None # holds the value of the desired difficulty level
        self.notes_enabled = False # enables or disables Sudoku notes
        self.start_time = None # start time of the game
        self.elapsed_time = None # currently elapsed time for the game
        self.end_time = None # finish time of the game
        self.locked_cells = [] # list holding the locked Sudoku cells
        self.font = pygame.font.SysFont("arial", CELL_SIZE//2) # text font
        self.notes_font = pygame.font.SysFont("arial", CELL_SIZE//3) #notes font
        self.sudoku_board = [] # holds the actual Sudoku board values
        # Holds the finished Sudoku board values (initialized to 0's)
        self.finished_board = [[0 for x in range(ROWS)] for x in range(COLS)]
        # Holds the note values that the user enters throughout the game.
        # Each note for each cell is initialized to False.
        self.notes = [[[False for x in range(ROWS)] for y in range(COLS)]
         for z in range(NUMS)]
        self.load_buttons() # loads the game buttons
        self.start_time = pygame.time.get_ticks() # starts the game time
        # clock used to cause a small delay when displaying the window
        self.clock = pygame.time.Clock()
        # used for testing the different boards
        # self.state = "PLAYING"
        # self.sudoku_board = UNSOLVABLE_BOARD2
        # self.reset_locked_cells()
        # self.difficulty = 1
        # print("Initializing program...")
        # if not self.is_solvable(self.sudoku_board):
        #     print("The provided Sudoku board isn't valid... Lets get a new one")
        #     self.get_sudoku_board(self.difficulty)
        # self.start_time = pygame.time.get_ticks()
        # self.clock = pygame.time.Clock()

################################# PROGRAM LOOP #################################

    #################### run function ####################
    # This function runs the correct events, updates, and drawing functions
    # based on what the current game state is.
    def run(self):
        while self.running:
            if self.state == "PLAYING":
                # Execute PLAYING state fuctions
                self.playing_events() # check events
                self.playing_update() # update game logic
                self.playing_draw() # draw game board
            if self.state == "FINISHED":
                # Execute FINISHED state functions
                self.finished_events() # check events
                self.finished_update() # update game logic
                self.finished_draw() # draw finished board
            if self.state == "CHANGE_DIFFICULTY":
                # Execute CHANGE_DIFFICULTY state functions
                self.difficulty_events() # check events
                self.difficulty_update() # update game logic
                self.difficulty_draw() # draw select difficulty window
        # when the game is no longer running, close pygame and exit the program
        pygame.quit() # quit pygame
        sys.exit() # exit the program
################################################################################



############################# PLAYING STATE LOGIC ##############################

    ############## playing_events function ###############
    # This function keeps track of important events that occur during the
    # PLAYING state. Such events include quitting the program, clicking on the
    # screen, or pressing a character on the keyboard.
    def playing_events(self):
        # iterate through each pygame event
        for event in pygame.event.get():
            # exit the program if the user wants to quit
            if event.type == pygame.QUIT:
                self.running = False # this causes exiting code to be performed
            # check to see if the user has clicked on the window
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouse_on_grid() # get the mouse position
                if selected:
                    # if the mouse position intersects with the grid, then
                    # assign the position to the self.selected variable,
                    # otherwise just ignore the mouse press
                    self.selected = selected
                    # reset conflicting cells (since the cell has now changed)
                    self.conflicting_cells = []
                else:
                    # make the variable empty since the mouse isn't on the board
                    self.selected = None
                    # Iterate through the playing buttons and check to see if
                    # any of them were pressed.
                    for button in self.playing_buttons:
                        # only execute the click function if the user actually
                        # pressed the button
                        if button.selected:
                            # Exit the note-taking state whenever another button
                            # is pressed (only if currently in said-state)
                            if button.text != "Notes" and self.notes_enabled:
                                self.toggle_notes()
                            # Prepare the program to create a new Sudoku board
                            if button.text == "New Game":
                                # Add in the current difficulty into the
                                # button's parameters and execute the click
                                # function
                                button.params = self.difficulty
                                button.click() # get_sudoku_board function
                                self.state = "PLAYING" # update game state
                                self.reset_time() # reset start time
                            else:
                                button.click() # execute button function
            # check to see if the user typed on keyboard
            if event.type == pygame.KEYDOWN:
                # make sure that the selected cell in inside of the Sudoku
                # board and that it isn't locked (has a pre-determined value)
                if self.selected != None and (list(self.selected)
                 not in self.locked_cells):
                    # make sure the key press was an integer
                    if self.is_int(event.unicode):
                        digit_val = int(event.unicode) # integer value of key
                        # check to see if notes are enabled
                        if self.notes_enabled:
                            # make sure key press was greater than 0
                            if (digit_val > 0):
                                # assign the correct note value (indexes are
                                # 0-based so subtract 1 from value to get it's
                                # correct index)
                                val = self.notes[self.selected[0]][
                                 self.selected[1]][digit_val - 1]
                                self.notes[self.selected[0]][self.selected[1]][
                                 digit_val - 1] = not val
                                # reset board value if a note was assigned to
                                # the selecetd cell.
                                self.sudoku_board[self.selected[0]][
                                 self.selected[1]] = 0
                        else:
                            # notes weren't enabled, then assign the selected
                            # cell with the key press value or toggle value
                            if self.sudoku_board[self.selected[0]][
                             self.selected[1]] == digit_val:
                                self.sudoku_board[self.selected[0]][
                                 self.selected[1]] = 0
                            else:
                                self.sudoku_board[self.selected[0]][
                                 self.selected[1]] = digit_val
                            self.cell_changed = True # set flag to true
                            # remove any notes in the selected cell's
                            # surrounding row, column, and subgrid (remember to
                            # subtract 1 from value since indexes are 0-based)
                            if (digit_val > 0):
                                self.remove_notes(self.selected, digit_val - 1)
                            # update conflicting cells accordingly
                            self.update_conflicting_cells(int(event.unicode))


    ############## playing_update function ###############
    # This function updates the overall game logic for the PLAYING state
    def playing_update(self):
        self.mouse_pos = pygame.mouse.get_pos() # get the mouse position
        # iterate through playing buttons and update them accordingly
        for button in self.playing_buttons:
            button.update(self.mouse_pos) # update button
        # check game board status
        if self.cell_changed:
            # check to see if the Sudoku board is finished
            if self.is_finished():
                self.state = "FINISHED" # update game state
                self.selected = None # update selected variable
                self.update_time() # update the elapsed time variable
                self.end_time = self.elapsed_time # get the finished game time


    ################ playing_draw function ###############
    # This function draws the elapsed time, the game board, and all of the
    # playing buttons to the screen.
    def playing_draw(self):
        self.window.fill(DK_GRAY) # fill in window with dark gray color
        self.update_time() # update elapsed time
        self.display_time(ELAPSED_TIME_TEXT, self.elapsed_time) # display time
        # iterate through each playing button and draw it on the window
        for button in self.playing_buttons:
            button.draw(self.window) # draw playing button
        # fill game area in with white
        pygame.draw.rect(self.window, WHITE, (GRID_POS[0], GRID_POS[1],
         GRID_SIZE, GRID_SIZE))
        # shade in the selected cell (if one is selected)
        if self.selected:
            # shade in the surrounding row, column, and subgrid
            self.shade_surrounding_cells(self.window, self.selected, STEEL_BLUE)
            self.shade_cells(self.window, [list(self.selected)], LIGHT_BLUE)
            #self.shade_selected_cell(self.window, self.selected, LIGHT_BLUE)
        # display any active notes on the Sudoku board
        self.show_notes(self.window)
        # shade in all of the locked cells
        self.shade_cells(self.window, self.locked_cells, LOCKED_GRAY)
        # shade in any conflicting cells (if hints are enabled)
        if self.hints_enabled:
            self.shade_cells(self.window, self.conflicting_cells, OLD_ROSE)
        # if the backtracking algorithm is being run, shade in all the correct
        # cells that the user has input to the Sudoku board
        if self.solving_board :
            self.shade_cells(self.window, self.correct_cells, GRAY)
        # show all of the current Sudoku values on the screen
        self.draw_numbers(self.window)
        # draw the Sudoku board grid (the gameboard outline and internal boxes)
        self.draw_grid(self.window)
        pygame.display.update() # update pygame
        self.cell_changed = False # update variable to prevent an infinite loop
################################################################################



############################# FINISHED STATE LOGIC #############################

    ############## finished_events function ##############
    # This function keeps track of important events that occur during the
    # FINISHED state. Such events include quitting the program and clicking on
    # the screen.
    def finished_events(self):
        # iterate through each pygame event
        for event in pygame.event.get():
            # exit the program if the user wants to quit
            if event.type == pygame.QUIT:
                self.running = False # this causes exiting code to be performed
            # check to see if the user has clicked on the window
            if event.type == pygame.MOUSEBUTTONDOWN:
                # iterate through each finished button
                for button in self.finished_buttons:
                    # check to see if the user clicked on a button
                    if button.selected:
                        if button.text == "New Game":
                            # add in difficulty parameters
                            button.params = self.difficulty
                            button.click() # get_sudoku_board function
                            self.state = "PLAYING" # update game state
                            self.reset_time() # reset starting time
                        elif button.text == "Change Difficulty":
                            self.state = "CHANGE_DIFFICULTY" # update game state
                            button.click() # change_difficulty function
                        else:
                            button.click() # execute button function


    ############## finished_update function ##############
    # This function updates the overall game logic for the FINISHED state
    def finished_update(self):
        self.mouse_pos = pygame.mouse.get_pos() # get current mouse position
        # iterate through each finished button
        for button in self.finished_buttons:
            button.update(self.mouse_pos) # update button accordingly


    ############### finished_draw function ###############
    # This function draws the finish time, the completed Sudoku board, and all
    # of the finished buttons to the screen.
    def finished_draw(self):
        self.window.fill(DK_GRAY) # fill window in with dark gray color
        self.display_time(TOTAL_TIME_TEXT, self.end_time) # display finish time
        # iterate through each finished button
        for button in self.finished_buttons:
            button.draw(self.window) # draw button on window
        # fill game area in with gray
        pygame.draw.rect(self.window, GRAY, (GRID_POS[0], GRID_POS[1],
         GRID_SIZE, GRID_SIZE))
        # Shade locked cells
        self.shade_cells(self.window, self.locked_cells, LOCKED_GRAY)
        # show all of the current Sudoku values on the screen
        self.draw_numbers(self.window)
        # draw the Sudoku board grid (the gameboard outline and internal boxes)
        self.draw_grid(self.window)
        pygame.display.update() # update pygame
################################################################################



######################## CHANGE_DIFFICULTY STATE LOGIC #########################

    ############# difficulty_events function #############
    # This function keeps track of important events that occur during the
    # CHANGE_DIFFICULTY state. Such events include quitting the program and
    # clicking on the screen.
    def difficulty_events(self):
        for event in pygame.event.get():
            # exit the program if the user wants to quit
            if event.type == pygame.QUIT:
                self.running = False # this causes exiting code to be performed
            # check to see if the user has clicked on the window
            if event.type == pygame.MOUSEBUTTONDOWN:
                # iterate through each difficulty button
                for button in self.difficulty_buttons:
                    # check to see if the user clicked on a button
                    if button.selected:
                        button.click() # get_sudoku_board function
                        self.state = "PLAYING" # update the game state
                        # update difficulty variable with button parameters
                        self.difficulty = button.params
                        self.reset_time() # reset start time


    ############# difficulty_update function #############
    # This function updates the overall game logic for the CHANGE_DIFFICULTY
    # state
    def difficulty_update(self):
        self.mouse_pos = pygame.mouse.get_pos() # get the current mouse position
        # iterate through each difficulty button
        for button in self.difficulty_buttons:
            button.update(self.mouse_pos) # update button accordingly


    ############## difficulty_draw function ##############
    # This function draws the change difficulty promp text and all of the
    # difficulty buttons to the screen.
    def difficulty_draw(self):
        self.window.fill(DK_GRAY) # fill  background in with dark gray color
        font = self.font.render(PROMPT_TEXT, True, BLACK) # prompt text font
        # get the center of the window
        x = (WIDTH - font.get_width())//2
        # Make sure to adjust the height coordinate to be closer towards the
        # top of the window since we don't want to have the text displayed
        # exactly in the center of the window.
        y = CHANGE_BTN_DIFF
        self.window.blit(font, (x, y)) # Blit prompt text to window
        # iterate through each difficulty button
        for button in self.difficulty_buttons:
            button.draw(self.window) # draw button on window
        pygame.display.update() # update pygame
################################################################################



########################### TIME-RELATED FUNCTIONS ###########################

    ################ reset_time function #################
    # This function resets the start time for the Sudoku game
    def reset_time(self):
        self.start_time = pygame.time.get_ticks() # reset start time
        self.update_time() # update elapsed time


    ################ update_time function ################
    # This function updates the elapsed time for the Sudoku game
    def update_time(self):
        # update elapsed time (time is returned in seconds)
        self.elapsed_time  = (pygame.time.get_ticks() - self.start_time) // 1000


    ################ convert_time function ###############
    # This function converts the given time into a string version of itself
    def convert_time(self, time):
        hours = time//3600 # 3,600 seconds in 1 hour
        minutes = time//60 % 60 # 60 seconds in a minute (1-59 minutes)
        seconds = time % 60 # (1 - 59 seconds)
        # add all of the time variables into the string (a 0 is put in front of
        # the variable if it is less than 10)
        time_str = ("" if hours < 1 else
         (("0" + str(hours) + ":") if hours < 10 else (str(hours)) + ":")) + (
         ("0" + str(minutes)) if minutes < 10 else str(minutes)) + ":" + (
         ("0" + str(seconds)) if seconds < 10 else str(seconds))
        return time_str # return string


    ################ display_time function ###############
    # this function displays the given time and text on the window
    def display_time(self, text, time):
        # Show elapsed time on the window
        font = self.font.render(text, True, BLACK) # font for the text
        # font for the given time string
        time_font = self.font.render(self.convert_time(time), True, BLACK)
        # get the center of the window
        font_width = font.get_width()
        x = (WIDTH - font_width - BTN_PADDING - time_font.get_width())//2
        # Make sure to adjust the height coordinate to be closer towards the
        # top of the window since we don't want to have the text displayed
        # exactly in the center of the window.
        y = (GRID_POS[1] - BTN_HEIGHT)
        self.window.blit(font, (x, y)) # blit text to window
        x += font_width + BTN_PADDING # add in padding between text and time
        self.window.blit(time_font, (x,y)) # blit time string to window
################################################################################



########################### BUTTON-RELATED FUNCTIONS ###########################

    ################ load_buttons function ###############
    # This function loads in all of the buttons used throughout the program
    def load_buttons(self):
        # PLAYING STATE BUTTONS
        # New Game button (starts a new game with the current difficulty)
        self.playing_buttons.append(btn.Button(PLAY_BTN_DIFF,
         (GRID_POS[1] + GRID_SIZE + (2 * BTN_PADDING)), BTN_WIDTH, BTN_HEIGHT,
         function = self.get_sudoku_board, color = STEEL_BLUE,
         background_color = LIGHT_BLUE, text = "New Game"))
        # Change Difficulty button (changes the Sudoku to a different difficulty
        # and starts a new game in said difficulty)
        self.playing_buttons.append(btn.Button((PLAY_BTN_DIFF + BTN_PADDING +
         BTN_WIDTH), (GRID_POS[1] + GRID_SIZE + (2 * BTN_PADDING)),
         BIG_BTN_WIDTH, BTN_HEIGHT, function = self.change_difficulty,
         color = SKY_BLUE, background_color = LIGHT_BLUE,
         text = "Change Difficulty"))
        # Notes button (allows the user to add in notes to the Sudoku)
        # I swap this button's color and background color when the user clicks
        # the button to let them know whether the button is enabled or not,
        # which is why I need a reference to this button.
        self.notes_button = btn.Button((PLAY_BTN_DIFF + (2 * BTN_PADDING) +
         BTN_WIDTH + BIG_BTN_WIDTH), (GRID_POS[1] + GRID_SIZE +
         (2 * BTN_PADDING)), BTN_WIDTH, BTN_HEIGHT,
         function = self.toggle_notes, color = OLD_ROSE,
         background_color = GREEN, text = "Notes")
        # add notes button to playing_buttons list
        self.playing_buttons.append(self.notes_button)
        # Solve button (solves the Sudoku using backtracking and shows
        # this process to the user)
        self.playing_buttons.append(btn.Button((PLAY_BTN_DIFF +
         (3 * BTN_PADDING) + (2 * BTN_WIDTH) + BIG_BTN_WIDTH),
         (GRID_POS[1] + GRID_SIZE + (2 * BTN_PADDING)), BTN_WIDTH,
         BTN_HEIGHT, function = self.show_solve, color = MUSTARD,
         background_color = LIGHT_BLUE, text = "Solve"))
        # Hints button (toggles whether the user wants to enable hints or not)
        # I swap this button's color and background color when the user clicks
        # the button to let them know whether the button is enabled or not,
        # which is why I need a reference to this button.
        self.hints_button = btn.Button((GRID_POS[0] + GRID_SIZE - BTN_WIDTH),
         (GRID_POS[1] - BTN_HEIGHT - BTN_PADDING), BTN_WIDTH, BTN_HEIGHT,
         function = self.toggle_hints, color = GREEN,
         background_color = OLD_ROSE, text = "Hints")
        # add hints button to playing_buttons list
        self.playing_buttons.append(self.hints_button)

        # CHANGE_DIFFICULTY state buttons
        # Easy button (creates an easy difficulty game)
        self.difficulty_buttons.append(btn.Button((WIDTH - BTN_WIDTH)//2,
         (CHANGE_BTN_DIFF + BTN_HEIGHT + BTN_PADDING), BTN_WIDTH, BTN_HEIGHT,
         function = self.get_sudoku_board, params = "1", color = GREEN,
         background_color = LIGHT_BLUE, text = "Easy"))
        # Medium button (creates a medium difficulty game)
        self.difficulty_buttons.append(btn.Button((WIDTH - BTN_WIDTH)//2,
         (CHANGE_BTN_DIFF + (2 * BTN_HEIGHT) + (2 * BTN_PADDING)), BTN_WIDTH,
         BTN_HEIGHT, function = self.get_sudoku_board, params = "2",
         color = MUSTARD, background_color = LIGHT_BLUE, text = "Medium"))
        # Hard button (creates a hard difficulty game)
        self.difficulty_buttons.append(btn.Button((WIDTH - BTN_WIDTH)//2,
         (CHANGE_BTN_DIFF + (3 * BTN_HEIGHT) + (3 * BTN_PADDING)), BTN_WIDTH,
         BTN_HEIGHT, function = self.get_sudoku_board, params = "3",
         color = ORANGE, background_color = LIGHT_BLUE, text = "Hard"))
        # Evil button (creates an evil difficulty game)
        self.difficulty_buttons.append(btn.Button((WIDTH - BTN_WIDTH)//2,
         (CHANGE_BTN_DIFF + (4 * BTN_HEIGHT) + (4 * BTN_PADDING)), BTN_WIDTH,
         BTN_HEIGHT, function = self.get_sudoku_board, params = "4",
         color = WARM_RED, background_color = LIGHT_BLUE, text = "Evil"))

        # FINISHED state buttons
        # New Game button (starts a new game with the current difficulty)
        self.finished_buttons.append(btn.Button(FIN_BTN_DIFF,
         (GRID_POS[1] + GRID_SIZE + (2 * BTN_PADDING)), BTN_WIDTH, BTN_HEIGHT,
         function = self.get_sudoku_board, color = STEEL_BLUE,
         background_color = LIGHT_BLUE, text = "New Game"))
        # Change Difficulty button (changes the Sudoku to a different difficulty
        # and starts a new game in said difficulty)
        self.finished_buttons.append(btn.Button((FIN_BTN_DIFF + BTN_WIDTH +
         BTN_PADDING), (GRID_POS[1] + GRID_SIZE + (2 * BTN_PADDING)),
         BIG_BTN_WIDTH, BTN_HEIGHT, function = self.change_difficulty,
         color = SKY_BLUE, background_color = LIGHT_BLUE,
         text = "Change Difficulty"))
        # Quit button (ends the game and quits the program)
        self.finished_buttons.append(btn.Button(
         (FIN_BTN_DIFF + BIG_BTN_WIDTH + BTN_WIDTH + (2 * BTN_PADDING)),
         (GRID_POS[1] + GRID_SIZE + (2 * BTN_PADDING)), BTN_WIDTH, BTN_HEIGHT,
         function = self.quit_game, color = RED, background_color = WARM_RED,
         text = "Quit"))


    ################# quit_game function #################
    # This function enables the program to finish and exit
    def quit_game(self):
        self.running = False # this causes exiting code to be performed


    ############# change_difficulty function #############
    # This function enables the program to swap into the CHANGE_DIFFICULTY state
    def change_difficulty(self):
        self.state = "CHANGE_DIFFICULTY" # update game state


    ################ toggle_hints function ###############
    # This function swaps the hints_button's primary and background colors,
    # updates the hints_enabled variable, and resets any conflicting cells
    # (since the grid is no longer selected)
    def toggle_hints(self):
        temp_color = self.hints_button.color # temporary variable
        # swap the button's color with its background color
        self.hints_button.color = self.hints_button.background_color
        # change the button's background color to equal its original color
        self.hints_button.background_color = temp_color
        # toggle hints_enabled value
        self.hints_enabled = not self.hints_enabled
        self.conflicting_cells = [] # reset conflicting cells


    ################ toggle_notes function ###############
    # This function swaps the notes_button's primary and background colors
    def toggle_notes(self):
        tempColor = self.notes_button.color # temporary variable
        # swap the button's color with its background color
        self.notes_button.color = self.notes_button.background_color
        # change the button's background color to equal its original color
        self.notes_button.background_color = tempColor
        # toggle notes_enabled value
        self.notes_enabled = not self.notes_enabled


    ################# show_solve function ################
    # This function prepares the Sudoku board to be solved by removing any
    # incorrect cells, adding the user's correct cells into a seperate list,
    # and resetting the conflicting cells and the notes lists. It then solves
    # the Sudoku by using the show_backtrack function. Once that is done, the
    # function then empties the pygame events queue, changes the game state to
    # FINISHED, updates the appropriate variables, and finally calculates the
    # total time that it took to solve the Sudoku.
    def show_solve(self):
        # Prepare the board to be solved:
        # Removing all of the incorrect cells from the sudoku_board prevents the
        # backtracking algorithm from trying to solve an un-solvable Sudoku
        # board.
        self.remove_incorrect_cells()
        # Add cells (if any) with the correct values to the correct_cells list
        # (this excludes any locked cells)
        self.add_correct_cells()
        self.conflicting_cells = [] # reset conflicting_cells list
        # reset notes list
        self.notes = [[[False for x in range(ROWS)] for y in range(COLS)]
         for z in range(NUMS)]
        self.solving_board  = True # update variable
        self.show_backtrack(self.sudoku_board) # solve the Sudoku
        pygame.event.clear() # clear events
        self.state = "FINISHED" # change game state
        # reset variables that are no longer needed
        self.solving_board  = False
        self.selected = None
        # get the end time for solving the sudoku
        self.update_time() # update the elapsed time one final time
        self.end_time = self.elapsed_time # assign the total end time
################################################################################



############################ NOTE-RELATED FUNCTIONS ############################

    ################ remove_notes function ################
    # This function removes a note from its surrounding row, column, and
    # subgrid. This function is called whenever the user inputs a value into
    # the Sudoku board.
    def remove_notes(self, pos, val):
        # remove all notes from cell
        for num in range(NUMS):
            self.notes[pos[0]][pos[1]][num] = False
        # remove note from row
        for i in range(ROWS):
            if self.notes[pos[0]][i][val]:
                self.notes[pos[0]][i][val] = False
        # remove note from column
        for i in range(COLS):
            if self.notes[i][pos[1]][val]:
                self.notes[i][pos[1]][val] = False
        # remove note from subgrid
        # start at the beginning of the subgrid
        row_delta = pos[0] - (pos[0] % SUBGRID_WIDTH)
        col_delta = pos[1] - (pos[1] % SUBGRID_HEIGHT)
        # iterate through subgrid and remove the note from each cell (if it
        # is present in that cell)
        for row in range(row_delta, row_delta + SUBGRID_WIDTH, 1):
            for col in range(col_delta, col_delta + SUBGRID_HEIGHT, 1):
                if self.notes[row][col][val]:
                    self.notes[row][col][val] = False


    ################# show_notes function ################
    # This function displays all of the notes on the window
    def show_notes(self, window):
        # iterate through each cell and display any notes that are present
        for x, row in enumerate(self.notes):
            for y, col in enumerate(row):
                for note_index, val in enumerate(col):
                    # only display enabled notes (value will be True)
                    if val != False:
                        # When displaying values to the window, remember to swap
                        # the x and y order to show them in the correct place.
                        pos = [(y * CELL_SIZE) + GRID_POS[0],
                         (x * CELL_SIZE) + GRID_POS[1]]
                        # draw the note on the window (since indices are
                        # 0-based, make sure to add 1 to the note_index to get
                        # the actual number that should be displayed)
                        self.draw_note(window, note_index + 1, OFF_BLACK, pos)

    ################# draw_note function #################
    # This function draws an individual note on the window. Each note can be
    # in 1 of 9 possible positions, so I make sure to add in the appropriate
    # offset value depending on which note was passed into the function
    def draw_note(self, window, val, color, pos):
        font = self.notes_font.render(str(val), True, color) # note font
        # divide the cell into 9 pieces (9 possible values)
        width = (CELL_SIZE - font.get_width())//9
        height = (CELL_SIZE - font.get_height())//9
        # add the correct offset to the value being displayed
        # Each cell has three values displayed in the top (1-3), three values
        # displayed in the middle (4-6), and three values displayed in the
        # bottom (7-9). I also subtract 1 from the value and perform a modulus
        # of three on that value so that I can position the note value
        # accordingly within those groupings of three (left, middle, or right)
        pos[0] += width + ((CELL_SIZE//3) * ((val-1)%3)) + NOTES_PADDING
        pos[1] += height + ((CELL_SIZE//3) * (((val-1)//3)%3)) - NOTES_PADDING
        window.blit(font, pos) # blit the number to the window
################################################################################



############################ CELL-RELATED FUNCTIONS ############################

    ############# reset_locked_cells function ############
    # This function resets all of the locked cells. It is called whenever a
    # new game is created.
    def reset_locked_cells(self):
        self.locked_cells = [] # reset locked_cells list
        self.correct_cells = [] # reset correct_cells list
        # Initialize the locked cells from the given sudoku_board
        for x, row in enumerate(self.sudoku_board):
            for y, val in enumerate(row):
                if val != 0:
                    self.locked_cells.append([x, y]) # add index to list


    ########### remove_incorrect_cells function ##########
    # This function removes any incorrect cells that the user has input into
    # the sudoku board. It is important to remove any incorrect cells from the
    # board before running the backtracking algorithm on it, otherwise the
    # board would be unsolvable and it would be a waste of time trying to solve
    # the board using backtracking
    def remove_incorrect_cells(self):
        # iterate through the sudoku_board and remove incorrect values
        for x, row in enumerate(self.sudoku_board):
            for y, val in enumerate(row):
                if val != self.finished_board[x][y]:
                    self.sudoku_board[x][y] = 0 # remove incorrect value


    ############# add_correct_cells function #############
    # This function adds any correct cells into the correct_cells list. I use
    # the correct_cells list when solving the board to show the user the correct
    # cells that they input into the Sudoku board.
    def add_correct_cells(self):
        # iterate through the sudoku_board and add correct indexes into the list
        for x, row in enumerate(self.sudoku_board):
            for y, val in enumerate(row):
                if [x, y] not in self.locked_cells and val != 0:
                    self.correct_cells.append([x, y]) # add index to list

    ######### update_conflicting_cells function ##########
    # This function updates any conflicting cells that are present when the
    # user inputs a value into the Sudoku board.
    def update_conflicting_cells(self, value):
        self.conflicting_cells = [] # reset conflicting cells
        # make sure value is greater than 0
        if value != 0:
            # check row for conflicting value
            for i in range(ROWS):
                # add conflicting cell index to list (if a conflict exists)
                if self.sudoku_board[self.selected[0]][i] == value and [
                 self.selected[0], self.selected[1]] != [self.selected[0], i]:
                    self.conflicting_cells.append([self.selected[0], i])
            # check column for conflicting values
            for i in range(COLS):
                # add conflicting cell index to list (if a conflict exists)
                if self.sudoku_board[i][self.selected[1]] == value and [
                 self.selected[0], self.selected[1]] != [i, self.selected[1]]:
                    self.conflicting_cells.append([i, self.selected[1]])
            # start at the first cell in the subgrid
            row_delta = self.selected[0] - (self.selected[0] % SUBGRID_WIDTH)
            col_delta = self.selected[1] - (self.selected[1] % SUBGRID_HEIGHT)
            # iterate through subgrid and check for conflicting values
            for row in range(row_delta, row_delta + SUBGRID_WIDTH, 1):
                for col in range(col_delta, col_delta + SUBGRID_HEIGHT, 1):
                    # add conflicting cell index to list (if a conflict exists)
                    if self.sudoku_board[row][col] == value and [
                     self.selected[0], self.selected[1]] != [row, col]:
                        self.conflicting_cells.append([row, col])
        else:
            # if the value is zero, then do nothing
            pass


    ################ shade_cells function ################
    # This function shades a list of cells in with a given color
    def shade_cells(self, window, cellList, color):
        # iterate through each index in the list
        for cell in cellList:
            # fill the cell in with the given color
            pygame.draw.rect(window, color, ((cell[1]*CELL_SIZE) + GRID_POS[0],
             (cell[0] * CELL_SIZE) + GRID_POS[1], CELL_SIZE, CELL_SIZE))


    ############ shade_selected_cell function ############
    # This function shades the selected cell in with a given color
    def shade_selected_cell(self, window, pos, color):
        # When highlighting the selected cell, remember to swap
        # the x and y position values to highlight the correct cell.
        # fill the cell in with the given color
        pygame.draw.rect(window, color, ((pos[1] * CELL_SIZE) + GRID_POS[0],
         (pos[0] * CELL_SIZE) + GRID_POS[1], CELL_SIZE, CELL_SIZE))


    ########## shade_surrounding_cells function ##########
    # This function shades in the surrounding row, column, and subgrid  of the
    # selected cell with a given color
    def shade_surrounding_cells(self, window, pos, color):
        # shade in the surrounding row
        for i in range(ROWS):
            # remember to swap the x and y position values to get the position
            # of the correct cell.
            pygame.draw.rect(window, color, ((i * CELL_SIZE) + GRID_POS[0],
             (pos[0] * CELL_SIZE) + GRID_POS[1], CELL_SIZE, CELL_SIZE))
        # shade the surrounding column
        for i in range(COLS):
            # remember to swap the x and y position values to get the position
            # of the correct cell.
            pygame.draw.rect(window, color, ((pos[1] * CELL_SIZE) + GRID_POS[0],
             (i * CELL_SIZE) + GRID_POS[1], CELL_SIZE, CELL_SIZE))
        # start at the first cell in the subgrid
        row_delta = pos[1] - (pos[1] % SUBGRID_WIDTH)
        col_delta = pos[0] - (pos[0] % SUBGRID_HEIGHT)
        # iterate through subgrid and shade each cell
        for row in range(row_delta, row_delta + SUBGRID_WIDTH, 1):
            for col in range(col_delta, col_delta + SUBGRID_HEIGHT, 1):
                # remember to swap the x and y position values to get the
                # position of the correct cell.
                pygame.draw.rect(window, color, ((row * CELL_SIZE)+ GRID_POS[0],
                 (col * CELL_SIZE) + GRID_POS[1], CELL_SIZE, CELL_SIZE))
################################################################################



############################### HELPER FUNCTIONS ###############################

    ################## is_int function ###################
    # This simple function just tries to convert a character value into an
    # integer. If it is successful, the function returns True, otherwise it
    # returns False.
    def is_int(self, char_val):
        try:
            int(char_val) # try to convert character into an integer
            return True # if successful, return True
        except:
            return False # if unsuccessful, return False


    ################ is_finished function ################
    # This function checks to see if the Sudoku board is finished. It achieves
    # this by comparing the sudoku_board values to the finished_board values.
    def is_finished(self):
        # iterate through the sudoku_board
        for x, row in enumerate(self.sudoku_board):
            for y, val in enumerate(row):
                # make sure that the values are identical
                if val != self.finished_board[x][y]:
                    return False # if they are not then return False
        # the end of the array has been reached, so that means that both of
        # them are identical (return True to signal that the board is finished)
        return True


    ############### mouse_on_grid function ###############
    # This function checks whether the mouse was clicked inside of the Sudoku
    # grid.
    def mouse_on_grid(self):
        if self.mouse_pos[0] < GRID_POS[0] or self.mouse_pos[1] < GRID_POS[1]:
            return False
        if self.mouse_pos[0] > (GRID_POS[0] + GRID_SIZE) or self.mouse_pos[1]> (
         GRID_POS[1] + GRID_SIZE):
            return False
        # The only remaining option is that the user clicked inside the
        # sudoku_board. Remember that when using a mouse, the result is flipped
        # with respect to the sudoku_board (the y value is given first and then
        # the x value), so to get the right sudoku_board index, simply return
        # in the correct format.
        return ((self.mouse_pos[1] - GRID_POS[1])//CELL_SIZE,
         (self.mouse_pos[0] - GRID_POS[0])//CELL_SIZE)


    ############### is_solvable function ###############
    # This function makes sure that the Sudoku board is solvable by making sure
    # that there are no conflicts between the locked cells. This function is
    # called right after a Sudoku board is created to make sure that it is
    # solvable. This prevents the backtracking algorithm from running into any
    # issues when trying to solve the Sudoku recursively.
    def is_solvable(self, board):
        for cell in self.locked_cells:
            if self.conflict_detected(cell[0], cell[1],
             board[cell[0]][cell[1]], board):
                return False
        # The end of the list has been reached and no conflicts have been
        # detected (return True).
        return True
################################################################################



############################### DRAWING FUNCTIONS ##############################

    ################ draw_numbers function ###############
    # This function draws each Sudoku value on the window
    def draw_numbers(self, window):
        # iterate through the Sudoku board
        for x, row in enumerate(self.sudoku_board):
            for y, num in enumerate(row):
                # make sure that the value is not 0
                if num != 0:
                    # When displaying values to the window, remember to swap
                    # the x and y order to show them in the correct place.
                    pos = [(y * CELL_SIZE) + GRID_POS[0],
                     (x * CELL_SIZE) + GRID_POS[1]]
                    # select the appripriate color for the number (locked cells
                    # will always have black numbers)
                    if [x, y] in self.locked_cells or not self.hints_enabled:
                        color = BLACK
                    else:
                        # if hints are enabled, then make the color blue if the
                        # value is correct and red if it is incorrect
                        color = BLUE if (self.finished_board[x][y]==
                         num) else RED
                    # blit the value to the window
                    self.draw_text(window, str(num), color, pos)


    ################# draw_text function
    # This function draws a single Sudoku value on the screen in a specified
    # color.
    def draw_text(self, window, text, color, pos):
        font = self.font.render(text, True, color) # value font
        # get the center of the cell
        pos[0] += (CELL_SIZE - font.get_width())//2
        pos[1] += (CELL_SIZE - font.get_height())//2
        window.blit(font, pos) # blit value to window


    ################# draw_grid function #################
    # This function draws the Sudoku board grid (the gameboard outline and
    # the internal boxes that make up a Sudoku board)
    def draw_grid(self, window):
        # blit the outline of the game board to the window
        pygame.draw.rect(window, BLACK, (GRID_POS[0], GRID_POS[1], GRID_SIZE,
         GRID_SIZE), 2)
        # blit all of the internal lines on the Sudoku board to the window
        for x in range(ROWS):
            # draw vertical lines on the window
            pygame.draw.line(window, BLACK,
             (GRID_POS[0] + (x * CELL_SIZE), GRID_POS[1]),
             (GRID_POS[0] + (x * CELL_SIZE), GRID_POS[1] + 450),
             (1 if (x % 3 != 0) else 2))
            # draw horizontal lines on the window
            pygame.draw.line(window, BLACK,
             (GRID_POS[0], GRID_POS[1] + (x * CELL_SIZE)),
             (GRID_POS[0] + 450, GRID_POS[1] + (x * CELL_SIZE)),
             (1 if (x % 3 != 0) else 2))
################################################################################



############################ BOARD-RELATED FUNCTIONS ###########################

    ########## populate_finished_board function ##########
    # This function resets the finished board and copies over the new Sudoku
    # board values. It is called whenever a new game is created so that the
    # finished board can be updated accordingly.
    def populate_finished_board(self, board):
        # reset finished board array
        self.finished_board = [[0 for x in range(ROWS)] for x in range(COLS)]
        # perform a deep copy of the sudoku_board to the finished_board
        for x, row in enumerate(self.sudoku_board):
            for y, val in enumerate(row):
                # copy each index value so they can be altered independently
                self.finished_board[x][y] = self.sudoku_board[x][y]
        # solve the board and update the finished_board accordingly
        if self.backtrack(self.finished_board):
            print(f"Solution: {self.finished_board}")
        else:
            print("Error solving board")


    ############## get_sudoku_board function #############
    # This function performs some web scraping in order to retrieve a Sudoku
    # board from https://nine.websudoku.com.
    def get_sudoku_board(self, difficulty):
        # difficulty needs to be parsed in as a string with one digit. 1-4
        html_doc = requests.get("https://nine.websudoku.com/?level={}".format(
         difficulty)).content
        # parse the contents of the webpage into a readable/retrievable format
        soup = BeautifulSoup(html_doc, "html.parser")
        # id names that are used in the website
        ids = ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08',
               'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18',
               'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28',
               'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38',
               'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48',
               'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58',
               'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68',
               'f70', 'f71', 'f72', 'f73', 'f74', 'f75', 'f76', 'f77', 'f78',
               'f80', 'f81', 'f82', 'f83', 'f84', 'f85', 'f86', 'f87', 'f88']
        data = [] # empty list which will be populated with the index values
        # iterate through the list of ids
        for id_val in ids:
            data.append(soup.find('input', id=id_val)) # add id_value into list
        # initialize and empty board to have all 0 values
        board = [[0 for x in range(ROWS)] for i in range(COLS)]
        # substitute in non-zero id values into the board
        for index, cell in enumerate(data):
            try:
                # parse the cell value into the board
                board[index//ROWS][index % COLS] = int(cell['value'])
            except:
                pass
        self.sudoku_board =  board # assign the new sudoku board
        self.reset_locked_cells() # reset the locked_cells list
        # reset the notes list
        self.notes = [[[False for x in range(ROWS)] for y in range(COLS)]
         for z in range(NUMS)]
        # reset conflicting cells
        self.conflicting_cells = []
        # make sure that the board is is_solvable
        if self.is_solvable(self.sudoku_board):
            # reinitialize the finished board and solve it
            self.populate_finished_board(self.sudoku_board)
        else:
            # if the board isn't solvable, then retrieve another Sudoku
            print("An error occured... Let me try to get a different board")
            self.get_sudoku_board(difficulty)

################################################################################



############################ BACKTRACKING ALGORITHM ############################

    ################# check_row function #################
    # This function checks to see if there are any conflicting row values
    def check_row(self, row, col, value, board):
        # check row for conflicting value
        for i in range(ROWS):
            # make sure to skip the index that is being checked against.
            if i != col:
                # check if the values are equal to each other (make sure
                # that only non-zero values are compared together)
                if value != 0 and board[row][i] == value:
                    # return True if the value appears in the same column
                    return True
        # no conflicting value detected, return False
        return False


    ################# check_col function #################
    # This function checks to see if there are any conflicting column values
    def check_col(self, row, col, value, board):
        # check column for conflicting values
        for i in range(COLS):
            # make sure to skip the index that is being checked against.
            if i != row:
                # check if the values are equal to each other (make sure
                # that only non-zero values are compared together)
                if value != 0 and board[i][col] == value :
                    # return True if the value appears in the same column
                    return True
        # no conflicting value detected, return False
        return False


    ############### check_subgrid function ###############
    # This function checks to see if there are any conflicting subgrid values
    def check_subgrid(self, row, col, value, board):
        # start at the first cell in the subgrid
        row_delta = row - (row % SUBGRID_WIDTH)
        col_delta = col - (col % SUBGRID_HEIGHT)
        # iterate through subgrid and check for conflicting values
        for r in range(row_delta, row_delta + SUBGRID_WIDTH, 1):
            for c in range(col_delta, col_delta + SUBGRID_HEIGHT, 1):
                # make sure to skip the index that is being checked against.
                if r != row and c != col:
                    # check if the values are equal to each other (make sure
                    # that only non-zero values are compared together)
                    if value != 0 and board[r][c] == value:
                        # return True if the value appears in the same subgrid
                        return True
        # no conflicting value detected, return False
        return False


    ############# conflict_detected function #############
    # This function checks to see if there are any conflicting values in the
    # surrounding row, column, or subgrid. If there are any conflicting values,
    # the function returns True. If there aren't any conflicting values, then
    # the function returns False.
    def conflict_detected(self, row, col, value, board):
        # check row, column, and subgrid for conflicting values
        return (self.check_row(row, col, value, board)
         or self.check_col(row, col, value, board)
         or self.check_subgrid(row, col, value, board))


    ################ backtrack function ################
    # This function performs the backtracking algorithm in order to solve the
    # provided Sudoku board. The backtracking algorithm iterates as far as
    # possible down one path until the board can no longer be solved. When it
    # reaches this point, it then backtracks to a previous point and then takes
    # a different path. This process repeats itself until the algorithm is able
    # to sucessfully complete the board.
    def backtrack(self, board):
        # iterate through the whole board
        for row in range(ROWS):
            for col in range(COLS):
                # make sure the space is empty
                if board[row][col] == 0:
                    # space is empty; plug in values (1-9) and try to solve
                    # the board.
                    for val in range (1, NUMS + 1, 1):
                        # make sure there are no conflicting values
                        if not self.conflict_detected(row, col, val, board):
                            board[row][col] = val # assign value to board
                            # iterate to next spot and continue trying to solve
                            # the Sudoku if no conflicts are detected
                            if self.backtrack(board):
                                return True
                            else :
                                # reset cell (backtrack) and try the next value
                                board[row][col] = 0;
                    # not possible to solve Sudoku using this iteration, so
                    # return false
                    return False
        # The end of the Sudoku has been reached, make sure that there are no
        # conflicts on the whole Sudoku and return the result.
        solved_successfully = True
        for row in range(ROWS):
            for col in range(COLS):
                # check if there is a conflict
                if self.conflict_detected(row, col, board[row][col], board):
                    solved_successfully = False
                    break
        return solved_successfully


    ############## show_backtrack function #############
    # This function performs the backtracking algorithm in order to solve the
    # provided Sudoku board. The only difference between this function and the
    # backtrack function above is that the show_backtrack function shows the
    # Sudoku being solved along the way. I could have added this functionality
    # to the backtrack function, but I figured that it didn't really make
    # sense to make that function more inefficient than it needed to be. This is
    # more of a niche case where I wanted to see firsthand what was going on
    # while the backtracking algorithm was at work. The backtracking algorithm
    # iterates as far as possible down one path until the board can no longer be
    # solved. When it reaches this point, it then backtracks to a previous point
    # and then takes a different path. This process repeats itself until the
    # algorithm is able to sucessfully complete the board.
    def show_backtrack(self, board):
        # I get pygame's events in this function to allow the user to quit the
        # program while the show_backtrack function is running. I also do this
        # because if you fail to make a call to the event queue for too long,
        # the system may decide your program has locked up, which causes the
        # program to become unresponsive. This prevents that from happening.
        # iterate through each pygame event
        for event in pygame.event.get():
            # exit the program if the user wants to quit
            if event.type == pygame.QUIT:
                pygame.quit() # quit pygame
                sys.exit() # exit the program
        # iterate through the whole board
        for row in range(ROWS):
            for col in range(COLS):
                # check if space is empty
                if board[row][col] == 0:
                    # space is empty; plug in values (1-9) and try to solve
                    # the board.
                    for val in range (1, NUMS + 1, 1):
                        # make sure there are no conflicting values
                        if not self.conflict_detected(row, col, val, board):
                            board[row][col] = val # assign value to board
                            self.playing_draw() # draw the playing state screen
                            self.clock.tick(30) # perform a small delay
                            # iterate to next spot and continue trying to solve
                            # the Sudoku if no conflicts are detected
                            if self.show_backtrack(board):
                                return True
                            else :
                                # reset cell (backtrack) and try the next value
                                board[row][col] = 0;
                    # not possible to solve sudoku using this iteration, so
                    # return false
                    return False
                else:
                    # space isn't empty, so check to see if there are any
                    # conflicts so far.
                    if self.conflict_detected(row, col, board[row][col], board):
                        return False
        # The end of the board has been reached, make sure that there are no
        # conflicts on the whole board and return the result.
        solved_successfully = True
        for row in range(ROWS):
            for col in range(COLS):
                # check if there is a conflict
                if self.conflict_detected(row, col, board[row][col], board):
                    solved_successfully = False
                    break
            if not solved_successfully:
                break
        return solved_successfully

################################################################################

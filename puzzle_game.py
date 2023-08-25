'''
    Kerry Owusu
    CS5001, Fall 2022
    Final Project: Puzzle Game

    Screen set up
    
'''

import turtle
import time 
import math
import PositionService # can potentially delete
import random
import logging

from pathlib import Path
import os


#initialization of general turtle and screen
cursor = turtle.Turtle()
screen = turtle.Screen()
screen.listen() # hears the clicks that we do on our end



# initiation of specialized turtles 
t_moves = turtle.Turtle() # updates player moves text
t_thumbnail = turtle.Turtle() # places thumbnail corresponding to puzzle
t_lose = turtle.Turtle() # showcases lose.gif when someone loses game
t_win = turtle.Turtle() # showcases winner.gif when someone wins game
t_2dlist = turtle.Turtle() 
t_leaderboard = turtle.Turtle()




# the creation of global lists for access of data throughout all functions
turtle_pieces_list, square_list, coordinate_two_d, puzzle_board, turtle_list_two_d = [], [], [], [], []

turtle_list = [] # holds .puz turtle objects
list_of_turtles_sol = [] # holds .puz turtle objects in order of solved puzzle
turtle_list_solution = [] # holds .puz turtle objects in order of solved puzzle
puzzle_board_sol = [] # holds 1  to {number of tiles in a given puzzle}
turtle_list_solution_two_d = [] # a 2D list that contains the turtle objects .puz images
leaderboard_list = [] # list that contains the game winners



# variable initialization for access of variables throughout all functions
chances = 0 # variable of the maximum moves a player needs to make to win a game
moves = 0 # initialization of the number of player moves
name = None # initialization of the input name



# initialization of the creation of the error file and error file format
logging.basicConfig(format='%(asctime)s : %(levelname)s - %(message)s', datefmt= '%m/%d/%Y %I:%M:%S %p', level=logging.ERROR, filename="5001_puzzle.err")
formatter = logging.Formatter('%(asctime)s : %(levelname)s - %(message)s')



                              
def screen_opener():
    '''
    Function -- screen_opener
        Functions as the introduciton to the Puzzle Game. This function
        initializes turtle screen, adds the splash screen gif and
        prompts the user to input name and enter the chances/moves
        they would like to have for each puzzle game.
    Parameters: None
    '''

    global cursor
    global chances
    global name

    # set up screen size 
    screen = turtle.Screen()
    screen.listen() # helps take in stuff from board
    screen.setup(900, 800)


    # creation of new turtle 
    cursor = turtle.Turtle()

    # adds and erases splash screen gif from screen
    screen.addshape("Resources/splash_screen.gif")
    cursor.shape("Resources/splash_screen.gif")
    time.sleep(3) # splash screen stays on screen for 3 seconds
    screen.clear() # splash screen disappears
    


    # creation of name input prompt and number of chances input prompt
    name = screen.textinput("CS5001 Puzzle Slide", "Name")
    chances = screen.numinput("5001 Puzzle Slide - Moves", "Enter the number of moves (chances) you want (5-200)?", minval=5, maxval=200)
    
        
    
    

    
def play_method(turtle_pieces_list, square_list, coordinate_two_d, puzzle_board, length,
                num_of_tiles, turtle_list_two_d, menu="mario.puz"): 
    '''
    Function -- play_method
        The outer (enclosing) function that retains its state and can share data
        to the button_functionality_clicked nested function. This function allows
        the nested function to have access to various lists returned throughout
        the program.
    Parameters:
        turtle_pieces_list: a list that contains the .puz gif image turtle objects
            returned from function, draw_shuffled_squares 
        square_list: a list (returned from draw shuffled squares) containing turtles that creates a square
            that encloses the puzzle tiles
        coordinate_two_d: a 2D list (cooresponding to puzzle board size) that contains the coordinate
            placement of each turtle in turtle_pieces_list (the list containing the turtle objects of
            gif .puz images
        puzzle_board: a 2D list that contains the shuffled or ordered numbers from
            1 to # of tiles for a given puzzle.
        length: the length of one side of a puzzle tile 
        num_of_tiles: the number of tiles in a given puzzle (int)
        turtle_list_two_d: a list containing the puzzle piece gif image turtles in the
            2D form
        menu: the name of the .puz file
    '''
    def button_functionality_clicked(x_coord, y_coord): # for us to see where we are clicking, don't necessarily need at the end
        '''
        Function -- button_functionality_clicked
            A nested function that stores all the results of a click and
            allows the puzzle board game when a user clicks
            the reset, load or quit game buttons.
        Parameters:
            x_coord: the X-coordinate of the the clicked position
                from user
            y_coord: the Y-coordinate of the clicked position
                from user
        '''
        # global variables that allow for change in data when reset and load are clicked 
        global cursor
        global screen
        global chances
        global moves, t_moves
        global t_2dlist
        global turtle_pieces_list, square_list, coordinate_two_d, puzzle_board, turtle_list_two_d

        # creation of a new turtle for quit message gif image palcement
        cursor2 = turtle.Turtle()
        cursor2.pencolor("white")
        screen = turtle.Screen() 


        # the nonlocal variables utilized in code from outer function
        nonlocal length
        nonlocal num_of_tiles
        nonlocal menu
        
        

        # the parameters of the quit button, if clicked quits/exits game
        if (273.0 <= x_coord <= 346.0) and (-304.0 >= y_coord >= -346.0): # QUIT button
            try: 
                # quit message appears on board if clicked in coordinates
                screen.addshape("Resources/quitmsg.gif") 
                cursor2.shape("Resources/quitmsg.gif")
                time.sleep(3)
                # screen.bye()
                quit()
            except IOError: # added exception in case errors arise that inhibit game exit
                logging.error(f'Error message arose when exiting game. LOCATION: Game.play_method()')
                screen.addshape("Resources/quitmsg.gif") # quit message appears on screen
                cursor2.shape("Resources/quitmsg.gif")
                time.sleep(3)
                screen.bye() # screen exits game
                # quit()

                
        if (178.0 < x_coord < 251.0) and (-359.0 < y_coord < -290.0): # LOAD button coordinate parameters
            
            # initialization of flag variable
            flag = False
            while flag == False:
                
                # retrieves the .puz file names that are in the same directory as puzzle_game.py file
                puzzle_names, puzzle_file_names = get_menu() 

                # displays list of puzzles for user to choose if clicks load button
                menu = screen.textinput(f"Load Puzzle",
                                        f"Enter the name of the puzzle you wish to load. Choices are:\n"
                                        f"{puzzle_names}")
                                      
                # ensures that 
                if menu[-4:] == '.puz':
                    try:
                        for each in turtle_list: #erases current turtles on turtle board
                            #each.reset()
                            each.clear()
                            each.hideturtle()
                        for each in square_list: # erases current square drawings
                            each.hideturtle()
                            each.clear()
                        length, num_of_tiles = open_puz_files(f"{menu}") # opens selected puzzle for game
                        

                        # initialization of variable to check to see if .puz file is not malformed 
                        check = is_perfect_square(num_of_tiles)
                        
                        
                        # if number of tiles in .puz file is invalid will prompt user to reenter valid puzzle
                        if check == False:
                            logging.error(f'File {menu} is malformed. LOCATION: Game.play_method()')
                            screen.addshape('Resources/file_error.gif')
                            t_2dlist.shape('Resources/file_error.gif')
                            time.sleep(4)
                            t_2dlist.hideturtle()
                            flag = False
                            continue 

                     
                        meta_dict, puz_pieces_dict = make_dictionary(f"{menu}")
                        turtle_list.clear() # erases elements in turtle list
                        square_list.clear() 
                        
                        # draws squares places tiles on puzzle board for chosen puzzle, creates lists corresponding to turtles, turtle location and square placement
                        turtle_pieces_list, square_list, coordinate_two_d, puzzle_board, turtle_list_two_d = draw_shuffled_squares(length, num_of_tiles, puz_pieces_dict)
                        thumbnail_pic = menu[:-4]
                        thumbnail_placement(f"Images/{thumbnail_pic}/{thumbnail_pic}_thumbnail.gif")

                        # turtle that writes player moves on the board after each puzzle move
                        t_moves.clear()
                        t_moves.penup()
                        t_moves.goto(-300, -350)
                        t_moves.pendown()
                        moves = 0
                        desired_text = "Player moves:{}".format(moves)
                        t_moves.write(desired_text, align="left", font=('Arial', 20, 'bold'))
                        
                        flag = True # prevents infinite while loop

                    # if invalid puzzle choice is inputted by user, user will be reprompted to choose valid puzzle    
                    except FileNotFoundError:
                        logging.error(f'File {menu} does not exist. LOCATION: Game.play_method()')
                        screen.addshape("Resources/file_error.gif") # file error gif appears on screen
                        cursor2.shape("Resources/file_error.gif")
                        time.sleep(3)
                        cursor2.hideturtle()
                        flag = False

                # will raise error if user's file input is invalid    
                else:
                    logging.error(f'File {menu} does not exist. LOCATION: Game.play_method()')
                    screen.addshape("Resources/file_error.gif") # file error gif appears on screen
                    cursor2.shape("Resources/file_error.gif")
                    time.sleep(3)
                    cursor2.hideturtle()
                    flag = False

                    
        # parameters of the reset button           
        if (72.0 < x_coord < 158.0) and (-357.0 < y_coord < -287.0): # RESET button
            if menu == "":
                
                reset_botton()
            else:
                # the selected puzzle that the user chooses loads on to the board when reset button is clicked
                turtle_pieces_list, square_list, coordinate_two_d, puzzle_board, turtle_list_two_d, length, num_of_tiles = reset_botton(menu)
                
                
            
        # runs the puzzle game 
        puzzle_functionality_clicked(x_coord, y_coord, length, num_of_tiles, coordinate_two_d,
                                     puzzle_board, turtle_list_two_d)
        
        
    # registers screen clicks    
    turtle.onscreenclick(button_functionality_clicked)
           


def get_menu():
    '''
    Function -- get_menu:
        This function retrieves the file names of the files ending in
        .puz that are in the same directory as puzzle_game.py file
    Parameters: None
    Returns: a string containing all of the puzzle names, a list
        containing all of the puzzle names

    '''
    puzzle_file_names = []
    for file in os.listdir():
        if file.endswith(".puz"):
            puzzle_file_names.append(file)

    puzzle_names = '\n'.join(puzzle_file_names)
    return puzzle_names, puzzle_file_names

def is_perfect_square(num_of_tiles):
    '''
    Function -- is_perfect_square:
        This function utilizes the math module to detect whether
        a number is a perfect square. Returns a boolean True if a
        number is perfect square and boolean False if number is
        not a perfect square
    Parameter:
        num_of_tiles: integer
    Returns:
        A boolean (True or False)
        
    '''

    root = math.sqrt(num_of_tiles)

    if int(root + 0.5) ** 2 == num_of_tiles:
        return True
    else:
        return False


def leaderboard():
    '''
    Function -- leaderboard
        This function updates and sorts the name and scores on the
        leaderboard
    Parameters: None
    '''
    
    # global turtles
    global t_leaderboard
    global leaderboard
    global name, moves
    t_leaderboard2 = turtle.Turtle()
    
    try:
        # opens and reads the leaderboard.txt file
        with open("leaderboard.txt", mode='r') as outfile:
            x, y = 140, 230
            for line in outfile:
                # ensures to only gather score, name information from txt file
                if line[0].isdigit() == False: 
                    continue
                else:
                    leaderboard_list.append(line.split(":")) # creates a leaderboard list from data from leaderboard.txt file
                    leaderboard_list.sort(key = lambda x: int(x[0])) # sorts the list based off of score (lower score first in list)
        with open("leaderboard.txt", mode='w') as outfile: # creating a new sorted leaderboard.txt file 
            for sublist in leaderboard_list: # version 2 possibly make a que
                line = "{}:{}\n\n".format(sublist[0], sublist[1]) 
                outfile.write(line) # overwrite old file and create a new sorted leaderboard.txt file
        
                write_text(f"{line}", x, y) # write on leaderboard
                y -= 30 # ensures that the words aren't written at same coordinate
            
        leaderboard_list.clear() # empties the list

    except FileNotFoundError: # if leaderboard .txt file isn't in same root at .py file, will alert user with error gif
        logging.error(f'File leaderboard.txt not found. LOCATION: Game.play_method()')
        screen.addshape("Resources/leaderboard_error.gif")
        t_leaderboard2.shape("Resources/leaderboard_error.gif")
        time.sleep(3)
        t_leaderboard2.hideturtle()
        
   

def reset_botton(puz_file_name="mario.puz"):
    '''
    Function -- reset_botton
        This function takes care of resetting the puzzle board by
        placing the puzzle pieces in order for the user to see the
        solution.
    Parameters:
        puz_file_name: the name of the puzzle file (string)
    Returns:
        turtle_pieces_list: a list that contains the .puz gif image turtle objects
        square_list: a list containing turtles that creates a square
            that encloses the puzzle tiles
        coordinate_two_d: a 2D list (cooresponding to puzzle board size) that contains the coordinate
            placement of each turtle in turtle_pieces_list (the list containing the turtle objects of
            gif .puz images
        puzzle_board: a 2D list that contains the shuffled or ordered numbers from
            1 to # of tiles for a given puzzle.
        length: the length of one side of a puzzle tile (int)
        num_of_tiles: the number of tiles in a given puzzle (int)
        turtle_list_two_d: a list containing the puzzle piece gif image turtles in the
            2D form
    '''
    
    global turtle_pieces_list, square_list, coordinate_two_d, puzzle_board, turtle_list_two_d
    global t_moves, moves 
    global puzzle_board_sol, turtle_list_solution, turtle_list_solution_two_d

    # retrieves the length and number of tiles of a puzzle from puzzle file
    length, num_of_tiles = open_puz_files(puz_file_name)
    # creates a dictionary from metadata and data from puzzle file
    meta_dict, puz_pieces_dict = make_dictionary(puz_file_name)
    

    # iterates through turtle list and deletes from list and hides on board
    for each in turtle_list: 
        each.clear()
        each.hideturtle()

    # iterates through square list and deletes currrent data and deletes from board    
    for each in square_list:
        each.clear()
        each.hideturtle()

    #  turtle that writes and updates player moves
    t_moves.clear() # deletes current player moves score
    t_moves.penup()
    t_moves.goto(-300, -350)
    t_moves.pendown()
    moves = 0 # set number of moves made by player back to zero
    desired_text = "Player moves:{}".format(moves) 
    t_moves.write(desired_text, align="left", font=('Arial', 20, 'bold')) # writes player moves: zero

    # draws the sqaures and puts the puzzle pieces back on the board in order, as well as updates global variables
    turtle_pieces_list, square_list, coordinate_two_d, puzzle_board, turtle_list_two_d = draw_solution_squares(length, num_of_tiles, puz_pieces_dict)

    
    for i in range(len(puzzle_board)):
        for j in range(len(puzzle_board[i])):
            puzzle_board_sol.append(puzzle_board[i][j])
            
    for i in range(len(turtle_list_two_d)):
        for j in range(len(turtle_list_two_d[i])):
            turtle_list_solution.append(turtle_list_two_d[i][j])
            
    # creates a two-d turtle list of solution format synonymous to puzzle board 
    turtle_list_solution_two_d = create_two_d_list(turtle_list_solution) 
   
    return turtle_pieces_list, square_list, coordinate_two_d, puzzle_board, turtle_list_two_d, length, num_of_tiles 





def is_winner(turtle_list_two_d, turtle_list_solution_two_d):
    '''
    Function -- is_winner
        This function compares the current global turtle_list_two_d (list
        containing the current state of objects on the puzzle_board) to
        an unchanged turtle_list_solution_two_d and returns a boolean
        True if they are the same, or returns boolean False if they
        are different
    Parameters:
        turtle_list_two_d: a list containing the puzzle piece gif image turtles in the
            2D form
        turtle_list_solution_two_d: a list containing the puzzle piece gif
            image turtles in order in 2D form
    Returns:
        equal: a Boolean True or False
    
    '''
    
    equal = True # initialization of equal variable
    if len(turtle_list_solution_two_d) == 0: # if list is empty, return False
        equal = False
        return equal
    else: 
        for i in range(len(turtle_list_two_d)):
            if turtle_list_two_d[i] != turtle_list_solution_two_d[i]: # compares the lists by indexes
                    equal = False # if the two lists are not equal will return False
                    return equal
            
    return equal



   
def is_blank(puzzle_board: list, coordinate_two_d):
    '''
    Function -- is_blank:
        Function determines where the blank tile is on the puzzleboard
        and returns the coordinate of the blank tile as well as
        the blank tile number (ie the largest number on the puzzleboard)
    Parameters:
        puzzle_board: a 2D list that contains the shuffled or ordered numbers from
            1 to # of tiles for a given puzzle.
        coordinate_two_d: a 2D list (cooresponding to puzzle board size) that contains the coordinate
            placement of each turtle in turtle_pieces_list (the list containing the turtle objects of
            gif .puz images
    Returns:
        blank tile: integer representing the blank tile
        blank_tile_coordinate: (tuple containing the integer coordinates of the blank tile)
    '''

    
    max_num = [max(num) for num in puzzle_board] # finds maximum number in puzzleboard
    blank_tile = max(max_num) # sets blank tile equal to maximum number
    blank_tile_coordinate = None # ininitialization of variable
    
    for i in range(len(puzzle_board)): 
        for j in range(len(puzzle_board[i])): # iterates through each element in puzzleboard
            if puzzle_board[i][j] == blank_tile: # compare each element in puzzle board to blank tile num
                blank_tile_coordinate = coordinate_two_d[i][j] # if found, set blank tile coordinate to variable
    
    return blank_tile, blank_tile_coordinate



def clicked_tile(x_coord, y_coord, coordinate_two_d, length, puzzle_board): 
    '''
    Function -- clicked_tile
        This function detects which tile is clicked by user
    Parameters:
        x_coord: the X-coordinate of the user's click
        y_coord: the Y-coordinate of the user's click
        coordinate_two_d: a 2D list (cooresponding to puzzle board size) that contains the coordinate
            placement of each turtle in turtle_pieces_list (the list containing the turtle objects of
            gif .puz images
        length: the length of each side of a given puzzle piece
        puzzle_board: a 2D list that contains the shuffled or ordered numbers from
            1 to # of tiles for a given puzzle.
    Returns:
        clicked_tile_coordinate: the coordinate of the clicked tile [tuple (x, y)]
        selected_tile: the number in the puzzle_board corresponding to
            clicked tile (int)
    '''
    
    for i in range(len(coordinate_two_d)): # iterate through coordinate_two_d list
        for j in range(len(coordinate_two_d[i])):
            for k in range(len(coordinate_two_d[i][j])): 
                # determines if click is within the area of a puzzle piece 
                if abs(coordinate_two_d[i][j][0] - x_coord) <= length/2 and\
                   abs(coordinate_two_d[i][j][1] - y_coord) <= length/2:
                    clicked_tile_coordinate = coordinate_two_d[i][j] # set clicked coordinate to respective coordinate
                    selected_tile = puzzle_board[i][j] # set selected tile to respective integer representing the clicked puzzle piece
                    
    
    return clicked_tile_coordinate, selected_tile

                    

def is_adjacent(blank_tile_coordinate, clicked_tile_coordinate, length):
    '''
    Function -- is_adjacent
        Function determines if clicked tile is adjacent to blank tile
    Parameters:
        blank_tile_coordinate: coordinate of the blank tile [tuple (x, y)]
        clicked_tile_coordinate: coordinate of the tile that is clicked by user
            [tuple (x, y)]
        length: length of one side of the puzzle piece
    Returns:
        Boolean True if clicked tile is adjacent to blank tile or
        Boolean False if clicked tile is not adjacent to blank tile

    '''
    
    for i in range(len(blank_tile_coordinate)): # iterate through coordinate (x, y) of blank tile
        
        # if distance between clicked & blank tile  x coord is less than or equal to 2 + length, return True
        if abs(blank_tile_coordinate[0] - clicked_tile_coordinate[0]) <= (length + 2) and\
           abs(blank_tile_coordinate[0] - clicked_tile_coordinate[0]) >= ((length/2) + 2):
            
            return True

        # if distance btwn clicked & blank tiles y coord is less than or equal to 2 + length, return True
        elif abs(blank_tile_coordinate[1] - clicked_tile_coordinate[1]) <= (length + 2) and\
             abs(blank_tile_coordinate[1] - clicked_tile_coordinate[1]) >= ((length/2) + 2):
            
            return True
        
        else:
            return False


        
        
def swap_tile(blank_tile, selected_tile, bool_is_adjacent, puzzle_board, turtle_list_two_d, coordinate_two_d):
    '''
    Function -- swap_tile
        Function takes care of horizontal tile swaps on puzzle board.
        The swap can only be initiated if the is_adjacent function
        returns True
    Parameters:
        blank_tile: integer representing the blank tile
        selected tile: the number in the puzzle_board corresponding to
            clicked tile (int)
        bool_is_adjacent: a boolean True if clicked puzzle piece is adjacent to
            blank tile, a boolean False if not adjacent
        puzzle_board: a 2D list that contains the shuffled or ordered numbers from
            1 to # of tiles for a given puzzle.
        turtle_list_two_d: a list containing the puzzle piece gif image turtles in the
            2D form
        coordinate_two_d: a 2D list (cooresponding to puzzle board size) that contains the coordinate
            placement of each turtle in turtle_pieces_list (the list containing the turtle objects of
            gif .puz images
    Returns:
        turtle_list_two_d: updated 2D list that contains the coordinate placement of each
            turtle object (gif puzzle piece images) post horizontal swap
        coordinate_two_d: a 2D list (cooresponding to puzzle board size) that contains the coordinate
            placement of each puzzle piece post horizontal swap

    '''

    # can only enter while loop is clicked tile is adjacent to blank tile
    while bool_is_adjacent == True:
        
        # iterate through puzzle board to retrieve location of blank and selected tile in list
        for i in range(len(puzzle_board)):
            if blank_tile in puzzle_board[i]: # checks which index of nested list (representing puzzle row) that blank tile is in
                blank_tile_index = puzzle_board[i].index(blank_tile)
                if selected_tile in puzzle_board[i]: # if selected_tile in same nested list as blank tile
                    selected_tile_index = puzzle_board[i].index(selected_tile) # assign variable to index of the selected in the nested list
                    
                    # swapping indexes of the blank and selected tile in puzzle_board list
                    puzzle_board[i][blank_tile_index], puzzle_board[i][selected_tile_index] =\
                                                        puzzle_board[i][selected_tile_index], puzzle_board[i][blank_tile_index]

                    # swapping indexes of the blank and selected tile in turtle_two_d list
                    turtle_list_two_d[i][blank_tile_index], turtle_list_two_d[i][selected_tile_index] =\
                                                        turtle_list_two_d[i][selected_tile_index], turtle_list_two_d[i][blank_tile_index]
        
                    
                    # swapping tiles on puzzle board
                    turtle_list_two_d[i][blank_tile_index].penup()
                    turtle_list_two_d[i][selected_tile_index].penup()
                    turtle_list_two_d[i][selected_tile_index].goto(coordinate_two_d[i][selected_tile_index])
                    turtle_list_two_d[i][blank_tile_index].goto(coordinate_two_d[i][blank_tile_index])
                    turtle_list_two_d[i][blank_tile_index].pendown()
                    turtle_list_two_d[i][selected_tile_index].pendown()
                    
                    num_of_moves() # updating player moves 

                    # setting bool_is_adjacent to false to avoid infinite looop
                    bool_is_adjacent = False 
            
            bool_is_adjacent = False 
        bool_is_adjacent = False
        
    return turtle_list_two_d, puzzle_board
           
                

def swap_tile_vertically(blank_tile, selected_tile, bool_is_adjacent, puzzle_board, turtle_list_two_d, coordinate_two_d):
    '''
    Function -- swap_tile_vertically
        This function takes care of vertical tile swaps on puzzle board.
        The swap can only be initiated if the is_adjacent function
        returns True
    Parameters:
        blank_tile: integer representing the blank tile
        selected tile: the number in the puzzle_board corresponding to
            clicked tile (int)
        bool_is_adjacent: a boolean True if clicked puzzle piece is adjacent to
            blank tile, a boolean False if not adjacent
        puzzle_board: a 2D list that contains the shuffled or ordered numbers from
            1 to # of tiles for a given puzzle.
        turtle_list_two_d: a list containing the puzzle piece gif image turtles in the
            2D form
        coordinate_two_d: a 2D list (cooresponding to puzzle board size) that contains the coordinate
            placement of each turtle in turtle_pieces_list (the list containing the turtle objects of
            gif .puz images
    Returns:
        turtle_list_two_d: updated 2D list that contains the coordinate placement of each
            turtle object (gif puzzle piece images) post vertical swap
        coordinate_two_d: a 2D list (cooresponding to puzzle board size) that contains the coordinate
            placement of each puzzle piece post vertical swap        
    '''

    # can only enter while loop is clicked tile is adjacent to blank tile
    while bool_is_adjacent == True:
        
        for i in range(len(puzzle_board)):
            if blank_tile in puzzle_board[i]: # determines which nested list the blank tile resides
                blank_i = i # assign index of nested list to blank_i
                blank_tile_index = puzzle_board[i].index(blank_tile) # assign index within nested list of the blank tile variable
            if selected_tile in puzzle_board[i]: # determines which nested list the selected tile resides
                selected_tile_i = i # assigns index of nested list to variable
                selected_tile_index = puzzle_board[i].index(selected_tile) # assigns index of selected tile within nested list to another variable
                
        # if the indexes of blank and selected tile within their respective nested lists are the same swap indexes
        if blank_tile_index == selected_tile_index: 
            puzzle_board[blank_i][blank_tile_index], puzzle_board[selected_tile_i][selected_tile_index] =\
                                                        puzzle_board[selected_tile_i][selected_tile_index], puzzle_board[blank_i][blank_tile_index]


            turtle_list_two_d[blank_i][blank_tile_index], turtle_list_two_d[selected_tile_i][selected_tile_index] =\
                                                    turtle_list_two_d[selected_tile_i][selected_tile_index], turtle_list_two_d[blank_i][blank_tile_index]
                
            # swapping of tiles on the puzzle board 
            turtle_list_two_d[blank_i][blank_tile_index].penup()
            turtle_list_two_d[selected_tile_i][selected_tile_index].penup()
            turtle_list_two_d[selected_tile_i][selected_tile_index].goto(coordinate_two_d[selected_tile_i][selected_tile_index])
            turtle_list_two_d[blank_i][blank_tile_index].goto(coordinate_two_d[blank_i][blank_tile_index])
                    
            turtle_list_two_d[blank_i][blank_tile_index].pendown()
            turtle_list_two_d[selected_tile_i][selected_tile_index].pendown()
            
            num_of_moves() # update player moves 
            
            
            bool_is_adjacent = False # set bool_is_adjacent to False to prevent infinite while loop
        bool_is_adjacent = False
             
    return turtle_list_two_d, puzzle_board           
     
    
         
def num_of_moves():
    '''
    Function -- num_of_moves
        This function updates the player moves on the board and
        determines if the user wins or loses games based
        on user's input
    Parameters: None
    '''
    
    global t_moves 
    global screen
    global puzzle_board
    global moves # number of moves the player has made 
    global chances # user input that determines maximum moves for each puzzle game 
    global t_win # turtle responsible for win gif

    # turtle responsible for writing player moves on board and updating # of moves
    t_moves.speed(10)
    t_moves.hideturtle()
    t_moves.penup()
    t_moves.goto(-300, -350)

    
    if chances >= moves: # conditional if player has enough moves to continue playing
        t_moves.clear()
        moves += 1
        desired_text = "Player moves:{}".format(moves) 
        t_moves.write(desired_text, align="left", font=('Arial', 20, 'bold') ) # updates the player moves

        # call winner function and return boolean, detect if turtle object list is equal to solution turtle object list
        equal = is_winner(turtle_list_two_d, turtle_list_solution_two_d)  

        if moves > 0 and equal == True: 
            with open("leaderboard.txt", mode='a') as outfile: 
                outfile.write(f"{moves}: {name}\n\n") # adding user's name and score to leaderboard.txt file
            screen.addshape("Resources/winner.gif") 
            t_win.shape("Resources/winner.gif") # adding winner gif to screen
            time.sleep(3)
            quit() # exit game
    
    else: # if user has no more chances 
        screen.addshape("Resources/lose.gif") # add loser gif to screen 
        t_lose.shape("Resources/lose.gif")
        time.sleep(3)
        screen.addshape("Resources/credits.gif") # add credits to screen 
        t_lose.shape("Resources/credits.gif")
        time.sleep(5)
        quit() # exit game
        
          

def puzzle_functionality_clicked(x_coord, y_coord, length, num_of_tiles, coordinate_two_d,
                                 puzzle_board, turtle_list_two_d): 
    '''
    Function -- puzzle_functionality_clicked
        Function obtains information to detect whether user's click is on puzzle.
        If yes, the functions runs helper functions involved in
        swapping tiles.
    Parameters:
        x_coord: the X-coordinate of the user's click
        y_coord: the Y-coordinate of the user's click
        length: the length of each side of a given puzzle piece (int)
        num_of_tiles: the number of tiles in a given puzzle (int)
        coordinate_two_d: a 2D list (cooresponding to puzzle board size) that contains the coordinate
            placement of each puzzle piece 
        puzzle_board: a 2D list that contains the shuffled or ordered numbers from
            1 to # of tiles for a given puzzle.
        turtle_list_two_d: a list containing the puzzle piece gif image turtles in the
            2D form
    '''
    global cursor
    global screen
    
    # determines the parameters of each puzzle board using the length and number of tiles data of each puzzle 
    if -380.0 < x_coord < (-380.0 + (length * math.sqrt(num_of_tiles)) + (2 * num_of_tiles))\
        and 330 >= y_coord >= (330 - (length * math.sqrt(num_of_tiles)) - (2 * num_of_tiles)):

        # calls function that determines the coordinates and tile of the user's click on the puzzle board
        clicked_tile_coordinate, selected_tile = clicked_tile(x_coord, y_coord, coordinate_two_d, length, puzzle_board)

        # calls function that determines where the blank tile is on the puzzle board as well as its coordinates
        blank_tile, blank_tile_coordinate = is_blank(puzzle_board, coordinate_two_d)

        # calls function that determines if user's click is adjacent blank tile
        bool_is_adjacent = is_adjacent(blank_tile_coordinate, clicked_tile_coordinate, length)

        # calls function that swaps tiles horizontally if adjacency is horizontally
        swap_tile(blank_tile, selected_tile, bool_is_adjacent, puzzle_board, turtle_list_two_d, coordinate_two_d)

        # calls function that swaps tiles vertically if adjacency is vertical
        swap_tile_vertically(blank_tile, selected_tile, bool_is_adjacent, puzzle_board, turtle_list_two_d, coordinate_two_d)
         
    

def draw_rectangle(length, width, x_coord, y_coord, color= 'black'):
    '''
    Function -- draw_rectangle
        Function responsible for drawing rectangular borders around
        the puzzle board, buttons, and leaderboard by utilizing
        the turtle module
    Parameters:
        length: the length of each side of the rectangle (int)
        width: the width of the rectangles (int)
        x_coord: the X-coordinate corresponding to where the
            turtle should be placed before drawing begins
        y_coord: the Y-coordinate corresponding to where the turtle
            should be initially placed before drawing begins
        color: the color of the border
        
    '''
    global cursor
    cursor = turtle.Turtle()
    cursor.hideturtle()
    cursor.speed(10)
    cursor.color(color)
    cursor.penup()
    cursor.goto(x_coord, y_coord) 
    cursor.pendown()
    cursor.width(4)
    cursor.forward(length)
    cursor.right(90)
    cursor.forward(width)
    cursor.right(90)
    cursor.forward(length)
    cursor.right(90)
    cursor.forward(width)
    cursor.right(90)
    cursor.penup()
    
    
    
    
def draw_gameboard(): 
    '''
    Function -- draw_gameboard
        This function draws the border that surrounds puzzle
        game board by calling the draw_rectangle function which
        utilizes the turtle module
    Parameters: None
    '''
    
    draw_rectangle(500, 600, -400, 350)


    

def draw_leaderboard():
    '''
    Function -- draw_leaderboard
        This function draws a blue border that surrounds the
        leaderboard by calling draw_rectangle which utilizes
        the turtle module
    Parameters: None
    '''
    draw_rectangle(250, 600, 125, 350, "blue")

    

def draw_buttonboard():
    '''
    Function -- draw_buttonboard
        This function calls a helper function, draw_rectangle,
        which utlizes the turtle module to draw border for button board
        as well as places the reset, load, and quit buttons
        in right place
    Parameters: None
    '''
    # draws rectangle to represent button board border
    draw_rectangle(775, 100, -400, -275)

    global cursor
    cursor = turtle.Turtle()
    cursor.pencolor("white")
    cursor2 = turtle.Turtle()
    cursor2.pencolor("white")
    cursor3 = turtle.Turtle()
    cursor3.pencolor("white") 
    screen = turtle.Screen()
    cursor.speed(10)
    cursor.penup()
    
    # placement of quit button
    cursor.goto(310, -325)
    screen.addshape("Resources/quitbutton.gif")
    cursor.shape("Resources/quitbutton.gif")

    # placement of load button
    cursor2.speed(10)
    cursor2.penup()
    cursor2.goto(215, -325)
    cursor.pendown()
    screen.addshape("Resources/loadbutton.gif")
    cursor2.shape("Resources/loadbutton.gif")

    # placement of reset button
    cursor3.speed(10)
    cursor3.penup()
    cursor3.goto(120, -325)
    cursor.pendown()
    screen.addshape("Resources/resetbutton.gif")
    cursor3.shape("Resources/resetbutton.gif")

    

def thumbnail_placement(thumbnail="Images/mario/mario_thumbnail.gif"):
    '''
    Function -- thumbnail_placement
        Function utilizes turtle module to place the thumbnail gif
        of current puzzle on the board at the top right corner of
        the leaderboard border
    Parameters:
        thumbnail: the pathway to thumbnail gif (string)    
    '''
    
    global t_thumbnail # turtle that places thumbnail gif 
    screen = turtle.Screen()
    t_thumbnail.clear()
    t_thumbnail.speed(10)
    t_thumbnail.penup()
    t_thumbnail.goto(325, 300) # turtle goes to upper right corner of leaderboard border
    t_thumbnail.pendown()
    screen.addshape(thumbnail) # thumbail is placed on screen
    t_thumbnail.shape(thumbnail) 




def write_text(desired_text, x, y):
    '''
    Function -- write_text
        This function utilizes turtle to write text.
        Specifically, responsible for writing the word
        'Leaders' on the leaderboard as well as leader's names.
    Parameters:
        desired_text: string containing the desired text that will
            be placed on the leaderboard (string)
        x: X-Coordinate of the placement of the turtle
            that will write the name on the leaderbaord (int)
        y: Y-Coordinate of the placement of the turtle that will
            write the name winner's name and score on the leaderboard (int)
    '''
    global cursor
    cursor = turtle.Turtle()
    cursor.color('blue')
    cursor.hideturtle()
    cursor.penup()
    cursor.goto(x, y)
    cursor.pendown()
    cursor.write(desired_text, False, "left", ('Arial', 20) )
    cursor.penup()



    

def make_dictionary(file_name):
    '''
    Function -- make_dictionary
        This function takes a file name (.puz files) and creates two
        dictionaries. The first dictionary created is the meta_data dictionary
        that creates a dictionary utilizing file_name, size, thumbnail, and
        number of tiles as keys. The puzzle dictionary utilizes integers from 1
        to max tile number as keys as the pathway to the gif image of the puzzle
        piece as its value
    Parameters:
        file_name: a string corresponding to the .puz file name 
    Returns:
        meta_dict: dictionary containing metadata name, number, size, and thumbnail
            as keys as their respective data within .puz file as value
        puz_pieces_dict: a dictionary containing the puzzle pieces
            number as key and pathway to image as value

    '''
    # open file and create a list containing puzzle pieces data and metadata
    with open(file_name, mode='r') as infile: # open file
        puz_list = []
        for line in infile:
            new_line = line.replace("\n", "")
            new_new_line = new_line.replace(" ", "")
            puz_list.append(new_new_line.split(":")) 
            
        # create two seperate lists one containing just meta data and the other containing puzzle pieces info
        meta_list = puz_list[:4]
        pieces_list = puz_list[4:]
        key_meta = []
        value_meta = []

        #create key, value meta_lists to create dictionary
        for each in meta_list:
            for j in range(len(each)):
                if j == 0:
                    key_meta.append(each[j])
                else: 
                    value_meta.append(each[j])

        # create key, value puzzle pieces lists to create dictionary
        key_puz_pieces = []
        value_puz_pieces = []
        for each in pieces_list:
            for j in range(len(each)):
                if j == 0:
                    key_puz_pieces.append(each[j])
                else:
                    value_puz_pieces.append(each[j])

        # creates dictionary from metadata of .puz files
        meta_dict = {}
        for i in key_meta:
            j = key_meta.index(i)
            meta_dict[i] = value_meta[j]
        puz_pieces_dict = {}
        for i in key_puz_pieces:
            j = key_puz_pieces.index(i)
            puz_pieces_dict[i] = value_puz_pieces[j]

        return meta_dict, puz_pieces_dict



        

def open_puz_files(file_name="mario.puz"):
    '''
    Function -- open_puz_files
        This function calls make_dictionary function to retrieve
        dictionaries containing the informaiton from the .puz files
        utilizes the meta data diction to return the length of a side
        of a puzzle piece within a given puzzle as well as the number of
        tiles in given puzzle
    Parameters:
        file_name: string containing the .puz file name (mario.puz is
            set as default parameter)
    Returns:
        length: an integer corresponding to the the length of each size
            of the square puzzle piece
        num_of_tiles: an integer corresponding to the number of tiles
            in a given puzzle
    '''

    # call make dictionary to make dictionaries out of metadata and data from file
    meta_dict, puz_pieces_dict = make_dictionary(file_name)

    length = '' # initialize length variable

    for each in meta_dict.keys(): # iterate through keys of dictionary
        if each == 'size':
            length = meta_dict[each] # obtain length from 'size' key
        if each == 'number':
            num_of_tiles = meta_dict[each] # obtain num_of_tiles form 'number' key
    
    return int(length), int(num_of_tiles)
     


     
def square(x_coord, y_coord, length):
    '''
    Function -- square
        This function utilizes turtle to draw the appropriate sized squares
        that enclose the puzzle pieces on the puzzleboard at the right location.
        Creates a new turtle each time it draws a square
    Parameters:
        x_coord: the X-coordinate corresponding to where the turtle should be placed
            prior to drawing the square (starts at upper right hand corner
            a given square) (int)
        y_coord: the Y-coordinate corresponding to where the turtle should be placed
            prior to drawing the square (starts at upper right hand corner
            a given square) (int)
        length: the size of one side of the square (int)
    Returns:
        square_list: a list containing turtle objects that are responsible for drawing
        the squares
    '''
    
    global cursor
    cursor = turtle.Turtle() # creation of a new turtle
    cursor.speed(10)
    cursor.hideturtle()
    cursor.penup()
    cursor.setpos(x_coord, y_coord)
    cursor.pendown()
    cursor.forward(length)
    cursor.right(90)
    cursor.forward(length)
    cursor.right(90)
    cursor.forward(length)
    cursor.right(90)
    cursor.forward(length)
    cursor.right(90)

    square_list.append(cursor) # append turtles to square list 
    return square_list




def create_list(start, stop):
    '''
    Function -- create_list
        This function creates a 1D list of numbers from a given
        start parameter to stop. For instance, if caller inputs
        1 for start and 16 for stop. A list containing
        integers from 1 to 16 will be created
    Parameters:
        start: integer representing the starting number at index 0
            of the returned list
        stop: integer is at the index -1 of the formed list. The numbers
            between the start and stop indexes increase by 1 step
    Returns:
        list_of_positions: a list that contains a list of integers
            increasing by 1 step
    '''
    list_of_positions = [position for position in range(start, stop + 1)]
    return list_of_positions




def create_two_d_list(list_of_positions):
    '''
    Function -- create_two_d_list:
        A function that creates a two d list from a given
        list parameter. The size of each nested list is
        the square root of the len(list_of_positions). Utilized
        to create the puzzle_board of each puzzle.
    Parameters:
        list_of_positions a list containing integers from 1 to
            length of the list
    Returns:
        puzzle_board: a nested 2D list synonymous to the puzzle board
            game
    
    '''
    # row size is the square root of the length of the list_of_positions parameter
    row_size = int(math.sqrt(len(list_of_positions))) 

    # creation of puzzle board
    puzzle_board = [list_of_positions[i:i + row_size] for i in range(0, len(list_of_positions), row_size)]

    puzzle_board_coordinates = [list_of_positions[i:i + row_size] for i in range(0, len(list_of_positions), row_size)]
    return puzzle_board
    
        


def create_coordinate_list(x, y):
    '''
    Function -- create_coordinate_list
        A function that creates a one dimensional coordinate list. Utilized
        when creating the coordinates of the puzzle piece turtles on the puzzle
        board
    Parameters:
        x: represents the X-coordinate
        y: represents the Y-coordinate
    Returns: a one dimensional list of tuples representing coordinates
    '''
    
    coordinate_list.append((x, y))

    return coordinate_list
    
    
def draw_shuffled_squares(length, num_of_tiles, puz_pieces_dict): 
    '''
    Function -- draw_shuffled_squares
        This function utilizes turtle and initiates the drawing of squares on the puzzle
        board as well as placing shuffled puzzle pieces on the puzzle
        board. This function returns lists containing information on the
        position of the turtle objects (puzzle piece gif images), the a coordinate list
        representing the position of each turtle object, anda puzzle board list to represent
        the board post shuffle
    Parameters:
        length: the length of each side of the square puzzle piece (integer)
        num_of_tiles: the number of tiles in a given puzzle (integer)
        puz_pieces_dict: a dictionary that contains an integer as its key
            and the image pathway to the puzzle piece gif image
            as its value
    Returns:
        turtle_pieces_list: a list that contains the gif image (puzzle piece images) turtle objects
            returned from function
        square_list: a list containing turtles that creates a square
            that encloses the puzzle tiles
        coordinate_two_d: a 2D list (corresponding to puzzle board size) that contains the coordinate
            placement of each turtle in turtle_pieces_list (the list containing the turtle objects of
            gif .puz images
        puzzle_board: a 2D list that contains the shuffled or ordered numbers from
            1 to # of tiles for a given puzzle.
        length: the length of one side of a puzzle tile 
        num_of_tiles: the number of tiles in a given puzzle (int)
        turtle_list_two_d: a list containing the puzzle piece gif image turtles in the
            2D form
    
    '''
    
    global cursor
    global screen

    # intiate start and stop variables for create_list function call
    start = 1
    stop = len(puz_pieces_dict)
    list_of_shuffled_positions = create_list(start, stop) # create ordered 1D list of numbers
    random.shuffle(list_of_shuffled_positions) # shuffle elements in numbers list

    # create a 2D list which is synonymous to how the puzzle pieces will be placed on board
    puzzle_board = create_two_d_list(list_of_shuffled_positions)
    
   
    # draw squares and add puzzle pieces to the puzzle board 
    
    x_coord, y_coord = -380, 330 # intialize x and y coordinates (all puzzles start at same position)
    turtle_pieces_list = []
    x_coord_list = []
    coordinate_list = []
    for row in puzzle_board: 
        for col in row:
            square_list = square(x_coord, y_coord, length) # draw square that encloses each puzzle piece
            x_coord += length + 2
            PositionService.set_position(x_coord, y_coord) 
            PositionService.set_visible( True) 
            
            # obtains puzzle_piece pathway to gif from puz_pieces dictionary 
            puz_piece = str(puz_pieces_dict[str(col)]) # col = an element (number) in puzzle board list

            
            # create a new turtle with each iteration
            col = turtle.Turtle() 
            col.pencolor("white")
            col.speed(10)
            col.penup()


            # set position of turtle puzzle piece object in center of drawn square
            puz_piece_x_coord = x_coord - (length/2) - 1
            puz_piece_y_coord = y_coord - (length/2) - 1

            # append turtle puzzle piece object to coordinate list
            coordinate_list.append((puz_piece_x_coord, puz_piece_y_coord))
            
            # place puzzle piece gif image to board 
            col.setpos(puz_piece_x_coord, puz_piece_y_coord)
            col.pendown()
            screen.addshape(fr'{os.path.normpath(puz_piece)}')   
            col.shape(fr'{os.path.normpath(puz_piece)}')

            # adding turtle puzzle piece objects to two turtle lists (the gif puzzle piece images become turtles)
            turtle_list.append(col)
            turtle_pieces_list.append(col) 
            
        # ensures that puzzle pieces are placed in row below after each row is finished
        y_coord -= length + 2
        x_coord = -380
        
    # creation of two dimensional coordinate list, contains the coordinates of the puzzle piece turtle objects 
    coordinate_two_d = create_two_d_list(coordinate_list)

    # creation 2D turtle pieces objects list, contains positions of objects synonymous to position on puzzle board
    turtle_list_two_d = create_two_d_list(turtle_list)
    
    return turtle_pieces_list, square_list, coordinate_two_d, puzzle_board, turtle_list_two_d


def draw_solution_squares(length, num_of_tiles, puz_pieces_dict): # call for when you hit reset button
    '''
    Function -- draw_solution_squares
        This function utilizes turtle and initiates the drawing of squares on the puzzle
        board as well as placing ordered puzzle pieces on the puzzle
        board. This function returns lists containing information on the
        position of the turtle objects (puzzle piece gif images), the a coordinate list
        representing the position of each turtle object, anda puzzle board list to represent
        the board post shuffle
    Parameters:
        length: the length of each side of the square puzzle piece (integer)
        num_of_tiles: the number of tiles in a given puzzle (integer)
        puz_pieces_dict: a dictionary that contains an integer as its key
            and the image pathway to the puzzle piece gif image
            as its value
    Returns: 
        turtle_pieces_list: a list that contains the .puz gif image turtle objects
            returned from function
        square_list: a list containing turtles that creates a square
            that encloses the puzzle tiles
        coordinate_two_d: a 2D list (corresponding to puzzle board size) that contains the coordinate
            placement of each turtle in turtle_pieces_list (the list containing the turtle objects of
            gif images)
        puzzle_board: a 2D list that contains the ordered numbers from
            1 to # of tiles for a given puzzle.
        length: the length of one side of a puzzle tile 
        num_of_tiles: the number of tiles in a given puzzle (int)
        turtle_list_two_d: a list containing the puzzle piece gif image turtles in the
            2D form
    '''


    global cursor
    global screen
    global list_of_turtles_sol

    
    cursor2 = turtle.Turtle()
    cursor2.hideturtle()
    cursor2.speed(10)

    # intiate start and stop variables for create_list function call
    start = 1
    stop = len(puz_pieces_dict)
    list_of_positions = create_list(start, stop)
    puzzle_board = create_two_d_list(list_of_positions)

    turtle_list.clear() # clears current turtle list


    # initialization of x and y coordinates as well as lists
    x_coord, y_coord = -380, 330
    sol_coordinate_list = []
    list_of_turtles_sol = []

    # draw squares and add puzzle pieces to the puzzle board 
    for row in puzzle_board: 
        for col in row:
            square(x_coord, y_coord, length)
            x_coord += length + 2
            PositionService.set_position(x_coord, y_coord) 
            PositionService.set_visible( True) 
            
             
            puz_piece = str(puz_pieces_dict[str(col)])
            
            # set position of turtle puzzle piece object in center of drawn square
            sol_puz_piece_x_coord = x_coord - (length/2) - 1
            sol_puz_piece_y_coord = y_coord - (length/2) - 1

            
            # append turtle puzzle piece object to solution coordinate list
            sol_coordinate_list.append((sol_puz_piece_x_coord, sol_puz_piece_y_coord))
            col = turtle.Turtle()
            col.speed(10)
            col.penup()

            # place puzzle piece gif image to board 
            col.setpos(x_coord - (length/2) - 1, y_coord - (length/2) - 1)
            col.pendown()
            screen.addshape(fr'{os.path.normpath(puz_piece)}')    
            col.shape(fr'{os.path.normpath(puz_piece)}')
           
            # adding turtle puzzle piece objects to two turtle list (the gif images become turtles)
            list_of_turtles_sol.append(col)
            turtle_list.append(col)
            
        # ensures puzzle pieces are placed in row below after all iterations of each nested list is finished    
        y_coord -= length + 2
        x_coord = -380
        
    # creation 2D turtle pieces objects list, contains positions of objects synonymous to position of puzzle board
    coordinate_two_d = create_two_d_list(sol_coordinate_list)
    turtle_list_two_d = create_two_d_list(turtle_list)
    
    return list_of_turtles_sol, square_list, coordinate_two_d, puzzle_board, turtle_list_two_d

   


def driver():
    '''
    Function -- driver
        This function acts a driver in order for puzzle game to run
        accordingly.
    Parameters: None
    '''
    screen_opener() # sets up screen size, splashscreen, and prompts user for name and num of chances
    draw_gameboard() # draws game board
    draw_leaderboard() # draws leader board
    draw_buttonboard() # draws button board

    # retrieves a list of the names of the .puz files in the directory
    puzzle_names, puzzle_file_names = get_menu()
    
    # opens files to obtain length of one side of puzzle piece and number of tiles in a given puzzle
    length, num_of_tiles = open_puz_files(puzzle_file_names[-1]) 
    meta_dict, puz_pieces_dict = make_dictionary(puzzle_file_names[-1]) # make dictionary for first puzzle
    menu = ""

    # places thumbnail on top right corner of leaderboard
    thumbnail_placement()

    # write 'Leaders:' on leaderboard
    t_leaderboard.penup()
    t_leaderboard.color('blue')
    t_leaderboard.goto(140, 325)
    t_leaderboard.pendown()
    t_leaderboard.write("Leaders:", False, "left", ('Arial', 20) )
    leaderboard() # write the name of the leaders on the leaderboard

    # draw squares and place shuffled puzzle pieces on board
    global turtle_pieces_list, square_list, coordinate_two_d, puzzle_board, turtle_list_two_d
    turtle_pieces_list, square_list, coordinate_two_d, puzzle_board, turtle_list_two_d = draw_shuffled_squares(length, num_of_tiles, puz_pieces_dict)
    
    # start game
    play_method(turtle_pieces_list, square_list, coordinate_two_d, puzzle_board,
                length, num_of_tiles, turtle_list_two_d, menu="mario.puz")
    
    
    
   

def main():
    driver()
    
    
    
if __name__ == "__main__":
    main()



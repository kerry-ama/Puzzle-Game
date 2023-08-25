# Puzzle-Game

# 1.1 Puzzle Sliding Game Overview
The puzzle slider game is a combination puzzle game where a player must slide pieces vertically or horizontally on a board to establish an end result that matches a solution. The pieces moved may consist of shapes, pictures, patterns, letters or numbers. Users must use the mouse to play the game and the use of keyboard action is necessary at the start of the game when user's are prompted to type their name. User interactions are achieved via Python's Turtle module. 

Source Files: 
>puzzle_game.py -> runs the game and contains all of the helper functions
>
>leaderboard.txt file -> if a player wins the game, it is added to the file
>
>5001_puzzle.err -> collects error messages

# 1.2 Game Illustrations
<img src="https://github.com/kerry-ama/Puzzle-Game/blob/main/solved_mario.png" width="300" height="300">



# 1.3 Detailed Game Design
To create my puzzle board game, I took a procedural approach by creating many helper functions, global variables, and one nested function for my program. First off, the opening of the game features a splash screen as well as two user input prompts. These features were created in the screen_opener() function. In order for the game board borders and buttons to be placed on the game board, I created one function, draw_rectangles(), that draws a rectangle using turtle module and three additional functions (draw_leaderboard(), draw_gameboard(), draw_puzzleboard()) to make the three borders as well as place the buttons in the right location. 

Furthermore, I created two dictionaries, one containing the general information of a puzzle and the other with an integer as a key and the gif image pathway to the puzzle image as the value. These dictionaries allowed me to create a two dimensional (2D) list of integers which I referred to as 'puzzle board'. With these dictionaries, a 2D nested list was created by utilizing the math.sqrt() method to create the correct number of nested lists as well as correct number of elements within the puzzle board list. As for achieving the puzzle pieces and squares to be placed in appropriate positions on the puzzle board, I created the function draw_shuffled squares() which utilizes for loops to iterate through the puzzle board list, draw squares as well as place the puzzle piece images in the middle of the enclosing square. 

For the puzzle board to swap tiles, I created functions to detect the parameters where the blank tile was on the game board, if a click on screen is a tile, the coordinate of the clicked tile (if clicked), and whether the clicked tile is adjacent to the blank tile. If a clicked tile is adjacent to the blank square, I created two functions, swap_tiles() and swap_tiles_vertically(), to swap tiles horizontally and vertically, respectively. In order for the swap to initiate, the indexes of the blank tile and the adjacent clicked tile are exchanged. Additionally, with each swap the number of player moves is updated. Lastly, if a player wins or loses, the a gif pops up to alert the user and the game ends and exits turtle module. 

To summarize, I utilized various 2D lists to keep track of turtle objects for gif placement, square drawings, and coordinates of puzzle pieces. With the use of global variables, I was able to access/update lists when necessary. The position of the indexes of the other puzzle pieces in comparison to the blank tile is what drove the puzzle swapping functionality. 

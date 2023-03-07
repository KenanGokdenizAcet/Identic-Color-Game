import sys

""" This function opens input file, and read all lines. If line ends with \n, function removes \n, and adds line into
lines list. Every line in lines list is splited by " ", and added into board list which is game board """
def create_board(inputFile):
    lines = []
    with open(inputFile, "r") as f:
        for line in f:
            if line.endswith("\n"):
                lines.append(line[:-1])
            else:
                lines.append(line)
    board = []
    for line in lines:
        board.append(line.split(" "))
    return board

""" This function looks every column in order. If there is an empty spot, "blank" increases by one. And if "blanks" is
equal to number of row, column number is added to "column_to_delete" list. Function removes every column from left to right. """
def check_column(board):
    column_to_delete = []
    for i in range(len(board[0])): #board[row][column]. Every row has same lenght, so I wrote board[0]
        blank = 0
        for line in board:
            if line[i] == " ":
                blank += 1
        if blank == len(board):
            column_to_delete.append(i)
    for j in sorted(column_to_delete, reverse = True):
        for line in board:
            line.pop(j)

""" This function looks at every row in order. If there is an empty spot, "blanks" increases by one. And if "blanks" is
equal to lenght of a row, row number is added to "row_to_delete" list. Function removes every row from bottom to top. """
def check_row(board):
    row_to_delete = []
    for row in range(len(board)): 
        blanks = 0
        for column in board[row]:
            if column == " ":
                blanks += 1
        if blanks == len(board[0]): #board[row][column]. Every row has same lenght, so I wrote board[0]
            row_to_delete.append(row)
    for row in sorted(row_to_delete, reverse = True): # Greatest number of row is bottom of the board, so reverse is True
        board.pop(row)

""" This function checks blanks in row. If a value which is in arow is blank, that row changes with the value in higher row.
And the value which is in heigher row becomes a blank. This process repeats number of row times."""
def check_blanks_in_row(board):
    for i in range(len(board)):
        for row_index in range(len(board) - 1,0,-1): #from bottom row to top row. Greatest row number is at bottom of the row
            for column_index in range(len(board[0])): #board[row][column]. Every row has same lenght, so I wrote board[0]
                if board[row_index][column_index] == " ":
                    board[row_index][column_index] = board[row_index - 1][column_index]
                    board[row_index -1][column_index] = " "

""" This function adds balls which is at bomb's column and row into balls set, and row and column are changed with " ".
If there is any bomb, bombs added bombs_in_balls set as (row, column). Lastly, score is calculated. This process repeats
every bomb in bombs_in_balls set. """
def bomb(board, row_index, column_index): 
    balls = set()
    bombs_in_balls = set()
    for row in range(len(board)): #this loop for balls in bomb's column
        if board[row][column_index] != " ": # checking if spot is blank
            balls.add((row, column_index, board[row][column_index])) # ball (row, column, color)
            if board[row][column_index] == "X": # checking if spot is bomb
                bombs_in_balls.add((row, column_index)) # adding bomb (row, column) into bombs_in_balls set
            board[row][column_index] = " " # changing with " "
    for column in range(len(board[row_index])): #this loop for bomb's row
        if board[row_index][column] != " ":
            balls.add((row_index, column, board[row_index][column])) # ball (row, column, color)
            if board[row_index][column] == "X":
                bombs_in_balls.add((row_index, column))
            board[row_index][column] = " "
    calculate_score(balls) # calculating score based on balls set
    
    if len(bombs_in_balls) != 0: # checking if there is any bomb
        for i, j in bombs_in_balls: # repating function for every bomb
            bomb(board,i,j)

""" This function removes same color neighbours of ball which row and column number are given. Function checks ball's neighbours' color. 
If same color ball and its neighbours, neighbours are added into balls set as (row number, column number, color). This process repaets
until amount of balls in balls set does not change, when initial and final lenght of balls set are equal."""
def check_neighbours(board, row_index, column_index):
    balls = set()
    color = board[row_index][column_index] 
    balls.add((row_index, column_index, color)) #firstly, choosen ball is added into balls set
    initial_lenght = 1 # value is given default
    final_lenght = -1 # value is given defalut
    while initial_lenght != final_lenght:  
        initial_lenght = len(balls)
        for row, column, color in balls:
            newballs = set()
            if column + 1 in range(len(board[0])): #checking if column number exists
                if board[row][column] == board[row][column + 1]: #checking negihbour's colur
                    newballs.add((row, column + 1, color)) #adding same color neighbour
            if column - 1 in range(len(board[0])): #checking if column number exists
                if board[row][column] == board[row][column - 1]:
                    newballs.add((row, column - 1, color))
            if row - 1 in range(len(board)): #checking if row number exists
                if board[row][column] == board[row - 1][column]:
                    newballs.add((row - 1, column, color))
            if row + 1 in range(len(board)): #checking if row number exists
                if board[row][column] == board[row + 1][column]:
                    newballs.add((row + 1, column, color))
            balls = set.union(balls, newballs)
        final_lenght = len(balls)
    if len(balls) != 1: # If lenght of balls set is equal to 1, there is only choosen ball in the balls.
        for i, j, color in balls: # every ball in balls set changes with " ", so ball is removed.
            board[i][j] = " "
        calculate_score(balls) # calculating score based on balls set

""" This function checks every ball's neighbours. If a ball's neighbour is the same color, ball's location is added balls set 
as (row, colum), or there is any "X" on the board, returns True. If there is no ball which its neighbour is the same color, returns False. """
def check_board(board):
    balls = set()
    for row_index in range(0,len(board)):
        for column_index in range(len(board[0])):
            if board[row_index][column_index] != " ":
                if board[row_index][column_index] == "X": #checking if there is any bomb on board.
                    balls.add(board[row_index][column_index]) #adding bomb into balls set
                if column_index + 1 in range(len(board[0])): #checking if column number exists 
                    if board[row_index][column_index] == board[row_index][column_index + 1]: #checking neighbour's color
                        balls.add((row_index, column_index + 1)) #adding same color neighbour
                if column_index - 1 in range(len(board[0])): #checking if column number exists
                    if board[row_index][column_index] == board[row_index][column_index - 1]:
                        balls.add((row_index, column_index - 1))
                if row_index - 1 in range(len(board)): #checking if row number exists
                    if board[row_index][column_index] == board[row_index - 1][column_index]:
                        balls.add((row_index - 1, column_index))
                if row_index + 1 in range(len(board)): #checking if row number exists
                    if board[row_index][column_index] == board[row_index + 1][column_index]:
                        balls.add((row_index + 1, column_index))
            if len(balls) != 0:
                return True
    if len(balls) == 0:
        return False

""" This function gives scores for removed balls from the board. It gives score for every ball in balls based on weight of colors dictionary. """
def calculate_score(balls):
    global score
    for ball in balls:
        score += weight_of_colors[ball[2]] #(row, column, color) for every ball.

""" This function prints board and score, and returns row and column number. """
def print_board(board, score):
    row = len(board) #board = [[row],[row], .....]
    column = len(board[0]) #board[row][column]. Every row has same lenght, so I wrote board[0]
    print()
    for line in board: #board = [[line], [line], [line], ...]
        print(" ".join(line))
    print("\n\nYour score is: {}\n".format(score))
    return row, column

board = create_board(sys.argv[1])
score = 0
weight_of_colors = {"B": 9, "G": 8, "W": 7, "Y": 6, "R": 5, "P": 4, "O": 3, "D": 2, "F": 1, "X": 0}

while True:
    if len(board) != 0:
        row, column = print_board(board, score) 
    else: # If board is completely blank:
        print("\n\n\nYour score is: {}".format(score))
        print("\nGame over!\n")
        break
    if not check_board(board): #checking game board
        print("Game over!\n")
        break

    while True:
        inp = input("Please enter a row and column number: ")
        coordinate = inp.split(" ")
        x = int(coordinate[1]) # x = column number
        y = int(coordinate[0]) # y = row number
        if y in range(0,row) and x in range(0, column) and board[y][x] != " ":
            break
        print("\nPlease enter a valid size!\n")
    if board[y][x] == "X": #checking if choosen ball is a bomb
        bomb(board, y, x)
        check_column(board) #checking if there is any empty column, and removing them
        check_blanks_in_row(board) #checking if there is any empty spot under a bal, and remove them
        check_row(board) #checking if there is any empty row, and remove them
    else:
        check_neighbours(board, y, x)
        check_column(board)
        check_blanks_in_row(board)
        check_row(board)
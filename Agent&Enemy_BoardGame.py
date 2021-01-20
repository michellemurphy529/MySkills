# main function 
def main():

    #text file for board of where Agents and Enemies are
    filename = "board3.txt"
    #text file used for where the Traps in the board are found
    trap_filename = "trap3.txt"
    #reading these two files to create boards for user to see and also so we can manipulate the board 2dlist as game progresses
    board = read_file(filename)
    #if file not found or there is not the right dimensions or we have no symbols in the file we terminate the program
    if board == None:
        return print("Please review your board textfile.")

    trap_map = read_file(trap_filename)

    #extra message to tell the user which file the program is having problems with
    if trap_map == None:
        return print("Please review your trap board textfile.")

    agent_count, trap_count, enemy_count = stats_for_description(board, trap_map)       #helper function


    #displaying the board and instructions to the user so they can play.
    print("You are playing with a {}x{} board.\n".format(len(board), len(board)))
    display_board(board)
    print()
    print("Board stats:\n============\nTotal Agent (A): {}\nTotal Enemies (E): {}\nThis board also has {} hidden traps (T) on rows [1-4].".format(agent_count, enemy_count, trap_count))
    print("You must kill all enemies to win this board.\nTo kill an enemy, move an Agent to that Enemy's location.\nYou can move Agents horizontally, vertically or diagonally.\nIf your Agent walks on a hidden trap, they will die.\nIf you choose a wrong move, you'll lose 2 points.\nIf you kill an Enemy, you'll get 5 points.\nIf you finish the board (kill all enemies), you'll get 10 more points.\nGame continues until you finish the board, or all Agents are dead, or you choose to quit.\n")

    #initializing score for the current game
    current_score = 0
    
    #initializing the counter for how many agents are left on the board
    num_of_agents_on_board = agent_count
    num_of_enemy_on_board = enemy_count
    
    #move loop
    while True:

        #user chooses to continue playing or quit game
        user_input_play_or_quit = input("Choose P/p to Play, or Q/q to Quit: ")
        #if user doesn't input the right input we continue looping until they provide input that makes sense to the program
        if not(user_input_play_or_quit in ["Q", "q", "P", "p"]):
            print("Invalid entry. Try again.")
        #we go to this condition when user wants to quit the game
        elif user_input_play_or_quit in ["Q", "q"]:
            print("You have decided to quit the game..\n")
            return
        #otherwise the input is valid and we move on with our game
        else:
            r1,c1,r2,c2 = take_input(board)     #verifying input given by user
            valid = check_for_valid_moves(board, r1, c1, r2, c2)        #checking if move is valid ie. horizontal, vertical or 1-1 diagonal line.
            
            if not valid:
                current_score -= 2
                helper_board(board, current_score)      #print our board to user with the score they received this round

            else:
                valid_direction = helper_for_valid_move(board, r1, c1, r2, c2)      #checking to see if the user input is a valid move
                print("Validating move.... valid {} move".format(valid_direction))
                
                trap_found, row, col = check_for_traps(trap_map, r1, c1, r2, c2)        #checking to see if there will be a trap to intercept the path or not
                
                board[r1][c1] = "-"

                if trap_found:
                    print("Oh no! A trap is found at {},{} and now your agent is dead! You lost 2 points".format(row, col))
                    board[row][col] = "T"
                    current_score -= 2      #take away 2 points
                    num_of_agents_on_board -= 1     # keeping track of how many agents are left on the board
                    helper_board(board, current_score)      #printing the board
                    if num_of_agents_on_board == 0:     #if all the agents die we force the end of game
                        print("All of your Agents are dead. Please play again.")
                        return
            
                else:
                    if board[r2][c2] == "-":    #if it is a valid move but doesn't hit an enemy
                        board[r2][c2] = "A"
                        print("You've successfully moved to {},{}, no points are scored in this step though.".format(r2,c2))
                        helper_board(board, current_score)

                    if board[r2][c2] == "E":        #if we get to an enemy
                        board[r2][c2] = "A"
                        print("GOT an ENEMY!!! Scored 5..")
                        current_score += 5      #increase score by 5
                        num_of_enemy_on_board -= 1      #track the amount of enemies left on the board
                        helper_board(board, current_score)
                        if num_of_enemy_on_board == 0:      #if we have no enemies left on the board we force the increase in 10 points and end game
                            current_score += 10
                            final_board = display_of_end_board(board, trap_map)
                            print("Well done!! All enemies are dead.")
                            display_board(final_board)      #displaying the last boad with the traps exposed to the user
                            return print("\nYour final score is {}! Game is terminating\n".format(current_score))

# this function takes a string input filename and returns a 2D-list to represent the board
def read_file(filename):

    #if file is not found we close file and then return our message
    try:
        f = open(filename, "r")
    except FileNotFoundError: 
        return print("File not found/available")

    #we read the file because we found a file and start to collect our information
    list_board = []
    while True:
        lines = f.readline().strip()
        lines_list = lines.split(",")
        if lines == "":
            break
        else:
            list_board.append(lines_list)

    #testing that the matrix is in fact a valid n x n matrix
    try:
        for i in range(len(list_board)):
            list_test = list_board[i]
            if len(list_board) != len(list_test):
                raise Exception
    #not a valid n x n matrix therefore, exception is raised
    except Exception:
        print("The board does not have the same length and width dimensions")
        return

    #testing to see that there are infact symbols on the board
    try:
        symbol = 0  #initial the symbol counter
        for row in range(len(list_board)):
            for col in range(len(list_board)):
                if list_board[row][col] == "A":
                    symbol += 1
                elif list_board[row][col] == "E":
                    symbol += 1
                elif list_board[row][col] == "T":
                    symbol += 1
                else:
                    continue
        if symbol == 0:     #if no symbols are found that match what we are looking for
            raise Exception
    except Exception:
        print("There are not enough symbols your file.")
        return 
    
    f.close()    #close the file
    return list_board

#this function is a helper funtion to determine how many Agents, Traps and Enemies are in the board provided.
# this info will be input for our description at the start of the game.
def stats_for_description(board_list2D, trap_list2D):
    agent_count = 0
    trap_count = 0
    enemy_count = 0
    #finding the symbols from loops
    for element in board_list2D:
        for board_piece in range(len(element)):
            if element[board_piece] == "A":
                agent_count += 1
            if element[board_piece] == "E":
                enemy_count += 1
    for element in trap_list2D:
        for board_piece in range(len(element)):
            if element[board_piece] == "T":
                trap_count += 1
    return agent_count, trap_count, enemy_count

# takes a 2D-list as an input and prints the list to the terminal in the specified format described before.
def display_board(list2D):
    #formatting of numbers at top
    print("  ", end="")
    for i in range(0, len(list2D)):
        print("{}".format(i), end="")
    print()
    # '+' and '=' for the fomatted output
    print(" ", end="")
    print("+" + ("=" * len(list2D)) + "+", end="")
    print()
    #formatting the middle of the board where we can have different values everytime board is created.
    for x in range(0, len(list2D)):
        print("{}|".format(x), end="")
        list_inner = list2D[x]
        for element in range(len(list_inner)):
            print("{}".format(list_inner[element]), end="")
        print("|{}".format(x), end="\n")
    #formatting of the bottom of the board
    print(" ", end="")
    print("+" + ("=" * len(list2D)) + "+", end="")
    print()
    #last line with numbers
    print("  ", end="")
    for i in range(0, len(list2D)):
        print("{}".format(i), end="")
    print()
    return

# takes a 2D-list as an input and prints the list to the terminal in the specified format
def take_input(list2D):
    #Validation of row,col Agent input
    print("Choose the row,col of the Agent that you want to move:")
    while True:
        try:
            row1, col1 = input("Enter location: ").split(",")
            row1 = int(row1)
            col1 = int(col1)
            if row1 <= (len(list2D) - 1) and col1 <= (len(list2D) - 1) and row1 >= 0 and col1 >= 0:
    
                #validation of row,col where Agent moves to input
                print("Choose the row,col where you want to move your Agent to:")
                while True:
                    try:
                        row2, col2 = input("Enter location: ").split(",")
                        row2 = int(row2)
                        col2 = int(col2)
                        if row2 <= (len(list2D) - 1) and col2 <= (len(list2D) - 1) and row2 >= 0 and col2 >= 0:
                            return row1,col1,row2,col2
                        else:
                            raise Exception
                    except TypeError:
                        print("Please enter 2 positive integers between [0,{}] seperated by ','.".format(len(list2D) - 1))
                    except ValueError:
                        print("Please enter 2 positive integers between [0,{}] seperated by ','.".format(len(list2D) - 1))
                    except Exception:
                        print("At least one input is out of bound.")
            else:
                raise Exception
        except TypeError:
            print("Please enter 2 positive integers between [0,{}] seperated by ','.".format(len(list2D) - 1))
        except ValueError:
            print("Please enter 2 positive integers between [0,{}] seperated by ','.".format(len(list2D) - 1))
        except Exception:
            print("At least one input is out of bound.")


# takes 5 input arguments, a 2D-list representing the board, and four positive integers representing
# the rows and columns of the current location and the new location, respectively, This function 
# returns True if the proposed move is valid, otherwise returns False.
def check_for_valid_moves(list2D, r1, c1, r2, c2):
    if list2D[r1][c1] == "-":
        print("Validating move.... There is no agent at that starting position. Invalid Move!")
        return False
    elif list2D[r1][c1] == "E":
        print("Validating move.... You cannot move an enemy. Invalid Move!")
        return False
    elif list2D[r2][c2] == "A":
        print("Validating move.... Another agent is already there. Invalid Move!")
        return False
    elif r1 == r2 and c1 == c2:
        print("Validating move.... You are already at this position on the board. Invalid Move!")
        return False
    else:
        #horizontal or vertical valid move
        if r1 == r2 or c1 == c2:
            return True
        #if diagonal line
        if abs(((r2 - r1)/(c2 - c1))) == 1:
            return True
        else:
            print("Validating move.... invalid move.")
            return False

# This function is helper function to know which direction a valid move is going and 
# we will use this info to tell the user more about the move they chose to make.
def helper_for_valid_move(list2D, r1, c1, r2, c2):
    if r1 == r2 and c1 != c2:
        return "horizontal"
    if c1 == c2 and r1 != r2:
        return "vertical"
    if abs(((r2 - r1)/(c2 - c1))) == 1:
        return "diagonal"

#this function is a helper for the recursive check_for_traps function.
# it helps by categorizing what kind of recursive function the check_for_traps will carry out
def helper_for_check_for_traps(r1, c1, r2, c2):
    #if direction is right
    if c2 > c1:
        if r1 == r2:
            return "horizontal right"
        elif r2 > r1:
            return "diagonal right/down"
        else:
            return "diagonal right/up"
    #if direction is left
    elif c1 > c2:
        if r1 == r2:
            return "horizontal left"
        elif r2 > r1:
            return "diagonal left/down"
        else:
            return "diagonal left/up"
    #if direction is neither
    else:
        #if direction is down
        if r2 > r1:
            return "vertical down"
        else:
            return "vertical up"

#this function will return the next coordinate in path
def helper_next_step(r1, c1, r2, c2):
    direction = helper_for_check_for_traps(r1, c1, r2, c2)      #see previous helper function

    if direction == "horizontal right":
        return r1, c1 + 1
    if direction == "horizontal left":
        return r1, c1 - 1
    if direction == "vertical up":
        return r1 - 1, c1
    if direction == "vertical down":
        return r1 + 1, c1
    if direction == "diagonal right/down":
        return r1 + 1, c1 + 1
    if direction == "diagonal right/up":
        return r1 - 1, c1 + 1
    if direction == "diagonal left/down":
        return r1 + 1, c1 - 1
    if direction == "diagonal left/up":
        return r1 - 1, c1 - 1

# This function checks for traps in the board between the path of starting agent and where the agent will go
def check_for_traps(list2D, r1, c1, r2, c2):
    #base case if you are on a trap
    if list2D[r1][c1] == "T":
        return True, r1, c1
    #base case of last square on path
    if r1 == r2 and c1 == c2:
        return False, -1, -1
    #recusive case moving towards end of the path
    new_r1, new_c1 = helper_next_step(r1, c1, r2, c2)       #see previous helper function
    return check_for_traps(list2D, new_r1, new_c1, r2, c2)

#this function display's the current score and board after every move is done
def helper_board(list2D, score):
    print("\nCurrent board:\n")
    display_board(list2D)
    print("\nYour current score is {}\n".format(score))

# this function will display the final board with all hidden traps to user when they finish the game
def display_of_end_board(board, trap_map):
    for row_of_board in range(len(trap_map)):
        for col_in_board in range(len(trap_map)):
            if trap_map[row_of_board][col_in_board] == "T":
                board[row_of_board][col_in_board] = "T"
    return board

# calling our main function
if __name__ == "__main__":
    main()
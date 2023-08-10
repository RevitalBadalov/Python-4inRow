# Mor and Revital 314616095 & 315406223
import numpy as np
import random
# Imports
import socket
import sys
import threading
import time
import pickle

# Define constants
HOST = '127.0.0.1'  # Standard loopback IP address (localhost)
PORT = 60000  # Port to listen on (non-privileged ports are > 1023)
FORMAT = 'utf-8'  # Define the encoding format of messages from client-server
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


# Function that starts the server
def start_server():
    server_socket.bind(ADDR)  # binding socket with specified IP+PORT tuple

    print(f"[LISTENING] server is listening on {HOST}")
    server_socket.listen()  # Server is open for connections

    while True:
        connection, address = server_socket.accept()  # Waiting for client to connect to server (blocking call)
        close_flag = 0
        # active_count = threading.active_count() - 1
        if threading.active_count() > 5:
            active_flag = 0
            print("active flag", active_flag)
            connection.send(str(active_flag).encode(FORMAT))  # send amount of threads working
            # connection.close()
        else:
            active_flag = 1
            print("active flag", active_flag)
            connection.send(str(active_flag).encode(FORMAT))  # send amount of threads working
            thread = threading.Thread(target=game, args=(connection, address))  # Creating new Thread object.
            # Passing the handle func and full address to thread constructor
            thread.start()  # Starting the new thread (<=> handling new client)

        # if threading.active_count() == 1:  # Checking if no clients connected to the server client in total
         # print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n")  # printing the amount of threads working

        # on this process (opening another thread for next client to come!)

# Functions for the game Connect 4
def check_col(board, col):  # check if col is avialable
    return board[5][col] == 0


def check_next_row(board, col): # find first available row
    for i in range(6):
        if board[i][col] == 0:
            return i
    return -1

# functions for computer in hard mode:

def finish_col(board):  # connect four in col
    # check col
    for i in range(7):  # for all the beginnings of columns
        for j in range(3):  # for all rows
            if board[j][i] == 2 and board[j + 1][i] == 2 and board[j + 2][i] == 2 and \
                    board[j + 3][i] == 0:
                return i  # return the right column
    return -1


def make_col_of_3(board):   # make 3 in col
    # check col
    for i in range(7):  # for all the beginnings of columns
        for j in range(3):  # for all rows
            if board[j][i] == 2 and board[j + 1][i] == 2 and board[j + 2][i] == 0:
                return i  # return the right column
    return -1


def finish_row(board):   # connect four in row
    # check row:
    # add fourth circle:
    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if board[j][i] == 2 and board[j][i + 1] == 2 and board[j][i + 2] == 2 and \
                    board[j][i + 3] == 0:
                return i + 3
    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if board[j][i] == 0 and board[j][i + 1] == 2 and board[j][i + 2] == 2 and \
                    board[j][i + 3] == 2:
                return i
    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if board[j][i] == 2 and board[j][i + 1] == 0 and board[j][i + 2] == 2 and \
                    board[j][i + 3] == 2:
                return i + 1
    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if board[j][i] == 2 and board[j][i + 1] == 2 and board[j][i + 2] == 0 and \
                    board[j][i + 3] == 2:
                return i + 2
    return -1  # if you cant complete a row, return -1


def make_row_of_3(board):
    # add 3rd circle:
    for i in range(5):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if board[j][i] == 2 and board[j][i + 1] == 2 and board[j][i + 2] == 0 and \
                    board[j][i + 3] == 0:
                return i + 2
    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if board[j][i] == 2 and board[j][i + 1] == 0 and board[j][i + 2] == 2 and \
                    board[j][i + 3] == 0:
                return i + 1
    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if board[j][i] == 2 and board[j][i + 1] == 0 and board[j][i + 2] == 0 and \
                    board[j][i + 3] == 2:
                return i + 1
    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if board[j][i] == 0 and board[j][i + 1] == 2 and board[j][i + 2] == 2 and \
                    board[j][i + 3] == 0:
                return i
    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if board[j][i] == 0 and board[j][i + 1] == 2 and board[j][i + 2] == 0 and \
                    board[j][i + 3] == 2:
                return i + 2
    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if board[j][i] == 0 and board[j][i + 1] == 0 and board[j][i + 2] == 2 and \
                    board[j][i + 3] == 2:
                return i + 1
    return -1  # if you cant complete a row, return -1


def block_col(board): # block rival's column
    # check col
    for i in range(7):  # for all the beginnings of columns
        for j in range(3):  # for all rows
            if board[j][i] == 1 and board[j + 1][i] == 1 and board[j + 2][i] == 1 and \
                    board[j + 3][i] == 0:
                return i  # return the right column
    return -1


def block_row(board): # block rival's row
    # check row:
    # add fourth circle:
    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if j == 0:
                if board[j][i] == 1 and board[j][i + 1] == 1 and board[j][i + 2] == 1 and board[j][i + 3] == 0:
                    return i + 3
            else:
                if board[j][i] == 1 and board[j][i + 1] == 1 and board[j][i + 2] == 1 and \
                        board[j][i + 3] == 0 and board[j-1][i+3] != 0:
                    return i + 3

    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if j == 0:
                if board[j][i] == 0 and board[j][i + 1] == 1 and board[j][i + 2] == 1 and \
                        board[j][i + 3] == 1:
                    return i
            else:
                if board[j][i] == 0 and board[j][i + 1] == 1 and board[j][i + 2] == 1 and \
                        board[j][i + 3] == 1 and board[j-1][i] != 0:
                    return i

    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if j == 0:
                if board[j][i] == 1 and board[j][i + 1] == 0 and board[j][i + 2] == 1 and \
                        board[j][i + 3] == 1:
                    return i + 1
            else:
                if board[j][i] == 1 and board[j][i + 1] == 0 and board[j][i + 2] == 1 and \
                        board[j][i + 3] == 1 and board[j-1][i+1] != 0:
                    return i + 1
    for i in range(4):  # for all the beginnings of columns
        for j in range(6):  # for all rows
            if j == 0:
                if board[j][i] == 1 and board[j][i + 1] == 1 and board[j][i + 2] == 0 and \
                        board[j][i + 3] == 1:
                    return i + 2
            else:
                if board[j][i] == 1 and board[j][i + 1] == 1 and board[j][i + 2] == 0 and \
                        board[j][i + 3] == 1 and board[j-1][i+2] != 0:
                    return i + 2
    return -1  # if you cant complete a row, return -1


def connect_4(board): # all moves of computer
    # col = -1
    col = finish_col(board)
    if col != -1:
        return col
    col = finish_row(board)
    if col != -1:
        return col
    col = block_col(board)
    if col != -1:
        return col
    col = block_row(board)
    if col != -1:
        return col
    col = make_col_of_3(board)
    if col != -1:
        return col
    col = make_row_of_3(board)
    if col != -1:
        return col
    col = random.randint(0, 6)
    return col


def is_victory(board, circle): # find if someone won
    # check row:
    for i in range(4):  # for all the beginings of columns
        for j in range(6):  # for all rows
            if board[j][i] == circle and board[j][i + 1] == circle and board[j][i + 2] == circle and \
                    board[j][i + 3] == circle:
                return True
    # check col
    for i in range(7):  # for all the beginings of columns
        for j in range(3):  # for all rows
            if board[j][i] == circle and board[j + 1][i] == circle and board[j + 2][i] == circle\
                    and \
                    board[j + 3][i] == circle:
                return True
    # diagonal
    for i in range(4):  # for all the beginnings of columns
        for j in range(3):  # for all rows
            if board[j][i] == circle and board[j + 1][i + 1] == circle and board[j + 2][i + 2] == circle and \
                    board[j + 3][i + 3] == circle:
                return True

    # diagonal the other way
    for i in range(4):  # for all the beginnings of columns
        for j in range(3, 6):  # for all rows
            if board[j][i] == circle and board[j - 1][i + 1] == circle and board[j - 2][i + 2] == circle and \
                    board[j - 3][i + 3] == circle:
                return True


#the game's function:


def game(conn, add):
    is_playing = int(conn.recv(1024).decode(FORMAT))  # ask client if they want to play
    # if the player wants to play:
    if is_playing != 1:
        victories_counter1 = 0
        victories_counter2 = 0
        game_mode = int(conn.recv(1024).decode(FORMAT))  # easy or hard
        victories_num = int(conn.recv(1024).decode(FORMAT))  # get victories number from client
        max_steps_game = 0  # initiate counter for the longest game

        # start game:
        print("let the game begin!")
        while (victories_counter1 != victories_num) and (victories_counter2 != victories_num): # until Final victory
            board = np.zeros((6, 7))  # create board
            print("\n A new round has begun, may the odds be ever in your favor!")
            print(np.flip(board, 0))  # print the game board
            conn.send(pickle.dumps(board))  # send board to client
            round_over = 0 # end of round flag
            turn = 0  # turn flag
            moves_counter = 0
            while round_over != 1:  # until round ends
                if turn == 0:  # if player 1's turn:
                    row = -1
                    while row == -1:  # while rows in column aren't not valid
                        col = int(conn.recv(1024).decode(FORMAT))  # receive new column
                        print("You chose column ", col)
                        players_choice_m = ("You chose column:" + str(col)) # define player's choice
                        conn.send(str(players_choice_m).encode(FORMAT))  # send the printing

                        if check_col(board, col): # if col is available
                            row = check_next_row(board, col)  # check first available row
                            if row != -1:  # if row is valid
                                board[row][col] = 1  # drop player's choice

                                if is_victory(board, 1): # if player 1 won:
                                    print("Player 1 won in this round!")
                                    victories_counter1 += 1
                                    round_over = 1 #raise flag

                        if row == -1: # if all rows are full in column
                            print("You chose an unavailable column, please choose another")
                        conn.send(str(row).encode(FORMAT))  # send the printing

                else:  # computer's turn:

                    row = -1
                    while row == -1:
                        if game_mode == 1:  # if easy mode
                            col = random.randint(0, 6)  # generate a random column
                        else:
                            col = connect_4(board)  # generate col in hard mode
                        print("Computer chose column:", col)
                        players_choice_m = ("Computer chose column:" + str(col))
                        time.sleep(0.5)
                        conn.send(players_choice_m.encode(FORMAT))  # send the printing
                        if check_col(board, col): # if the col is available
                            row = check_next_row(board, col) # find first row
                            if row != -1:
                                board[row][col] = 2 # drop player's choice
                                if is_victory(board, 2): # if computer won:
                                    print("Player 2 won in this round!")
                                    victories_counter2 += 1
                                    round_over = 1 # raise flag
                        if row == -1: # if no available rows
                            print("An unavailable column was chosen")

                print(np.flip(board, 0))  # print the game board
                conn.send(pickle.dumps(board))  # send board to client
                # if round isn't over yet:
                time.sleep(0.2)
                conn.send(str(round_over).encode(FORMAT)) # send round's flag
                turn += 1 # update turn
                turn = turn % 2
                moves_counter += 1  # count the move
            # if round is over:
            if max_steps_game < moves_counter:  # update max steps counter is necessary
                max_steps_game = moves_counter

            # round summary:
            print("\nSTATUS OF THE GAME:\n")
            message = "\nSTATUS OF THE GAME:\n"
            time.sleep(0.5)
            conn.send(message.encode(FORMAT))  # send the printing
            time.sleep(0.2)

            print("This round took ", moves_counter, "moves")
            message = "This round took " + str(moves_counter) + "moves"
            conn.send(message.encode(FORMAT))  # send the printing
            time.sleep(0.2)

            print("Total victories of player 1: ", victories_counter1)
            message = "Total victories of player 1: " + str(victories_counter1)
            conn.send(message.encode(FORMAT))  # send the printing
            time.sleep(0.2)

            print("Total victories of player 2: ", victories_counter2)
            message = "Total victories of player 2: " + str(victories_counter2)
            conn.send(message.encode(FORMAT))  # send the printing
            time.sleep(0.2)

            # check leading player:
            if victories_counter1 > victories_counter2:
                print("Leading player: player 1\nplayer 1 will need ", victories_num - victories_counter1,
                      " more victories to win\n")
                message = "Leading player: player 1\nplayer 1 will need " + str(victories_num - victories_counter1)\
                          + " more victories to win"
            elif victories_counter1 < victories_counter2:
                print("Leading player: player 2\nplayer 2 will need ", victories_num - victories_counter2,
                      " more victories to win")
                message = "Leading player: player 2\nplayer 2 will need " + str(victories_num - victories_counter2) \
                          + " more victories to win\n"
            else:
                print("theres a tie! You both need ", victories_num - victories_counter2, " more victories to win")
                message = "theres a tie! You both need " + str(victories_num - victories_counter2)\
                          + " more victories to win\n"
            conn.send(message.encode(FORMAT))  # send the printing
            time.sleep(0.2)

            #check if the game is over:
            finish_game = 0
            if victories_counter1 == victories_num or victories_counter2 == victories_num:
                finish_game = 1  # raise flag
            time.sleep(1)
            conn.send(str(finish_game).encode(FORMAT))  # send flag
            time.sleep(0.2)

        # end of game:
        is_playing = 1
        print("\nGAME OVER!")
        time.sleep(0.5)

        # find winner:
        if victories_counter1 > victories_counter2:
            print("The winner is: player 1!!!")
            winner = "The winner is: player 1!!!"
            conn.send(winner.encode(FORMAT))  # send the printing
            time.sleep(0.2)
        elif victories_counter1 < victories_counter2:
            print("The winner is: player 2!!!")
            winner = "The winner is: player 2!!!"
            conn.send(winner.encode(FORMAT))  # send the printing
            time.sleep(0.2)

        #send game summary to client:
        message = "Summery of the game:"
        conn.send(message.encode(FORMAT))  # send the printing
        print("Summery of the game:")
        time.sleep(0.2)

        message = "Total victories of player 1: " + str(victories_counter1)
        conn.send(message.encode(FORMAT))  # send the printing
        print("Total victories of player 1: ", victories_counter1)
        time.sleep(0.2)

        message = "Total victories of player 2: " + str(victories_counter2)
        conn.send(message.encode(FORMAT))  # send the printing
        print("Total victories of player 2: ", victories_counter2)
        time.sleep(0.2)

        message = "The longest game took: " + str(max_steps_game) + "moves"
        conn.send(message.encode(FORMAT))  # send the printing
        print("The longest game took ", max_steps_game, "moves")
        time.sleep(0.2)

        rounds = victories_counter1 + victories_counter2
        message = "Total rounds in the game: " + str(rounds)
        conn.send(message.encode(FORMAT))  # send the printing
        print("Total rounds in the game:", rounds)

        print()


# Main
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())  # finding your current IP address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Server socket

    print("[STARTING] server is starting...")
    start_server()
    game() # start game
    print("THE END!")

import socket
import time
import pickle
import numpy as np

# Mor and Revital 314616095 & 315406223

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 60000  # The port used by the server
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


def start_client(): # start client function:
    # check if new game:

    client_socket.connect((HOST, PORT))  # Connecting to server's socket

    active_flag = int(client_socket.recv(1024))
    if active_flag == 0:
        print("\nThere are too many players in the game\n [CLOSING CONNECTION] client closed socket!")
        return
        # client_socket.close()  # Closing client's connection with server (<=> closing socket)

    is_playing = int(input("Welcome to Connect Four!\nDo you want to play?  no(1) or play against computer (2) "))

    while is_playing != 1 and is_playing != 2:  # if input isn't available:
        is_playing = int(input("Please choose an available value:1 to leave game, 2 to play"))  # ask again from client

    print(is_playing)
    client_socket.send(str(is_playing).encode(FORMAT))  # send  player's choice

    i = 0
    turn = 0
    if is_playing != 1: # if the player wants to play
        game_mode = int(input("Choose a legal game level: easy (1) or hard (2)")) # get game_mode from player:
        while game_mode != 1 and game_mode != 2: # if game mode isn't available, get a new one
            game_mode = int(input("Unavailable input. Please choose a legal game level: easy (1) or hard (2)"))

        client_socket.send(str(game_mode).encode(FORMAT)) # send game_mode to server
        err_counter = 1
        victories_num = int(input("How many victories does it take to win? "))  # get victories_num from player:
        while victories_num < 1: # if victories num isn't available, get a new one from player
            victories_num = int(input("PLease enter a number bigger than 0. How many victories does it take to win?"))
            err_counter += 1
            if (err_counter % 5) == 0:
                print("You inserted wrong input ", err_counter, "times. wait ",60 * (err_counter / 5), "seconds")
                time.sleep(60 * (err_counter / 5)) # delay every fifth wrong output, multiplied by 2 every 5 mistakes
        client_socket.send(str(victories_num).encode(FORMAT))  # send victories_num to server

        # get col from player:
        round_over = 0
        finish_game = 0
        while finish_game != 1: # while game isn't over
            print("\n A new round has begun, may the odds be ever in your favor!")
            pickled_board = client_socket.recv(1024)  # receive board from server
            board = pickle.loads(pickled_board)
            print(np.flip(board, 0))  # print board
            turn = 0  # flags
            round_over = 0

            while round_over != 1:  # while round isn't over
                if turn == 0: # player's turn:
                    row = -1
                    while row == -1: # ask for column
                        col = int(input("Please choose a column between 0-6: "))
                        while col > 6 or col < 0:  # if column isn't available get a new one
                            col = int(input("You chose an unavailable column. Please choose a column between 0-6: "))
                        client_socket.send(str(col).encode(FORMAT)) # send chosen column
                        players_choice_m1 = client_socket.recv(1024).decode(FORMAT)  # Receiving player's choice from server
                        print(players_choice_m1)
                        row = int(client_socket.recv(1024).decode(FORMAT))  # Receiving row from server
                        if row == -1: # if no available row:
                            print("You chose an unavailable column, it's already full")
                else: # Receiving computer's choice from server
                    players_choice_m2 = client_socket.recv(1024).decode(FORMAT)
                    print(players_choice_m2)
                turn += 1  # update turns
                turn = turn % 2

                # receive& print board
                pickled_board = client_socket.recv(1024)
                board = pickle.loads(pickled_board)
                print(np.flip(board, 0))
                # get round_over flag from server
                round_over = int(client_socket.recv(1024).decode(FORMAT))
            # after round is over:
            # Receive round summary
            for i in range(5):
                message = client_socket.recv(1024).decode(FORMAT)  # Receive round summary
                print(message)
            # get finish_game flag from server
            finish_game = int(client_socket.recv(1024).decode(FORMAT))
    # END OF GAME
    if is_playing != 1:
        winner = client_socket.recv(1024).decode(FORMAT)  # Receiving data from server
        print(winner)
        print("\n")

        # get & print game summary:
        for i in range(5):
            message = client_socket.recv(1024).decode(FORMAT)
            print(message)

    if is_playing == 1: # if the player doesn't want to play:
        print("Too bad, see you next time!")

    client_socket.close()  # Closing client's connection with server (<=> closing socket)
    print("\n[CLOSING CONNECTION] client closed socket!")


if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[CLIENT] Started running")
    start_client()
    print("\nGoodbye client:)")
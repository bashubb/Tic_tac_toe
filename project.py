import getpass
import random
import sqlite3
import sys
import os
import time
from werkzeug.security import check_password_hash, generate_password_hash

import pyfiglet
from prettytable import PrettyTable
from rich import print as rprint
from rich.panel import Panel
from simple_term_menu import TerminalMenu


# =================================== CREATE NEW DATA BASE

# Connect to the SQLite database
conn = sqlite3.connect('tic_tac_toe.db')
cursor = conn.cursor()

# Create a table for user information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Create a table for game statistics
cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_statistics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        result TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()


#==================================== global variables
NUM_SQUARES = 9
EMPTY = " "
draw = "draw"
O = 'O'
X = 'X'
hello_instructions = pyfiglet.figlet_format("Tic Tac Toe")


#=================================== DATA BASE FUNCTIONS

def get_user_from_database(cursor, username):
    """Retrieve user information from the database."""
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    return cursor.fetchone()


def save_game_statistics(username, result):
    """Save game statistics to the database."""
    if result is None:
        result = 'draw'  # Provide a default value for no winner

    conn = sqlite3.connect('tic_tac_toe.db')
    cursor = conn.cursor()

    user_id = get_user_id(username)
    cursor.execute('INSERT INTO game_statistics (user_id, result) VALUES (?, ?)', (user_id, result))

    conn.commit()
    conn.close()


def get_user_id(username):
    """Retrieve the user ID from the database."""
    conn = sqlite3.connect('tic_tac_toe.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user_id = cursor.fetchone()
    return user_id[0] if user_id else None



# =================================== MENU


def menu(*args, title=""):
    options = (args)
    terminal_menu = TerminalMenu(options, title=title)
    menu_entry_index = terminal_menu.show()
    return options[menu_entry_index]


def main_menu():
    main_menu_choice = menu("Play as guest", "Log in", "Sign in", "Exit")

    if main_menu_choice == "Play as guest":
        #play as a guest
        username = "Guest"
    elif main_menu_choice == "Log in" :
        #play as a logged user
        username = login()
    elif main_menu_choice == "Sign in" :
        #play as a logged user
        username = register()
    else:
        sys.exit(pyfiglet.figlet_format("Bye !"))

    game_loop(username)
    os.system('clear')



# =================================== MAIN FUNCTIONS


def game_loop(username):
    if username != "Guest":
        rprint(f"\n[bold yellow]Hi {username}, choose what you want to do ![/bold yellow]\n")
        chosen_option = menu("Play new game", "Show statistics")
        if chosen_option == "Show statistics":
            display_game_statistics(username)
    try:
        play_again = None
        while play_again != "No":
            # define who is making first move
            computer = {"name": "computer"}
            human = {"name": username}
            computer, human = first_move(computer, human)
            turn = X
            #create empty board
            board = new_board()
            time.sleep(2)

            while not winner(board):
                #display actual board

                if turn == human["symbol"]:
                    display_board(board, human["name"])
                    move = human_move(board, human)
                    board[move] = human["symbol"]
                    display_board(board, human["name"])

                else:
                    display_board(board, computer["name"])
                    move = computer_move(board, computer, human)
                    time.sleep(2)
                    board[move] = computer["symbol"]
                    display_board(board, computer["name"])

                time.sleep(3)
                turn = next_turn(turn)

            the_winner = the_winner_display(computer, human, winner(board))
            congrat_winner(the_winner, computer, human)

            # Save game statistics to the database
            if username != "Guest":
                if the_winner == username:
                    result = "win"
                elif the_winner == "computer":
                    result = "lose"
                else:
                    result = the_winner
                save_game_statistics(username, result)

                show_statistics = menu("Yes","No", title="Do you want to see your statistics ?")
                if show_statistics == "Yes":
                    display_game_statistics(username)

            play_again = menu("Yes", "No", title="Do you want to play again ?")

    except EOFError:
        os.system("clear")
        sys.exit(pyfiglet.figlet_format("Bye !"))


def main():
    os.system('clear')
    display_hello()
    # Option to play as a guest or register/login
    time.sleep(3)
    #Menu - guest, log in ,sign in
    main_menu()


# =================================== DISPLAY FUNCTIONS


def display_hello():
    """Display instructions for the game """
    print()
    print()
    rprint(Panel.fit(f'''[red]{hello_instructions} [/red]
                    [bold red]Hello![/bold red]
                    [italic]This is a game of tic-tac-toe. I invite you to play a game between 
                    me - the computer and you - the human.
                    Your move will be indicated by selecting a field number on the board,
                    which looks like this:[/italic]


                            0 | 1 | 2
                            ---------
                            3 | 4 | 5
                            ---------
                            6 | 7 | 8



                   [italic]I hope you're ready to fail :)[/italic] [bold red]Let's get started![/bold red]

          '''))
    print()
    print()


def display_board(board, turn):
    '''Display the board on the screen'''
    os.system("clear")
    rprint(Panel.fit(f'''





                 {board[0]} | {board[1]} | {board[2]}       0 | 1 | 2
                -----------      ---------
                 {board[3]} | {board[4]} | {board[5]}       3 | 4 | 5
                -----------      ---------
                 {board[6]} | {board[7]} | {board[8]}       6 | 7 | 8






                                                            ''',title=f"Turn: [yellow]{turn}[/yellow]", subtitle="For exit press Control+D"))


def computer_image(message):
    rprint(f'''
     _______________
    |  ___________  |
    | |    \\ /    | |
    | |   [red bold]0   0[/red bold]   | |           [italic bold]{message}[/italic bold]
    | |     -     | |
    | |    ___    | |
    | |___     ___| |
    |_____|\\_/|_____|
      _|__|/ \\|_|_
     / **********   \\
    /  ************  \\
   -------------------
    ''')


def display_game_statistics(username):
    """Function to display game statistics"""
    # Connect to the SQLite database
    conn = sqlite3.connect('tic_tac_toe.db')
    cursor = conn.cursor()

    user_id = get_user_id(username)
    if user_id is not None:
        cursor.execute('''
            SELECT result FROM game_statistics WHERE user_id = ?
        ''', (user_id,))
        results = cursor.fetchall()
        # Close the database connection
        conn.close()
        # Count the number of wins, losses, and draws
        wins = results.count(('win',))
        losses = results.count(('lose',))
        draws = results.count(('draw',))

        # Display the statistics in a table
        table = PrettyTable()
        table.field_names = ["Outcome", "Count"]
        table.add_row(["Wins", wins])
        table.add_row(["Losses", losses])
        table.add_row(["Draws", draws])

        os.system("clear")
        rprint(f'''
                    [bold yellow]---------- Statistics ----------[/bold yellow]

          ''')
        print(f"Game Statistics for {username}:")
        print()
        print(table)
        print()
        menu_choice = menu("Back to the game", "Exit from a game")
        if menu_choice == "Back to the game":
            time.sleep(2)
            return
        elif menu_choice == "Exit from a game":
            os.system('clear')
            sys.exit(pyfiglet.figlet_format("Bye !"))
    else:
        print(f"User {username} not found.")


def congrat_winner(the_winner, computer, human):
    '''Congratulate the winner'''
    if the_winner != draw:
        if the_winner == computer['name']:
            rprint(f'''
                    [bold yellow]---------- Computer wins! ----------[/bold yellow]

            ''')
            print()
            print()
            computer_image('As I thought, there can only be one winner, once again you can\'t compare to me!')
        elif the_winner == human['name']:
            rprint(f'''
                    [bold yellow]---------- {the_winner} You are the winner ! ----------[/bold yellow]

            ''')
            print()
            print()
            computer_image('Somehow you managed to win! Enjoy it, it was probably the last time!')
    else:
        rprint(f'''
                    [bold yellow]---------- Draw ! ----------[/bold yellow]

            ''')
        print()
        print()
        computer_image('You were very lucky, or I had a bad day, you managed to draw!')




# =================================== LOGIN/REGISTER


def login():
    os.system("clear")
    rprint(f'''
                    [bold yellow]---------- Log In ----------[/bold yellow]

          ''')
    logged_in = False
    while logged_in == False:
        try:
            # conntect to the data base
            conn = sqlite3.connect('tic_tac_toe.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Ensure username was submitted
            username = input("\n\t\tEnter your username: ")
            # Ensure password was submitted
            password = getpass.getpass("\n\t\tEnter your password: ")
            # Query database for username
            fetched_user = get_user_from_database(cursor, username)
            # Ensure username exists and password is correct
            if not fetched_user or not check_password_hash(fetched_user["password"], password):
                rprint("\n\t\t[bold red]Username or password is invalid [/bold red]\n")
                # menu
                menu_choice = menu("Try again", "Back to main menu", "Exit from a game")
                if menu_choice == "Try again":
                    continue
                elif menu_choice == "Back to main menu":
                    main_menu()
                elif menu_choice == "Exit from a game":
                    os.system('clear')
                    sys.exit(pyfiglet.figlet_format("Bye !"))
            rprint("[bold yellow]\nSuccessfully logged in![/bold yellow]\n")
            time.sleep(2)
            logged_in = True
            os.system('clear')
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

        finally:
            conn.close()

    return username


def register():
    #Some UI
    os.system("clear")
    rprint(f'''
                    [bold yellow]---------- Sign In ----------[/bold yellow]

          ''')
    registered = False
    while registered == False:
        try:
            #connecto to the data base
            conn = sqlite3.connect('tic_tac_toe.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Ensure username was submitted
            username = input("\n\t\tEnter your username: ")
            # Ensure passwod and confirmation match
            password = get_matching_password()
            # Query database for username
            fetched_user = get_user_from_database(cursor, username)
            # Ensure username does not already exist
            if fetched_user:
                print("\n\t\tThis username is already taken")
                # menu
                menu_choice = menu("Try again", "Back to main menu", "Exit from a game")
                if menu_choice == "Try again":
                    continue
                elif menu_choice == "Back to main menu":
                    main_menu()
                elif menu_choice == "Exit from a game":
                    os.system('clear')
                    sys.exit(pyfiglet.figlet_format("Bye !"))
            else:
                # Insert user into a database
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, generate_password_hash(password)))
                # commit changes into database
                conn.commit()
                registered = True
                rprint("[bold yellow]\nSuccessfully registered and logged in![/bold yellow]\n")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

        finally:
            conn.close()

    return username


def get_matching_password():
    """Ask the user to enter and confirm a password, ensuring they match."""
    while True:
        password = getpass.getpass("\n\t\tEnter your password: ")
        confirm_password = getpass.getpass("\n\t\tConfirm your password: ")

        if password == confirm_password:
            return password
        else:
            rprint("\n\t\t[bold red]Passwords do not match. Please try again.[/bold red]")
            menu_choice = menu("Try again", "Back to main menu", "Exit from a game")
            if menu_choice == "Try again":
                continue
            elif menu_choice == "Back to main menu":
                main_menu()
            elif menu_choice == "Exit from a game":
                os.system('clear')
                sys.exit(pyfiglet.figlet_format("Bye !"))



# =================================== GAME LOGIC

def ask_number(question, low, high):
    '''Ask for a digit in a given range '''
    response = None
    while response not in range (low,high+1):
        try:
            response = int(input(question))
        except ValueError:
            rprint("\n\t\t[bold red]You did not enter a number, Please try again![/bold red]")
    return response


def first_move(computer,human):
    '''Determine who has the first move '''
    os.system("clear")
    print()
    rprint("[bold yellow]Do You want to make first move ?[/bold yellow]")
    print()
    go_first = menu("Yes", "No")
    if go_first == "Yes":
        rprint('\t\t[italic]The first move is yours, player![/italic]')
        human["symbol"] = X
        computer["symbol"] = O
    else:
        rprint('\t\t[italic]Ok, so here I go. Get ready, player ![/italic]')
        human["symbol"] = O
        computer["symbol"] = X
    return computer, human


def new_board():
    '''Create a new game board'''
    board = []
    for _ in range(NUM_SQUARES):
        board.append(EMPTY)
    return board


def legal_moves(board):
    '''Create a list of correct moves '''
    moves = []
    for square in range(NUM_SQUARES):
        if board[square] == EMPTY:
            moves.append(square)
    return moves


def winner(board):
    '''Determine the winner '''
    WAYS_TO_WIN = ((0,1,2),
                   (3,4,5),
                   (6,7,8),
                   (0,3,6),
                   (1,4,7),
                   (2,5,8),
                   (0,4,8),
                   (2,4,6))
    for row in WAYS_TO_WIN:
        if board[row[0]] == board[row[1]] == board[row[2]] != EMPTY:
            winning_player_symbol = board[row[0]]
            return winning_player_symbol

    if EMPTY not in board:
        return draw

    return None


def human_move(board, human):
    '''Read human movement'''
    legal = legal_moves(board)
    move = None
    while move not in legal:
        move = ask_number('\n\t\tWhat will your move be? (0-8): ', 0, NUM_SQUARES)
        if move not in legal:
            rprint("\n[red bold]This field is already taken, choose another field[/red bold]")
    rprint("\n[italic]Very nicely[/italic]")
    return move


def computer_move(board, computer, human):
    '''Have the computer select a move'''
    # Create a working copy because the function will manipulate the list
    board = board[:]

    # Best items to create in order
    BEST_MOVES = (4, 9, 2, 6, 8, 1, 3, 5, 7)

    rprint("\n\n[italic]I select field number[/italic]", end=" ")

    # Introduce a chance for the computer to make a random move
    if random.random() < 0.15:
        legal_moves_list = legal_moves(board)
        random_move = random.choice(legal_moves_list)
        print(random_move)
        return random_move

    # Check whether a given move will win the computer
    for move in legal_moves(board):
        board[move] = computer['symbol']
        if winner(board) == computer['symbol']:
            print(move)
            return move
        # This move has been checked; withdraw it to match the next one
        board[move] = EMPTY

    # If the human can win, block this move
    for move in legal_moves(board):
        board[move] = human['symbol']
        if winner(board) == human['symbol']:
            print(move)
            return move
        # This move has been checked; withdraw it to make another one
        board[move] = EMPTY

    for move in BEST_MOVES:
        if move in legal_moves(board):
            print(move)
            return move


def next_turn(turn):
    '''Replace the movers'''
    if turn == X:
        return O
    else:
        return X


def the_winner_display (computer, human, winner_symbol):
    the_winner = None
    if winner_symbol == computer['symbol']:
        the_winner = computer['name']
    elif winner_symbol == human['symbol']:
        the_winner = human['name']
    else:
        the_winner = winner_symbol
    return the_winner




if __name__ == "__main__":
    main()

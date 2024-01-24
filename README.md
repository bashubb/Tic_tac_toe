Tic Tac Toe with Python 
==========================

About
-----

Welcome to my Tic Tac Toe project for CS50 with Python! 🚀 I've crafted this game to bring the classic Tic Tac Toe experience to your computer. Whether you're playing against a friend or challenging the computer, get ready for some fun and strategic gaming!

Features 🌟
-----------

-   **User Friendly:** Log in, register, or play as a guest to enjoy the game.
-   **Stats Tracker:** Keep tabs on your wins, losses, and draws.
-   **Single-Player Mode:** Test your skills against the computer.
-   **Clean UI:** Enjoy a clear and visually appealing interface.

Tech Stack 🛠️
--------------

-   Python
-   SQLite3 (For user authentication and game statistics)
-   External Libraries:
    -   pyfiglet: Adds a cool title
    -   prettytable: Displays game statistics
    -   rich: Enhances console printing
    -   simple-term-menu: Creates terminal menus

Installation 🚀
---------------

1.  Clone the repository: `git clone "https://github.com/bashubb/Tic_tac_toe.git"`
2.  Navigate to the project directory: `cd Tic_Tac_Toe`
3.  Install required libraries: `python3 -m pip install -r requirements.txt`
4.  Run the game: `python3 project.py`

How to Play 🕹️
---------------

1.  Run `project.py`.
2.  Choose an option: Play as guest, Log in, Sign in, or Exit.
3.  Follow the prompts and make your moves.
4.  Enjoy the game and track your stats!

Database Structure 🗃️
----------------------

The game uses SQLite (`tic_tac_toe.db`) with two tables:

-   `users`: Stores user info (id, username, password).
-   `game_statistics`: Records game results (id, user_id, result).

Credits 🙌
----------

- [pyfiglet](https://github.com/pwaller/pyfiglet)
- [prettytable](https://github.com/dprince/python-prettytable)
- [rich](https://github.com/willmcgugan/rich)
- [simple-term-menu](https://github.com/an2if4/simple-term-menu)


Example Usage 📺
----------------

Check out how to play on [YouTube!](https://youtu.be/5jw8xzq1nQo?si=ErUoxW3BfiPiss9A)


Feel free to explore the code, make improvements, and share the game with others. Happy gaming!

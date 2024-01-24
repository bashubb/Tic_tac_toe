import unittest
from unittest.mock import patch
from io import StringIO

# Import functions to test
from project import (
    new_board,
    legal_moves,
    winner,
    next_turn,
)

def test_new_board():
    board = new_board()
    assert len(board) == 9
    assert board.count(" ") == 9

def test_legal_moves():
    board = ["X", "O", " ", " ", "X", "O", " ", " ", " "]
    moves = legal_moves(board)
    assert moves == [2, 3, 6, 7, 8]

def test_winner():
    # Test horizontal win
    board = ["X", "X", "X", " ", "O", "O", " ", " ", " "]
    assert winner(board) == "X"

    # Test vertical win
    board = ["X", "O", " ", "X", "O", " ", "X", " ", "O"]
    assert winner(board) == "X"

    # Test diagonal win
    board = ["X", "O", " ", "O", "X", " ", " ", " ", "X"]
    assert winner(board) == "X"


def test_next_turn():
    assert next_turn("X") == "O"
    assert next_turn("O") == "X"



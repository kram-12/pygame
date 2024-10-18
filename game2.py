import numpy as np
import random

# Color definitions
COLOR_RED = 1
COLOR_YELLOW = 2
EMPTY_SLOT = 0

# Dimensions of the board
NUM_ROWS = 6
NUM_COLUMNS = 7

# Number of pieces required to win
WIN_SEQUENCE = 4

class Game:
    def __init__(self, id):
        self.board = self.initialize_board()
        self.current_turn = random.randint(0, 1)  # 0 for HUMAN, 1 for AI
        self.game_over = False
        self.id = id
        self.ready = False

    def initialize_board(self):
        return np.zeros((NUM_ROWS, NUM_COLUMNS))

    def play(self, player, column):
        if not self.is_column_available(column) or self.game_over:
            return
        row = self.get_available_row(column)
        self.place_piece(row, column, COLOR_RED if player == 0 else COLOR_YELLOW)
        
        if self.is_winning_move(COLOR_RED if player == 0 else COLOR_YELLOW):
            self.game_over = True

        self.current_turn = 1 - self.current_turn  # Switch turns

    def reset(self):
        self.board = self.initialize_board()
        self.current_turn = random.randint(0, 1)
        self.game_over = False

    def is_column_available(self, col):
        return self.board[NUM_ROWS - 1][col] == EMPTY_SLOT

    def get_available_row(self, col):
        for r in range(NUM_ROWS):
            if self.board[r][col] == EMPTY_SLOT:
                return r

    def place_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_winning_move(self, piece):
        return self.check_horizontal(piece) or self.check_vertical(piece) or self.check_diagonal(piece)

    def check_horizontal(self, piece):
        for c in range(NUM_COLUMNS - 3):
            for r in range(NUM_ROWS):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and self.board[r][c + 3] == piece:
                    return True
        return False

    def check_vertical(self, piece):
        for c in range(NUM_COLUMNS):
            for r in range(NUM_ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and self.board[r + 3][c] == piece:
                    return True
        return False

    def check_diagonal(self, piece):
        for c in range(NUM_COLUMNS - 3):
            for r in range(NUM_ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    return True
        for c in range(NUM_COLUMNS - 3):
            for r in range(3, NUM_ROWS):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    return True
        return False

    def get_board(self):
        return self.board

    def connected(self):
        return self.ready

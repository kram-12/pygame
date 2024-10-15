import numpy as np # type: ignore
import random
import pygame
import sys
import math

# Color definitions
COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)

# Dimensions of the board
NUM_ROWS = 6
NUM_COLUMNS = 7

# Constants for the players
HUMAN_PLAYER = 0
AI_PLAYER = 1

# Constants for empty, human, and AI pieces
EMPTY_SLOT = 0
HUMAN_PIECE = 1
AI_PIECE = 2

# Number of pieces required to win
WIN_SEQUENCE = 4

# Function to create an empty game board
def initialize_board():
    board = np.zeros((NUM_ROWS, NUM_COLUMNS))
    return board

# Function to place a piece in the specified row and column
def place_piece(board, row, col, piece):
    board[row][col] = piece

# Function to check if a column is available for a move
def is_column_available(board, col):
    return board[NUM_ROWS - 1][col] == 0

# Function to get the first open row in a column
def get_available_row(board, col):
    for r in range(NUM_ROWS):
        if board[r][col] == 0:
            return r

# Function to print the board in the terminal (for debugging)
def display_board(board):
    print(np.flip(board, 0))

# Function to check for a winning move
def is_winning_move(board, piece):
    # Check horizontal conditions
    for c in range(NUM_COLUMNS - 3):
        for r in range(NUM_ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical conditions
    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLUMNS - 3):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLUMNS - 3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Function to evaluate a section of the board for scoring
def evaluate_sequence(window, piece):
    score = 0
    opponent_piece = HUMAN_PIECE
    if piece == HUMAN_PIECE:
        opponent_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY_SLOT) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY_SLOT) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(EMPTY_SLOT) == 1:
        score -= 4

    return score

# Function to score the current board state
def score_board(board, piece):
    score = 0

    # Score center column
    center_column = [int(i) for i in list(board[:, NUM_COLUMNS//2])]
    center_count = center_column.count(piece)
    score += center_count * 3

    # Score horizontal sequences
    for r in range(NUM_ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(NUM_COLUMNS - 3):
            window = row_array[c:c + WIN_SEQUENCE]
            score += evaluate_sequence(window, piece)

    # Score vertical sequences
    for c in range(NUM_COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(NUM_ROWS - 3):
            window = col_array[r:r + WIN_SEQUENCE]
            score += evaluate_sequence(window, piece)

    # Score positively sloped diagonals
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLUMNS - 3):
            window = [board[r+i][c+i] for i in range(WIN_SEQUENCE)]
            score += evaluate_sequence(window, piece)

    # Score negatively sloped diagonals
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLUMNS - 3):
            window = [board[r+3-i][c+i] for i in range(WIN_SEQUENCE)]
            score += evaluate_sequence(window, piece)

    return score

# Function to check if the board state is terminal (win or draw)
def is_game_over(board):
    return is_winning_move(board, HUMAN_PIECE) or is_winning_move(board, AI_PIECE) or len(get_available_columns(board)) == 0

# Minimax algorithm to determine the best move for the AI
def minimax(board, depth, alpha, beta, maximizing_player):
    valid_columns = get_available_columns(board)
    is_terminal = is_game_over(board)
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if is_winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif is_winning_move(board, HUMAN_PIECE):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_board(board, AI_PIECE))
    
    if maximizing_player:
        value = -math.inf
        selected_column = random.choice(valid_columns)
        for col in valid_columns:
            row = get_available_row(board, col)
            temp_board = board.copy()
            place_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                selected_column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return selected_column, value

    else:  # Minimizing player
        value = math.inf
        selected_column = random.choice(valid_columns)
        for col in valid_columns:
            row = get_available_row(board, col)
            temp_board = board.copy()
            place_piece(temp_board, row, col, HUMAN_PIECE)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                selected_column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return selected_column, value

# Function to get available columns for moves
def get_available_columns(board):
    valid_columns = []
    for col in range(NUM_COLUMNS):
        if is_column_available(board, col):
            valid_columns.append(col)
    return valid_columns

# Function to render the game board using Pygame
def render_board(board):
    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS):
            pygame.draw.rect(screen, COLOR_BLUE, (c * CELL_SIZE, r * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, COLOR_BLACK, (int(c * CELL_SIZE + CELL_SIZE / 2), int(r * CELL_SIZE + CELL_SIZE + CELL_SIZE / 2)), RADIUS)
    
    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS):
            if board[r][c] == HUMAN_PIECE:
                pygame.draw.circle(screen, COLOR_RED, (int(c * CELL_SIZE + CELL_SIZE / 2), height - int(r * CELL_SIZE + CELL_SIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, COLOR_YELLOW, (int(c * CELL_SIZE + CELL_SIZE / 2), height - int(r * CELL_SIZE + CELL_SIZE / 2)), RADIUS)
    pygame.display.update()

# Initialize Pygame and board setup
board = initialize_board()
display_board(board)
game_over = False

pygame.init()

CELL_SIZE = 100
width = NUM_COLUMNS * CELL_SIZE
height = (NUM_ROWS + 1) * CELL_SIZE
RADIUS = int(CELL_SIZE / 2 - 5)

screen = pygame.display.set_mode((width, height))
render_board(board)
pygame.display.update()

font = pygame.font.SysFont("monospace", 75)
current_turn = random.randint(HUMAN_PLAYER, AI_PLAYER)

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, width, CELL_SIZE))
            mouse_x = event.pos[0]
            if current_turn == HUMAN_PLAYER:
                pygame.draw.circle(screen, COLOR_RED, (mouse_x, int(CELL_SIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, width, CELL_SIZE))

            if current_turn == HUMAN_PLAYER:
                mouse_x = event.pos[0]
                selected_col = int(math.floor(mouse_x / CELL_SIZE))

                if is_column_available(board, selected_col):
                    selected_row = get_available_row(board, selected_col)
                    place_piece(board, selected_row, selected_col, HUMAN_PIECE)

                    if is_winning_move(board, HUMAN_PIECE):
                        label = font.render("Player wins!!", 1, COLOR_RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    current_turn += 1
                    current_turn = current_turn % 2

                    display_board(board)
                    render_board(board)

    # AI turn
    if current_turn == AI_PLAYER and not game_over:
        selected_col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if is_column_available(board, selected_col):
            selected_row = get_available_row(board, selected_col)
            place_piece(board, selected_row, selected_col, AI_PIECE)

            if is_winning_move(board, AI_PIECE):
                label = font.render("AI wins!!", 1, COLOR_YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            display_board(board)
            render_board(board)

            current_turn += 1
            current_turn = current_turn % 2

    if game_over:
        pygame.time.wait(3000)

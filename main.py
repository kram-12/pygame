import numpy as np
import pygame
import sys
import math

# Color definitions
COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)

# Dimensions for the board
NUM_ROWS = 6
NUM_COLUMNS = 7

# Function to initialize the game board
def initialize_board():
    # Create a 6x7 grid filled with zeros (empty slots)
    board = np.zeros((NUM_ROWS, NUM_COLUMNS))
    return board

# Function to place a piece on the board
def place_piece(board, row, col, player_piece):
    board[row][col] = player_piece

# Function to check if a column has space for a piece
def is_column_valid(board, col):
    return board[NUM_ROWS - 1][col] == 0

# Get the next available row in the selected column
def get_open_row(board, col):
    for r in range(NUM_ROWS):
        if board[r][col] == 0:
            return r

# Function to display the board (for terminal debugging)
def display_board(board):
    print(np.flip(board, 0))

# Function to check if the current move leads to a win
def check_winning_move(board, player_piece):
    # Check horizontal win conditions
    for col in range(NUM_COLUMNS - 3):
        for row in range(NUM_ROWS):
            if board[row][col] == player_piece and board[row][col+1] == player_piece and board[row][col+2] == player_piece and board[row][col+3] == player_piece:
                return True

    # Check vertical win conditions
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == player_piece and board[row+1][col] == player_piece and board[row+2][col] == player_piece and board[row+3][col] == player_piece:
                return True

    # Check diagonals (positive slope)
    for col in range(NUM_COLUMNS - 3):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == player_piece and board[row+1][col+1] == player_piece and board[row+2][col+2] == player_piece and board[row+3][col+3] == player_piece:
                return True

    # Check diagonals (negative slope)
    for col in range(NUM_COLUMNS - 3):
        for row in range(3, NUM_ROWS):
            if board[row][col] == player_piece and board[row-1][col+1] == player_piece and board[row-2][col+2] == player_piece and board[row-3][col+3] == player_piece:
                return True

# Function to render the game board visually using Pygame
def render_board(board):
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS):
            # Draw the grid
            pygame.draw.rect(screen, COLOR_BLUE, (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # Draw the empty circles (black)
            pygame.draw.circle(screen, COLOR_BLACK, (int(col * CELL_SIZE + CELL_SIZE / 2), int(row * CELL_SIZE + CELL_SIZE + CELL_SIZE / 2)), RADIUS)
    
    # Draw the pieces (Red for player 1, Yellow for player 2)
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS):        
            if board[row][col] == 1:
                pygame.draw.circle(screen, COLOR_RED, (int(col * CELL_SIZE + CELL_SIZE / 2), height - int(row * CELL_SIZE + CELL_SIZE / 2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, COLOR_YELLOW, (int(col * CELL_SIZE + CELL_SIZE / 2), height - int(row * CELL_SIZE + CELL_SIZE / 2)), RADIUS)
    pygame.display.update()

# Initialize the game board
game_board = initialize_board()
display_board(game_board)
game_is_over = False
current_turn = 0

# Initialize Pygame
pygame.init()

CELL_SIZE = 100
width = NUM_COLUMNS * CELL_SIZE
height = (NUM_ROWS + 1) * CELL_SIZE

# Set window size and radius for pieces
screen = pygame.display.set_mode((width, height))
RADIUS = int(CELL_SIZE / 2 - 5)

# Draw the initial empty board
render_board(game_board)
pygame.display.update()

# Set font for win messages
font = pygame.font.SysFont("monospace", 75)

# Main game loop
while not game_is_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Handle mouse movement to show the piece hovering over the board
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, width, CELL_SIZE))
            mouse_x = event.pos[0]
            if current_turn == 0:
                pygame.draw.circle(screen, COLOR_RED, (mouse_x, int(CELL_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, COLOR_YELLOW, (mouse_x, int(CELL_SIZE / 2)), RADIUS)
        pygame.display.update()

        # Handle mouse click to place the piece
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, width, CELL_SIZE))
            
            # Player 1's turn
            if current_turn == 0:
                mouse_x = event.pos[0]
                selected_col = int(math.floor(mouse_x / CELL_SIZE))

                if is_column_valid(game_board, selected_col):
                    open_row = get_open_row(game_board, selected_col)
                    place_piece(game_board, open_row, selected_col, 1)

                    if check_winning_move(game_board, 1):
                        label = font.render("Player 1 wins!!", 1, COLOR_RED)
                        screen.blit(label, (40, 10))
                        game_is_over = True

            # Player 2's turn
            else:
                mouse_x = event.pos[0]
                selected_col = int(math.floor(mouse_x / CELL_SIZE))

                if is_column_valid(game_board, selected_col):
                    open_row = get_open_row(game_board, selected_col)
                    place_piece(game_board, open_row, selected_col, 2)

                    if check_winning_move(game_board, 2):
                        label = font.render("Player 2 wins!!", 1, COLOR_YELLOW)
                        screen.blit(label, (40, 10))
                        game_is_over = True

            display_board(game_board)
            render_board(game_board)

            # Switch turn
            current_turn += 1
            current_turn %= 2

            # Pause when the game is over
            if game_is_over:
                pygame.time.wait(3000)

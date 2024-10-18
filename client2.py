import pygame
import sys
from network2 import Network
import numpy as np
import math

# Color definitions
COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)

# Dimensions of the board
NUM_ROWS = 6
NUM_COLUMNS = 7
CELL_SIZE = 100
RADIUS = int(CELL_SIZE / 2 - 5)

# Initialize Pygame
pygame.init()
width = NUM_COLUMNS * CELL_SIZE
height = (NUM_ROWS + 1) * CELL_SIZE
screen = pygame.display.set_mode((width, height))

def render_board(board):
    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS):
            pygame.draw.rect(screen, COLOR_BLUE, (c * CELL_SIZE, r * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, COLOR_BLACK, (int(c * CELL_SIZE + CELL_SIZE / 2), int(r * CELL_SIZE + CELL_SIZE + CELL_SIZE / 2)), RADIUS)

    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, COLOR_RED, (int(c * CELL_SIZE + CELL_SIZE / 2), height - int(r * CELL_SIZE + CELL_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, COLOR_YELLOW, (int(c * CELL_SIZE + CELL_SIZE / 2), height - int(r * CELL_SIZE + CELL_SIZE / 2)), RADIUS)
    pygame.display.update()

def main():
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while True:
        try:
            board = n.send("get")
        except:
            print("Couldn't get game")
            break

        render_board(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = event.pos[0]
                selected_col = int(math.floor(mouse_x / CELL_SIZE))
                n.send(str(selected_col))

        if board is not None and len(np.unique(board)) < 3:  # game is ongoing
            continue

        pygame.time.wait(2000)
        n.send("reset")

if __name__ == "__main__":
    main()

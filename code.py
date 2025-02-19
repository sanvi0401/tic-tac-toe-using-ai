import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe AI")

# Define colors
WHITE = (255, 255, 255)
LINE_COLOR = (28, 170, 156)
X_COLOR = (242, 85, 96)
O_COLOR = (28, 170, 156)

# Define fonts
font = pygame.font.SysFont('Arial', 40)

# Create a 3x3 board
board = [[None for _ in range(3)] for _ in range(3)]

# Draw grid lines
def draw_lines():
    screen.fill(WHITE)
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, 100), (300, 100), 2)
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (300, 200), 2)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (100, 0), (100, 300), 2)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 300), 2)

# Draw X or O in the cells
def draw_marks():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                pygame.draw.line(screen, X_COLOR, (col * 100 + 20, row * 100 + 20), 
                                 (col * 100 + 80, row * 100 + 80), 5)
                pygame.draw.line(screen, X_COLOR, (col * 100 + 20, row * 100 + 80), 
                                 (col * 100 + 80, row * 100 + 20), 5)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, O_COLOR, (col * 100 + 50, row * 100 + 50), 40, 5)

# Check if a player has won
def check_winner(player):
    # Check rows and columns
    for row in range(3):
        if all([board[row][col] == player for col in range(3)]) or \
           all([board[col][row] == player for col in range(3)]):
            return True
    # Check diagonals
    if all([board[i][i] == player for i in range(3)]) or \
       all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

# Check if the board is full
def is_board_full():
    return all([board[row][col] is not None for row in range(3) for col in range(3)])

# Minimax Algorithm to choose AI's move
def minimax(board, depth, is_maximizing):
    # Base case: Check for a winner or draw
    if check_winner('O'):
        return 1
    if check_winner('X'):
        return -1
    if is_board_full():
        return 0
    
    # Maximizing for AI (O)
    if is_maximizing:
        max_eval = -math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[row][col] = None
                    max_eval = max(max_eval, eval)
        return max_eval
    # Minimizing for player (X)
    else:
        min_eval = math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[row][col] = None
                    min_eval = min(min_eval, eval)
        return min_eval

# Get the best move for AI
def get_best_move():
    best_score = -math.inf
    best_move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = 'O'
                score = minimax(board, 0, False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

# Main game loop
def main():
    running = True
    player_turn = True  # Player plays first
    
    while running:
        draw_lines()
        draw_marks()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                x, y = event.pos
                row, col = x // 100, y // 100
                if board[row][col] is None:
                    board[row][col] = 'X'
                    if check_winner('X'):
                        draw_marks()
                        pygame.display.update()
                        pygame.time.wait(2000)
                        print("Player Wins!")
                        running = False
                    elif is_board_full():
                        draw_marks()
                        pygame.display.update()
                        pygame.time.wait(2000)
                        print("It's a Draw!")
                        running = False
                    else:
                        player_turn = False

        # AI's move
        if not player_turn:
            row, col = get_best_move()
            board[row][col] = 'O'
            if check_winner('O'):
                draw_marks()
                pygame.display.update()
                pygame.time.wait(2000)
                print("AI Wins!")
                running = False
            elif is_board_full():
                draw_marks()
                pygame.display.update()
                pygame.time.wait(2000)
                print("It's a Draw!")
                running = False
            else:
                player_turn = True

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

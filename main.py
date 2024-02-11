import pygame
import random

icon = pygame.image.load('icon.ico')
pygame.display.set_icon(icon)

# Constants
ROWS = 10
COLS = 10
MINE_COUNT = 10
CELL_SIZE = 40
BORDER_SIZE = 50

# Colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Calculate window dimensions
WIDTH = COLS * CELL_SIZE + 2 * BORDER_SIZE
HEIGHT = ROWS * CELL_SIZE + 2 * BORDER_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Fonts
font = pygame.font.SysFont(None, 40)

# Game states
game_over = False
game_won = False
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
flags = [[False for _ in range(COLS)] for _ in range(ROWS)]
show_mines = False  # Flag to show mines

# Load the mine icon
mine_icon = pygame.image.load('assets/mine.png').convert_alpha()
mine_icon = pygame.transform.scale(mine_icon, (CELL_SIZE, CELL_SIZE))
flag_icon = pygame.image.load('assets/flag.png')
flag_icon = pygame.transform.scale(flag_icon, (CELL_SIZE, CELL_SIZE))

# Function to calculate remaining flags
def calculate_remaining_flags():
    total_flags = sum(row.count(True) for row in flags)
    remaining_flags = MINE_COUNT - total_flags
    return remaining_flags

# Function to draw remaining flags count
def draw_remaining_flags():
    remaining_flags = calculate_remaining_flags()
    flags_text = font.render(f"Flags: {remaining_flags}", True, BLACK)
    screen.blit(flags_text, (10, HEIGHT - CELL_SIZE))

# Function to draw the game board
def draw_board():
    screen.fill(GRAY)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(
                BORDER_SIZE + col * CELL_SIZE,
                BORDER_SIZE + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

            if revealed[row][col]:
                if board[row][col] == -1:  # If it's a mine
                    mine_icon_x = BORDER_SIZE + col * CELL_SIZE + (CELL_SIZE - mine_icon.get_width()) // 2
                    mine_icon_y = BORDER_SIZE + row * CELL_SIZE + (CELL_SIZE - mine_icon.get_height()) // 2
                    screen.blit(mine_icon, (mine_icon_x, mine_icon_y))
                else:
                    text = font.render(str(board[row][col]), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
            elif flags[row][col]:
                flag_icon_x = BORDER_SIZE + col * CELL_SIZE + (CELL_SIZE - flag_icon.get_width()) // 2
                flag_icon_y = BORDER_SIZE + row * CELL_SIZE + (CELL_SIZE - flag_icon.get_height()) // 2
                screen.blit(flag_icon, (flag_icon_x, flag_icon_y))

    draw_remaining_flags()  # Draw remaining flags count

    if game_over:
        lose_font= pygame.font.SysFont(None, 50)
        game_over_text = lose_font.render("YOU EXPLODED!", True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 12))
        screen.blit(game_over_text, text_rect)
        draw_play_again_button()

    if game_won:
        win_font= pygame.font.SysFont(None, 50)
        game_won_text = win_font.render("CONGRATS, You Win!", True, RED)
        text_rect = game_won_text.get_rect(center=(WIDTH // 2, HEIGHT // 12))
        screen.blit(game_won_text, text_rect)
        draw_play_again_button()


def draw_play_again_button():
    # Draw the "Play Again" button
    play_again_rect = pygame.Rect(0, HEIGHT - CELL_SIZE, WIDTH, CELL_SIZE)
    pygame.draw.rect(screen, WHITE, play_again_rect)
    play_again_text = font.render("--> Play Again <--", True, BLACK)
    text_rect = play_again_text.get_rect(center=play_again_rect.center)
    screen.blit(play_again_text, text_rect)


# Function to place mines on the board
def place_mines(click_row, click_col):
    mine_count = 0
    while mine_count < MINE_COUNT:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        if board[row][col] != -1 and not (row == click_row and col == click_col):
            board[row][col] = -1
            mine_count += 1


# Function to count adjacent mines for each cell
def count_adjacent_mines():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != -1:
                count = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= row + i < ROWS and 0 <= col + j < COLS and board[row + i][col + j] == -1:
                            count += 1
                board[row][col] = count


# Function to reveal cells recursively
def reveal_cells(row, col):
    if 0 <= row < ROWS and 0 <= col < COLS and not revealed[row][col] and not flags[row][col]:
        revealed[row][col] = True
        if board[row][col] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    reveal_cells(row + i, col + j)


# Function to handle game over
def handle_game_over():
    global game_over
    game_over = True


# Function to handle win condition
def handle_game_won():
    global game_won
    game_won = True


# Function to reset the game
def reset_game():
    global board, revealed, flags, game_over, game_won
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flags = [[False for _ in range(COLS)] for _ in range(ROWS)]
    game_over = False
    game_won = False
    place_mines(-1, -1)
    count_adjacent_mines()


# Function to draw the title screen
def draw_title_screen():
    screen.fill(WHITE)
    # Define fonts
    title_font = pygame.font.SysFont(None, 80)
    subtitle_font = pygame.font.SysFont(None, 40)  # Adjust the font size here

    # Render the title text
    title_text = title_font.render("Minesweeper", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)

    # Render the subtitle text
    subtitle_text = subtitle_font.render("By Kris Manangan", True, BLACK)
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(subtitle_text, subtitle_rect)

    button_font = pygame.font.SysFont(None, 40)

    # Play button
    play_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
    pygame.draw.rect(screen, GRAY, play_button_rect)
    play_text = button_font.render("Play", True, BLACK)
    play_text_rect = play_text.get_rect(center=play_button_rect.center)
    screen.blit(play_text, play_text_rect)

    

    pygame.display.flip()


# Modify the main() function
def main():
    global game_over, game_won

    title_screen = True
    game_running = True

    while game_running:
        if title_screen:
            draw_title_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if WIDTH // 4 <= x <= WIDTH // 4 + WIDTH // 2:
                        if HEIGHT // 2 <= y <= HEIGHT // 2 + 50:
                            title_screen = False
                            reset_game()
                        elif HEIGHT // 2 + 100 <= y <= HEIGHT // 2 + 150:
                            # Handle Rules button click (not implemented)
                            pass
                        elif HEIGHT // 2 + 200 <= y <= HEIGHT // 2 + 250:
                            # Handle Settings button click (not implemented)
                            pass
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not game_won:
                    x, y = pygame.mouse.get_pos()
                    row = (y - BORDER_SIZE) // CELL_SIZE
                    col = (x - BORDER_SIZE) // CELL_SIZE

                    if event.button == 1:  # Left click
                        if board[row][col] == -1:
                            handle_game_over()
                            # Reveal all mines when one mine is clicked
                            for r in range(ROWS):
                                for c in range(COLS):
                                    if board[r][c] == -1:
                                        revealed[r][c] = True
                        else:
                            reveal_cells(row, col)
                            if all(all(revealed[row][col] or board[row][col] == -1 for col in range(COLS)) for row in range(ROWS)):
                                handle_game_won()
                    elif event.button == 3:  # Right click
                        if not revealed[row][col]:  # Check if the cell is unrevealed
                            if not flags[row][col] and calculate_remaining_flags() > 0:
                                flags[row][col] = True
                            elif flags[row][col]:
                                flags[row][col] = False

                elif event.type == pygame.MOUSEBUTTONDOWN and (game_over or game_won):
                    if HEIGHT - CELL_SIZE <= event.pos[1] <= HEIGHT:
                        title_screen = True 
                        reset_game()

            draw_board()
            pygame.display.flip()

    pygame.quit()


# Call the main function
if __name__ == "__main__":
    main()

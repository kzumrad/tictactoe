'''
A simple TicTacToe game involving two players.
'''
# importing and initialize the pygame
import pygame
import numpy as np

pygame.init()

# setting up the drawing window
game_win = pygame.display.set_mode([600, 600])
pygame.display.set_caption("Tic Tac Toe")

# some constants
space_cross = 45
width_cross = 20


def draw_main():
    game_win.fill("skyblue")
    # draw the lines - vertical
    pygame.draw.line(game_win, "steelblue", (200, 0), (200, 600), 8)
    pygame.draw.line(game_win, "steelblue", (400, 0), (400, 600), 8)
    # draw the lines - horizontal
    pygame.draw.line(game_win, "steelblue", (0, 200), (600, 200), 8)
    pygame.draw.line(game_win, "steelblue", (0, 400), (600, 400), 8)


# setting board - for tracking the game
board_rows = 3
board_cols = 3
board = np.zeros((board_rows, board_cols))


# mark_square --> function for players to mark the spot
def mark_square(row, col, player_id):
    board[row][col] = player_id


# an available square would be the one that is not marked
def available_square(row, col):
    return board[row][col] == 0


# checking if there are any available squares
def is_board_full():
    return 0 not in board


# drawing figures
def draw_figures():
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 1:
                pygame.draw.circle(game_win, "bisque", (int(col * 200 + 100), int(row * 200 + 100)), 75, 15)
            if board[row][col] == 2:
                pygame.draw.line(game_win, "rosybrown", (int(col * 200) + space_cross, int(row * 200) + space_cross),
                                 (int(col * 200 + 200) - space_cross, int(row * 200 + 200) - space_cross), width_cross)
                pygame.draw.line(game_win, "rosybrown",
                                 (int(col * 200 + 200) - space_cross, int(row * 200) + space_cross),
                                 (int(col * 200) + space_cross, int(row * 200 + 200) - space_cross), width_cross)
    if find_winner() != "":
        draw_winner()


def diag_reverse(array_in):
    array_out = []
    y = len(array_in[0]) - 1
    for x in range(len(array_in[0])):
        array_out.append(array_in[x][y])
        y -= 1
    return array_out


# finding who the winner is
def find_winner():
    winner = ""
    diag_prod = np.prod(board.diagonal())
    diag_reverse_prod = np.prod(diag_reverse(board))
    if diag_prod == 1 or diag_reverse_prod == 1:
        winner = "PLAYER 1"
    if diag_prod == 8 or diag_reverse_prod == 8:
        winner = "PLAYER 2"
    # checking the rows and columns
    if diag_prod != 1 or diag_prod != 8 or diag_reverse_prod != 1 or diag_reverse_prod != 8:
        for num in range(len(board[0])):
            if np.prod(board[num]) == 1 or np.prod(np.transpose(board)[num]) == 1:
                winner = "PLAYER 1"
            if np.prod(board[num]) == 8 or np.prod(np.transpose(board)[num]) == 8:
                winner = "PLAYER 2"
    return winner


def draw_winner():
    diag_prod = np.prod(board.diagonal())
    diag_reverse_prod = np.prod(diag_reverse(board))
    if diag_prod == 1 or diag_prod == 8:
        pygame.draw.line(game_win, "steelblue", (30, 30), (570, 570), 8)
    if diag_reverse_prod == 1 or diag_reverse_prod == 8:
        pygame.draw.line(game_win, "steelblue", (570, 30), (30, 570), 8)
    if diag_prod != 1 or diag_prod != 8 or diag_reverse_prod != 1 or diag_reverse_prod != 8:
        for num in range(len(board[0])):
            if np.prod(board[num]) == 1 or np.prod(board[num]) == 8:
                pygame.draw.line(game_win, "steelblue", (30, num*200 + 100), (570, num*200 + 100), 8)
            if np.prod(np.transpose(board)[num]) == 1 or np.prod(np.transpose(board)[num]) == 8:
                pygame.draw.line(game_win, "steelblue", (num * 200 + 100, 30), (num * 200 + 100, 570), 8)


def display_message(message, font_size):
    font = pygame.font.SysFont(None, font_size)
    img = font.render(message, True, "steelblue")
    return img


# running until a user asks to quit
draw_main()
running = True
player = 1
while running:

    # if the user clicks the window close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # linking board to game_win
            mouse_xcor = event.pos[0]  # x-cor
            mouse_ycor = event.pos[1]  # y-cor

            clicked_row = int(mouse_ycor // 200)
            clicked_col = int(mouse_xcor // 200)

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                draw_figures()
                player = player % 2 + 1

        # updating teh contents of the display to the screen
        # Without this call, nothing appears in the window
        pygame.display.update()

        if find_winner() != "":
            pygame.time.delay(1000)
            game_win.fill("skyblue")
            game_win.blit(display_message("THE WINNER IS " + find_winner() + "!", 40), (125, 250))
            game_win.blit(display_message("PRESS THE \"SPACE\" BAR TO PLAY AGAIN.", 30), (100, 300))

        if is_board_full() and find_winner() == "":
            pygame.time.delay(1000)
            game_win.fill("skyblue")
            game_win.blit(display_message("IT'S A TIE!", 40), (225, 250))
            game_win.blit(display_message("PRESS THE \"SPACE\" BAR TO PLAY AGAIN.", 30), (100, 300))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                draw_main()
                board = np.zeros((board_rows, board_cols))

# exiting pygame - this happens once the loop finishes
pygame.quit()

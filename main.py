import pygame
import board

WIDTH = 600
HEIGHT = 700

BLUE = (0, 0, 255)

CHOICE_RECT = pygame.Rect(0, 0, WIDTH, 100)

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Connect Four')

playing_board = board.Board(rows = 7, cols = 7, left_corner_x = 0, left_corner_y = 100, width = 600, height = 600, color = BLUE)
playing_board.draw(SCREEN)

pygame.display.update()

running = True
choice_col = -1
choice_row = -1

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            if(CHOICE_RECT.collidepoint(mouse_pos)):
                for i in range(playing_board.get_num_cols()):
                    if(i * playing_board.get_width() / playing_board.get_num_cols() < mouse_pos[0] and mouse_pos[0] <= (i + 1) * playing_board.get_width() / playing_board.get_num_cols()):
                        choice_col = i
                        break
                print(f"choice_col: {choice_col}")

                if(playing_board.get_chip_matrix()[playing_board.get_num_rows() - 1][choice_col] == 0):
                    choice_row = playing_board.get_num_rows() - 1

                if(choice_row == -1):
                    for i in range(playing_board.get_num_rows()):
                        if(playing_board.get_chip_matrix()[i][choice_col] != 0):
                            choice_row = i - 1
                            break
                print(f"choice_row: {choice_row}")

                playing_board.set_chip_matrix(choice_row, choice_col, 1)
                playing_board.draw(SCREEN)

                choice_row = -1
                choice_col = -1

    pygame.display.update()

pygame.quit()

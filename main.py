import pygame
import pymunk
import board
import button
import numpy as np
import pymunk.pygame_util

WIDTH = 800
HEIGHT = 700

WHITE = (255, 255, 255)
BLUE = (0, 0, 255, 100)
BLACK = (0, 0, 0, 100)
RED = (255, 0, 0, 10)
YELLOW = (255, 255, 0, 10)

pygame.init()
CLOCK = pygame.time.Clock()
FPS = 50
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Connect Four')

def create_chip(center_x: int, center_y: int, radius: int, disk_color, space):
    body = pymunk.Body()
    body.position = (center_x, center_y)

    shape = pymunk.Circle(body, radius)
    shape.color = disk_color
    shape.mass = 1
    shape.elasticity = 0.4
    shape.friction = 0.6
    space.add(body, shape)

    return body

def draw_text(font_size: int, text: str, center_position: tuple[int, int], text_color: tuple[int, int, int] = WHITE, background_color: tuple[int, int, int] = BLACK):
	font = pygame.font.SysFont(None, font_size)
	text_render = font.render(text, True, text_color, background_color)
	text_rect = text_render.get_rect()
	text_rect.center = center_position
	SCREEN.blit(text_render, text_rect)

def get_time_text(time: int) -> str:
    if time >= 60 and time % 60 >= 10:
        time_text = f"{int(time/60)}: {time % 60}"
    if time >= 60 and time % 60 < 10:
        time_text = f"{int(time/60)}: 0{time % 60}"
    elif time >= 10:
        time_text = f"0: {time}"
    else:
        time_text = f"0: 0{time}"
    
    return time_text

def create_boundaries(playing_board: np.array, empty_row_per_col: np.array, space):
    choice_row = -1
    for c in range(playing_board.get_num_cols()):
        if(playing_board.get_chip_matrix()[playing_board.get_num_rows() - 1][c] == 0):
            choice_row = playing_board.get_num_rows() - 1

        if(choice_row == -1):
            for r in range(playing_board.get_num_rows()):
                if(playing_board.get_chip_matrix()[r][c] != 0):
                    choice_row = r - 1
                    break
        
        empty_row_per_col = np.append(empty_row_per_col, choice_row)
        choice_row = -1

    rects = np.array([])
    rect_width = playing_board.get_width() / playing_board.get_num_cols()
    rect_height = playing_board.get_buffer()
    for i in range(len(empty_row_per_col)):
         rects = np.append(rects, [playing_board.get_left_corner_x() + rect_width / 2 + i * (2 * playing_board.get_token_radius() + playing_board.get_buffer()), 
                                   playing_board.get_left_corner_y() + rect_height / 2 + (empty_row_per_col[i] + 1) * (2 * playing_board.get_token_radius() + playing_board.get_buffer()), 
                                   rect_width, 
                                   rect_height])
    
    rects = rects.reshape((7, 4))

    for i in range(rects.shape[0]):
         body = pymunk.Body(body_type = pymunk.Body.STATIC)
         body.position = rects[i][0], rects[i][1]
         shape = pymunk.Poly.create_box(body, (rects[i][2], rects[i][3]))
         shape.elasticity = 0.4
         shape.friction = 1
         shape.color = BLACK
         space.add(body, shape)


def run_game():
    CHOICE_RECT = pygame.Rect(100, 0, 600, 100)

    SPACE1 = pymunk.Space()
    SPACE2 = pymunk.Space()
    SPACE1.gravity = (0, 9000)

    WAIT_TIME = 500

    playing_board = board.Board(rows = 7, cols = 7, left_corner_x = 100, left_corner_y = 100, width = 600, height = 600, color = BLUE)
    playing_board.draw(SPACE2)
    # playing_board.draw(SPACE2)
    pygame.display.update()

    running = True
    choice_col = -1
    choice_row = -1
    player_one = True
    game_over = False
    player_one_time = 10
    player_two_time = 10
    time_after_click = -(WAIT_TIME + 1000)

    player_one_time_event = pygame.USEREVENT + 1
    pygame.time.set_timer(player_one_time_event, 1000)
    player_two_time_event = pygame.USEREVENT + 1
    pygame.time.set_timer(player_two_time_event, 1000)

    DRAW_OPTIONS = pymunk.pygame_util.DrawOptions(SCREEN)

    MENU_BUTTON = button.Button(WHITE, 350, 50, 150, 50, pygame.font.SysFont(None, 30), "Menu")
    PLAY_AGAIN_BUTTON = button.Button(WHITE, 550, 50, 150, 50, pygame.font.SysFont(None, 30), "Play Again")

    while running:
        SCREEN.fill(BLACK)

        if(not game_over):
            player_one_time_text = get_time_text(player_one_time)
            player_two_time_text = get_time_text(player_two_time)
        else:
            MENU_BUTTON.draw(SCREEN)
            PLAY_AGAIN_BUTTON.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()

                if(CHOICE_RECT.collidepoint(mouse_pos) and not game_over and pygame.time.get_ticks() - time_after_click >= WAIT_TIME):
                    time_after_click = pygame.time.get_ticks()

                    empty_row_per_col = np.array([])
                    create_boundaries(playing_board, empty_row_per_col, SPACE1)

                    for i in range(playing_board.get_num_cols()):
                        if(playing_board.get_left_corner_x() + i * playing_board.get_width() / playing_board.get_num_cols() < mouse_pos[0] and mouse_pos[0] <= playing_board.get_left_corner_x() + (i + 1) * playing_board.get_width() / playing_board.get_num_cols()):
                            choice_col = i
                            break

                    if(playing_board.get_chip_matrix()[playing_board.get_num_rows() - 1][choice_col] == 0):
                        choice_row = playing_board.get_num_rows() - 1

                    if(choice_row == -1):
                        for i in range(playing_board.get_num_rows()):
                            if(playing_board.get_chip_matrix()[i][choice_col] != 0):
                                choice_row = i - 1
                                break
                    if(choice_row != 1):
                        create_chip((choice_col + 5) * playing_board.get_buffer() + (2 * choice_col + 3) * playing_board.get_token_radius(), playing_board.get_token_radius(), playing_board.get_token_radius(), RED if player_one else YELLOW, SPACE1)

                    playing_board.set_chip_matrix(choice_row, choice_col, 1 if player_one else -1)

                    choice_row = -1
                    choice_col = -1
                    player_one = not player_one
            
            elif(event.type == player_one_time_event and player_one and not game_over):
                player_one_time -= 1
                if player_one_time == 0:
                    game_over = True
            elif(event.type == player_two_time_event and not player_one and not game_over):
                player_two_time -= 1
                if player_two_time == 0:
                    game_over = True


        draw_text(50, player_one_time_text, (50, 25), WHITE, BLACK)
        draw_text(50, player_two_time_text, (WIDTH - 50, 25), WHITE, BLACK)

        if(playing_board.check_win() == 1):
            draw_text(50, "Player 1 Wins", (210, 80), WHITE, BLACK)
            game_over = True
        elif(playing_board.check_win() == -1):
            draw_text(50, "Player 2 Wins", (210, 80), WHITE, BLACK)
            game_over = True
        elif(playing_board.check_win() == 2):
            draw_text(50, "Game is a Tie", (210, 80), WHITE, BLACK)
            game_over = True

        SPACE2.debug_draw(DRAW_OPTIONS)
        SPACE1.debug_draw(DRAW_OPTIONS)
        
        SPACE1.step(1 / FPS)
        SPACE2.step(1 / FPS)

        CLOCK.tick(FPS)
        pygame.display.update()

    pygame.quit()

run_game()

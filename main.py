import pygame
import pymunk
import pymunk.pygame_util
import board
import button
import dropdown
import numpy as np

WIDTH = 800
HEIGHT = 700

WHITE = (255, 255, 255, 100)
BLUE = (0, 0, 255, 100)
BLACK = (0, 0, 0, 100)
RED = (255, 0, 0, 10)
GREEN = (0, 255, 0, 100)
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

    return shape, body

def draw_text(font_size: int, text: str, center_position: tuple[int, int], text_color: tuple[int, int, int] = WHITE, background_color: tuple[int, int, int] = BLACK):
    font = pygame.font.SysFont(None, font_size)
    text_render = font.render(text, True, text_color, background_color)
    text_rect = text_render.get_rect()
    text_rect.center = center_position
    SCREEN.blit(text_render, text_rect)

    return text_rect

def get_time_text(time: int) -> str:
    if time >= 60 and time % 60 >= 10:
        time_text = f"{int(time/60)}: {time % 60}"
    elif time >= 60 and time % 60 < 10:
        time_text = f"{int(time/60)}: 0{time % 60}"
    elif time >= 10:
        time_text = f"0: {time}"
    else:
        time_text = f"0: 0{time}"
    
    return time_text

def create_boundaries(playing_board: np.array, space):
    choice_row = -1
    empty_row_per_col = np.array([])
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
    
    rect_shapes = np.array([])
    rect_bodies = np.array([])
    rect_width = 2 * playing_board.get_token_radius()
    rect_height = playing_board.get_buffer()
    for i in range(len(empty_row_per_col)):
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = (playing_board.get_left_corner_x() + (2 * i + 1) * playing_board.get_token_radius() + (i + 1) * playing_board.get_buffer(), 
                        playing_board.get_left_corner_y() + (empty_row_per_col[i] + 1) * 2 * playing_board.get_token_radius() + (empty_row_per_col[i] + 1.5) * playing_board.get_buffer())
        
        shape = pymunk.Poly.create_box(body, (rect_width, rect_height))
        shape.elasticity = 0.4
        shape.friction = 1
        shape.color = BLUE
        space.add(body, shape)

        rect_shapes = np.append(rect_shapes, shape)
        rect_bodies = np.append(rect_bodies, body)

    return rect_shapes, rect_bodies

def run_game(game_time: int, size: str, consecutive_tokens: int) -> bool:
    SIZE_TO_NUM = {"Small": 8, "Normal": 10, "Medium": 12, "Large": 14}

    SPACE1 = pymunk.Space()
    SPACE2 = pymunk.Space()
    SPACE1.gravity = (0, 1000)

    WAIT_TIME = 1200
    time_after_click = -(WAIT_TIME + 1000)

    playing_board = board.Board(rows = SIZE_TO_NUM[size], cols = SIZE_TO_NUM[size], left_corner_x = 100, left_corner_y = 100, width = 600, height = 600, color = BLUE, consecutive_tokens = consecutive_tokens)
    CHOICE_RECT = pygame.Rect(playing_board.get_left_corner_x(), 0, playing_board.get_width(), 100)
    playing_board.draw(SPACE2)

    token_shapes = np.array([])
    token_bodies = np.array([])
    rect_shapes = np.array([])
    rect_bodies = np.array([])

    running = True

    choice_col = -1
    choice_row = -1
    player_one = True
    game_over = False

    win_line_start_pos = None
    win_line_end_pos = None

    player_one_time = game_time
    player_two_time = game_time
    player_one_time_event = pygame.USEREVENT + 1
    pygame.time.set_timer(player_one_time_event, 1000)
    player_two_time_event = pygame.USEREVENT + 1
    pygame.time.set_timer(player_two_time_event, 1000)

    DRAW_OPTIONS = pymunk.pygame_util.DrawOptions(SCREEN)

    MENU_BUTTON = button.Button(WHITE, left_corner_x = 350, left_corner_y = 50, width = 175, height = 50, font_size = 40, text = "Menu")
    PLAY_AGAIN_BUTTON = button.Button(WHITE, left_corner_x = 550, left_corner_y = 50, width = 175, height = 50, font_size = 40, text = "Play Again")

    while running:
        SCREEN.fill(BLACK)

        player_one_time_text = get_time_text(player_one_time)
        player_two_time_text = get_time_text(player_two_time)
        player_one_time_text_rect = draw_text(50, player_one_time_text, (50, 25), RED if player_one_time == 0 else WHITE, BLACK)
        player_two_time_text_rect = draw_text(50, player_two_time_text, (WIDTH - 50, 25), RED if player_two_time == 0 else WHITE, BLACK)

        if(game_over):
            MENU_BUTTON.draw(SCREEN)
            PLAY_AGAIN_BUTTON.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()

                if(MENU_BUTTON.is_over_mouse(mouse_pos) and game_over):
                    return True
                
                elif(PLAY_AGAIN_BUTTON.is_over_mouse(mouse_pos) and game_over):
                    playing_board.draw(SPACE2, True)
                    playing_board.clear_chip_matrix()

                    player_one = True
                    game_over = False
                    player_one_time = game_time
                    player_two_time = game_time

                    for i in range(len(token_shapes)):
                        SPACE1.remove(token_shapes[i], token_bodies[i])
                    for i in range(len(rect_shapes)):
                        SPACE1.remove(rect_shapes[i], rect_bodies[i])

                    token_shapes = np.array([])
                    token_bodies = np.array([])
                    rect_shapes = np.array([])
                    rect_bodies = np.array([])

                elif(CHOICE_RECT.collidepoint(mouse_pos) and not game_over and pygame.time.get_ticks() - time_after_click >= WAIT_TIME):
                    time_after_click = pygame.time.get_ticks()

                    new_rect_shapes, new_rect_bodies = create_boundaries(playing_board, SPACE1)
                    rect_shapes = np.append(rect_shapes, new_rect_shapes)
                    rect_bodies = np.append(rect_bodies, new_rect_bodies)

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

                    if(choice_row != -1):
                        token_shape, token_body = create_chip(playing_board.get_left_corner_x() + (choice_col + 1) * playing_board.get_buffer() + (2 * choice_col + 1) * playing_board.get_token_radius(), 
                                    playing_board.get_token_radius(), 
                                    playing_board.get_token_radius(), 
                                    RED if player_one else YELLOW, 
                                    SPACE1)
                        
                        token_shapes = np.append(token_shapes, token_shape)
                        token_bodies = np.append(token_bodies, token_body)

                        playing_board.set_chip_matrix(choice_row, choice_col, 1 if player_one else -1)

                        choice_row = -1
                        choice_col = -1
                        player_one = not player_one
            
            elif(event.type == player_one_time_event and player_one and not game_over):
                player_one_time -= 1
                SCREEN.fill(BLACK, player_one_time_text_rect)
                player_one_time_text_rect = draw_text(50, player_one_time_text, (50, 25), WHITE, BLACK)

            elif(event.type == player_two_time_event and not player_one and not game_over):
                player_two_time -= 1
                SCREEN.fill(BLACK, player_two_time_text_rect)
                player_two_time_text_rect = draw_text(50, player_two_time_text, (WIDTH - 50, 25), WHITE, BLACK)

        result, win_line_start_pos, win_line_end_pos =  playing_board.check_win()
        if(result == 1):
            draw_text(50, "Player 1 Wins", (210, 80), WHITE, BLACK)
            game_over = True
        elif(result == -1):
            draw_text(50, "Player 2 Wins", (210, 80), WHITE, BLACK)
            game_over = True
        elif(result == 2):
            draw_text(50, "Game is a Tie", (210, 80), WHITE, BLACK)
            game_over = True
        elif(player_one_time == 0):
            draw_text(30, "Player 1 Ran Out of Time", (210, 50), WHITE, BLACK)
            draw_text(30, "Player 2 Wins", (210, 80), WHITE, BLACK)
            game_over = True
        elif(player_two_time == 0):
            draw_text(30, "Player 2 Ran Out of Time", (210, 50), WHITE, BLACK)
            draw_text(30, "Player 1 Wins", (210, 80), WHITE, BLACK)
            game_over = True

        SPACE2.debug_draw(DRAW_OPTIONS)
        SPACE1.debug_draw(DRAW_OPTIONS)
        
        SPACE1.step(1 / FPS)
        SPACE2.step(1 / FPS)

        if(win_line_start_pos != None and win_line_end_pos != None):
            # print(win_line_start_pos)
            # print(win_line_end_pos)
            pygame.draw.line(SCREEN, GREEN, win_line_start_pos, win_line_end_pos, 10)

        CLOCK.tick(FPS)
        pygame.display.update()
    
    return False

def menu():
    SCREEN.fill(BLACK)

    start_game = False

    draw_text(80, "CONNECT-N", (WIDTH/2, 50), WHITE, BLACK)

    START_BUTTON = button.Button(BLUE, WIDTH/2 - 100, HEIGHT/2 - 200, 200, 100, 50, "Start")
    START_BUTTON.draw(SCREEN)

    TIME_DROPDOWN = dropdown.DropDown(button.Button(WHITE, 50, 275, 200, 80, text = "Choose Time", font_size = 30), options = np.array(["30", "60", "90", "120"]))
    TIME_DROPDOWN.draw(SCREEN)

    SIZE_DROPDOWN = dropdown.DropDown(button.Button(WHITE, 300, 275, 200, 80, text = "Choose Size", font_size = 30), options = np.array(["Small", "Normal", "Medium", "Large"]))
    SIZE_DROPDOWN.draw(SCREEN)

    CONSECUTIVE_TOKENS_DROPDOWN = dropdown.DropDown(button.Button(WHITE, 550, 275, 200, 80, text = "Choose Consecutive", font_size = 30), options = np.array(["4", "5", "6", "7"]))
    CONSECUTIVE_TOKENS_DROPDOWN.draw(SCREEN)

    while not start_game:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
            
            if(event.type == pygame.MOUSEBUTTONUP):
                mouse_pos = pygame.mouse.get_pos()

                if(START_BUTTON.is_over_mouse(mouse_pos)):
                    start_game = True
                elif(TIME_DROPDOWN.is_over_mouse(mouse_pos)):
                    TIME_DROPDOWN.update(SCREEN)
                elif(SIZE_DROPDOWN.is_over_mouse(mouse_pos)):
                    SIZE_DROPDOWN.update(SCREEN)
                elif(CONSECUTIVE_TOKENS_DROPDOWN.is_over_mouse(mouse_pos)):
                    CONSECUTIVE_TOKENS_DROPDOWN.update(SCREEN)

        pygame.display.update()
    
    return int(TIME_DROPDOWN.get_current_option()), SIZE_DROPDOWN.get_current_option(), int(CONSECUTIVE_TOKENS_DROPDOWN.get_current_option())

while True:
    exit = False
    GAME_TIME, BOARD_SIZE, CONSECUTIVE_TOKENS = menu()
    while not exit:
        exit = run_game(game_time = GAME_TIME, size = BOARD_SIZE, consecutive_tokens = CONSECUTIVE_TOKENS)
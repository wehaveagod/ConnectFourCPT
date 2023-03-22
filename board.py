import pygame
import numpy as np

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
NUMS_TO_COLORS = {1: RED, -1: YELLOW, 0: BLACK}
BUFFER = 5

class Board:
    def __init__(self, rows: int, cols: int, left_corner_x: int, left_corner_y: int, width: int, height: int, color: tuple[int, int, int]):
        self.rows = rows
        self.cols = cols

        self.left_corner_x = left_corner_x
        self.left_corner_y = left_corner_y

        self.width = width
        self.height = height

        self.color = color

        self.chip_matrix = np.zeros((self.rows, self.cols), int)

    def draw(self, window: pygame.display):
        pygame.draw.rect(window, self.color, (self.left_corner_x, self.left_corner_y, self.width, self.height), 0)

        radius = (self.height - (self.rows + 1) * BUFFER) / (2 * self.rows)

        for i in range(self.rows):
            for j in range(self.cols):
                pygame.draw.circle(window, 
                                   NUMS_TO_COLORS[self.chip_matrix[i][j]], 
                                   (self.left_corner_x + (j + 1) * BUFFER + (2 * j + 1) * radius, 
                                    self.left_corner_y + (i + 1) * BUFFER + (2 * i + 1) * radius), 
                                   radius)
    
    def clear_display(self, window: pygame.display):
        buffer = 5
        radius = (self.height - (self.rows + 1) * buffer) / (2 * self.rows)

        for i in range(self.rows):
            for j in range(self.cols):
                pygame.draw.circle(window, BLACK, (self.left_corner_x + (i + 1) * buffer + (2 * i + 1) * radius, self.left_corner_y + (j + 1) * buffer + (2 * j + 1) * radius), radius)

        self.chips_matrix = np.zeros((self.rows, self.cols), int)

    def get_num_rows(self):
        return self.rows

    def get_num_cols(self):
        return self.cols

    def get_width(self):
        return self.width
    
    def get_chip_matrix(self):
        return self.chip_matrix
    
    def set_chip_matrix(self, element_x: int, element_y: int, new_num: int):
        self.chip_matrix[element_x][element_y] = new_num
               



